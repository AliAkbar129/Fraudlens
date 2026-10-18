"""Local-only research API: trained scores, durable cases, explicit limitations."""
import hashlib,json,os,sqlite3,time
from pathlib import Path
import joblib
from fastapi import FastAPI,HTTPException,Header
from fastapi.responses import FileResponse
from pydantic import BaseModel,Field,ConfigDict
from research_lab.experiment import single_features
app=FastAPI(title='FraudLens Decision Lab',version='0.2.0'); ROOT=Path(__file__).parent
def db():
    path=Path(os.environ.get('FRAUD_DB',str(ROOT/'artifacts/lab.sqlite')));path.parent.mkdir(parents=True,exist_ok=True)
    con=sqlite3.connect(path,timeout=10);con.row_factory=sqlite3.Row;con.execute('PRAGMA journal_mode=WAL')
    con.execute('CREATE TABLE IF NOT EXISTS transactions (id TEXT PRIMARY KEY,payload TEXT NOT NULL,card TEXT NOT NULL,amount REAL NOT NULL,event_time REAL NOT NULL,score REAL NOT NULL,model_version TEXT NOT NULL,status TEXT NOT NULL,revision INTEGER NOT NULL DEFAULT 0)')
    con.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY AUTOINCREMENT,transaction_id TEXT NOT NULL,action TEXT NOT NULL,timestamp REAL NOT NULL)');con.commit();return con
def artifact():
    path=Path(os.environ.get('FRAUD_MODEL',str(ROOT/'artifacts/model.joblib')))
    if not path.exists():raise HTTPException(503,'Train the baseline first; no mock scores are available.')
    a=joblib.load(path)
    if a.get('schema_version')!=1:raise HTTPException(503,'Unsupported artifact')
    return a,hashlib.sha256(path.read_bytes()).hexdigest()
def authorize(token):
    if token!=os.environ.get('FRAUD_LAB_KEY','local-demo-only'):raise HTTPException(403,'Local lab key required')
class Transaction(BaseModel):
    model_config=ConfigDict(allow_inf_nan=False)
    transaction_id:str=Field(min_length=1,max_length=100)
    card_id:str=Field(min_length=1,max_length=100)
    amount:float=Field(gt=0,le=1e9)
    time_step:float=Field(ge=0,le=1e12)
class Transition(BaseModel):
    status:str
    revision:int=Field(ge=0)
@app.get('/')
def home():return FileResponse(ROOT/'index.html')
@app.get('/health')
def health():return {'status':'alive','scope':'local_research_only'}
@app.get('/evidence')
def evidence():
    try:a,digest=artifact()
    except HTTPException as e:return {'ready':False,'reason':e.detail}
    return {'ready':True,'sha256':digest,**a['report']}
@app.post('/transactions')
def ingest(tx:Transaction,x_lab_key:str=Header(default='')):
    authorize(x_lab_key);a,digest=artifact();payload=tx.model_dump_json();con=db()
    try:
        con.execute('BEGIN IMMEDIATE');old=con.execute('SELECT * FROM transactions WHERE id=?',(tx.transaction_id,)).fetchone()
        if old:
            if old['payload']!=payload:raise HTTPException(409,'Same ID with different content')
            return dict(old)
        newest=con.execute('SELECT MAX(event_time) FROM transactions').fetchone()[0]
        if newest is not None and tx.time_step<=newest:raise HTTPException(409,'Live replay requires strictly increasing timestamps.')
        hist=con.execute('SELECT COUNT(*),COALESCE(SUM(amount),0) FROM transactions WHERE card=?',(tx.card_id,)).fetchone()
        score=float(a['model'].predict_proba(single_features(tx.amount,tx.time_step,hist[0],hist[1]))[0,1])
        con.execute('INSERT INTO transactions (id,payload,card,amount,event_time,score,model_version,status) VALUES (?,?,?,?,?,?,?,?)',(tx.transaction_id,payload,tx.card_id,tx.amount,tx.time_step,score,digest,'open'))
        con.execute('INSERT INTO events(transaction_id,action,timestamp) VALUES (?,?,?)',(tx.transaction_id,'scored',time.time()));con.commit()
        return dict(con.execute('SELECT * FROM transactions WHERE id=?',(tx.transaction_id,)).fetchone())
    finally:con.close()
@app.get('/transactions')
def transactions():
    con=db()
    try:return [dict(r) for r in con.execute('SELECT id,card,amount,event_time,score,status,revision FROM transactions ORDER BY score DESC LIMIT 100')]
    finally:con.close()
@app.post('/cases/{identifier}/transition')
def transition(identifier:str,change:Transition,x_lab_key:str=Header(default='')):
    authorize(x_lab_key);con=db()
    try:
        con.execute('BEGIN IMMEDIATE');row=con.execute('SELECT * FROM transactions WHERE id=?',(identifier,)).fetchone()
        if not row:raise HTTPException(404,'Unknown transaction')
        if row['revision']!=change.revision:raise HTTPException(409,'Stale revision; refresh')
        allowed={'open':{'reviewing'},'reviewing':{'confirmed_fraud','cleared'},'confirmed_fraud':set(),'cleared':set()}
        if change.status not in allowed[row['status']]:raise HTTPException(422,'Invalid transition')
        con.execute('UPDATE transactions SET status=?,revision=revision+1 WHERE id=?',(change.status,identifier))
        con.execute('INSERT INTO events(transaction_id,action,timestamp) VALUES (?,?,?)',(identifier,change.status,time.time()));con.commit()
        return {'id':identifier,'status':change.status,'revision':change.revision+1}
    finally:con.close()
@app.get('/audit')
def audit():
    con=db()
    try:return [dict(r) for r in con.execute('SELECT * FROM events ORDER BY seq DESC LIMIT 100')]
    finally:con.close()

@app.get('/benchmarks/ulb')
def ulb_benchmark():
    path = ROOT / 'evidence/ulb/evaluation.json'
    if not path.is_file():
        raise HTTPException(503, 'Real-data benchmark evidence is not installed.')
    return json.loads(path.read_text())
