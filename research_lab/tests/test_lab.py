import numpy as np
import pytest
from fastapi.testclient import TestClient
from research_lab.api import app
from research_lab.experiment import generate,features,budget_metrics

def test_past_features_do_not_change_with_future_transactions():
    df=generate(days=2,per_day=20)
    assert np.allclose(features(df)[:15],features(df.iloc[:15]))
    changed=df.copy();changed['label']=1-changed.label
    assert np.allclose(features(df),features(changed))

def test_budget_is_per_day():
    df=generate(days=2,per_day=20)
    result=budget_metrics(df,np.arange(len(df)),3)
    assert result['reviewed']==6

@pytest.fixture
def client(monkeypatch,tmp_path):
    monkeypatch.setenv('FRAUD_DB',str(tmp_path/'db.sqlite'))
    return TestClient(app)

def test_model_is_required(client,monkeypatch,tmp_path):
    monkeypatch.setenv('FRAUD_MODEL',str(tmp_path/'missing'))
    assert client.get('/evidence').json()['ready'] is False
    assert client.post('/transactions',headers={'X-Lab-Key':'local-demo-only'},json={'transaction_id':'a','card_id':'a','amount':1,'time_step':1}).status_code==503

def test_idempotency_conflicts_case_revisions_and_auth(client):
    tx={'transaction_id':'a','card_id':'a','amount':123,'time_step':1};h={'X-Lab-Key':'local-demo-only'}
    assert client.post('/transactions',json=tx).status_code==403
    first=client.post('/transactions',json=tx,headers=h);assert first.status_code==200
    assert client.post('/transactions',json=tx,headers=h).json()==first.json()
    assert len(client.get('/transactions').json())==1
    assert client.post('/transactions',json={**tx,'amount':124},headers=h).status_code==409
    assert client.post('/cases/a/transition',json={'status':'cleared','revision':0},headers=h).status_code==422
    assert client.post('/cases/a/transition',json={'status':'reviewing','revision':0},headers=h).status_code==200
    assert client.post('/cases/a/transition',json={'status':'cleared','revision':0},headers=h).status_code==409
    assert client.post('/cases/a/transition',json={'status':'cleared','revision':1},headers=h).status_code==200
    assert len(client.get('/audit').json())==3

def test_chronology_enforced(client):
    h={'X-Lab-Key':'local-demo-only'};tx={'transaction_id':'b','card_id':'a','amount':12,'time_step':10}
    assert client.post('/transactions',json=tx,headers=h).status_code==200
    assert client.post('/transactions',json={**tx,'transaction_id':'c','time_step':9},headers=h).status_code==409
