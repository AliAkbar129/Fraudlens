"""Legacy hybrid endpoint fails explicitly until a validated model is implemented."""
from fastapi import FastAPI,HTTPException
app=FastAPI(title='FraudLens legacy hybrid API',version='0.2.0')
@app.get('/health')
def health():return {'status':'alive','model_status':'not_trained'}
@app.get('/model/info')
def model_info():return {'model_type':'Hybrid GNN+LightGBM (untrained)','version':'not-trained','metrics':{},'last_trained':None}
@app.get('/ready')
def ready():raise HTTPException(503,'Legacy model is not trained. See the research_lab workbench.')
@app.post('/predict')
@app.post('/predict/batch')
@app.post('/explain/{transaction_id}')
def unavailable():raise HTTPException(503,'No validated hybrid artifact is installed; mock scores and explanations are disabled.')
