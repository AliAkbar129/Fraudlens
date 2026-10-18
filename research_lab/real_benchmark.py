"""Chronological ULB/Worldline benchmark; independent from the synthetic live demo."""
import argparse,gzip,hashlib,json,platform,time
from pathlib import Path
import numpy as np,pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score,roc_auc_score,brier_score_loss
from threadpoolctl import threadpool_limits

def load(path):
    with open(path) as f:
        names=[]
        for line in f:
            if line.lower().startswith('@attribute'):names.append(line.split()[1].strip("'\""))
            if line.strip().lower()=='@data':break
        frame=pd.read_csv(f,header=None,names=names)
    frame['Class']=frame['Class'].astype(str).str.strip("'\"").astype(int)
    return frame

def run(path,output):
    start=time.perf_counter();out=Path(output);out.mkdir(parents=True,exist_ok=True)
    df=load(path);original=len(df)
    if original!=284807 or set(df.Class.unique())!={0,1}:raise ValueError('Expected complete OpenML 1597')
    df=df.drop_duplicates().sort_values('Time',kind='stable').reset_index(drop=True)
    t=df.Time.to_numpy();y=df.Class.to_numpy();bounds=np.quantile(t,[.6,.75,.85])
    masks={'train':t<bounds[0],'validation':(t>=bounds[0])&(t<bounds[1]),'calibration':(t>=bounds[1])&(t<bounds[2]),'test':t>=bounds[2]}
    tr,va,ca,te=[masks[k] for k in ['train','validation','calibration','test']]
    features=[c for c in df if c not in ['Time','Class']];x=df[features].to_numpy()
    models={'logistic':make_pipeline(StandardScaler(),LogisticRegression(max_iter=1500,class_weight='balanced',random_state=42)),'hist_gradient_boosting':HistGradientBoostingClassifier(max_iter=100,max_leaf_nodes=15,l2_regularization=1,random_state=42)}
    validation={};scores={}
    for name,m in models.items():
        m.fit(x[tr],y[tr]);validation[name]=float(average_precision_score(y[va],m.predict_proba(x[va])[:,1]));scores[name]=m.predict_proba(x[te])[:,1]
    selected=max(validation,key=validation.get)
    def logit(p):
        p=np.clip(p,1e-8,1-1e-8);return np.log(p/(1-p)).reshape(-1,1)
    calibrator=LogisticRegression(C=1e6,max_iter=1000).fit(logit(models[selected].predict_proba(x[ca])[:,1]),y[ca])
    scores[selected+'_calibrated']=calibrator.predict_proba(logit(scores[selected]))[:,1]
    scores['amount_rank_reference']=df.loc[te,'Amount'].to_numpy();scores['prevalence_reference']=np.full(te.sum(),y[tr].mean())
    results={};yt=y[te];hours=(t[te]//3600).astype(int)
    for name,s in scores.items():
        budgets=[]
        for k in [5,10,25]:
            chosen=np.concatenate([np.flatnonzero(hours==h)[np.argsort(-s[hours==h],kind='stable')[:k]] for h in np.unique(hours)])
            tp=int(yt[chosen].sum());budgets.append({'budget_per_observed_hour':k,'reviewed':len(chosen),'frauds_found':tp,'precision':tp/len(chosen),'recall':tp/int(yt.sum())})
        results[name]={'average_precision':float(average_precision_score(yt,s)),'roc_auc':float(roc_auc_score(yt,s)),'budgets':budgets}
        if name!='amount_rank_reference':results[name]['brier']=float(brier_score_loss(yt,s))
    blocks=(t[te]//1800).astype(int);unique=np.unique(blocks);by={b:np.flatnonzero(blocks==b) for b in unique};rng=np.random.default_rng(42);boot=[]
    for _ in range(300):
        ix=np.concatenate([by[b] for b in rng.choice(unique,len(unique),replace=True)])
        if len(np.unique(yt[ix]))==2:boot.append(average_precision_score(yt[ix],scores[selected][ix]))
    csv=pd.DataFrame({'time_seconds':t[te],'label':yt,**scores}).to_csv(index=False).encode();(out/'test_predictions.csv.gz').write_bytes(gzip.compress(csv,mtime=0))
    report={'mode':'real_public_retrospective','source':'OpenML 1597, creditcard v1, Worldline/ULB','source_sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'original_rows':original,'duplicates_removed':original-len(df),'split_boundaries_seconds':bounds.tolist(),'splits':{k:{'rows':int(m.sum()),'frauds':int(y[m].sum()),'min_time':float(t[m].min()),'max_time':float(t[m].max())} for k,m in masks.items()},'features':features,'selected_model':selected,'validation_average_precision':validation,'test':results,'selected_AP_block_bootstrap_95_percentile':list(map(float,np.quantile(boot,[.025,.975]))),'valid_bootstrap_replicates':len(boot),'test_prevalence':float(yt.mean()),'elapsed_seconds':time.perf_counter()-start,'platform':platform.platform(),'calibration_note':'Clipping before logit can merge saturated-score ties. AP changes do not establish improved discrimination.','limitations':['Only two historical days','No customer identifiers; no customer-disjoint guarantee','Original PCA fitting provenance unknown','Assumes labels available at fitting; no delayed-feedback validation','Few blocks; descriptive interval only','Separate from live synthetic scoring','No financial savings or production validation claim']}
    (out/'evaluation.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--data',required=True);p.add_argument('--output',default='research_lab/evidence/ulb');a=p.parse_args()
    with threadpool_limits(limits=1):run(a.data,a.output)
