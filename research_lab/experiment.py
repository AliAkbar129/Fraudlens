"""Stylized synthetic-data experiment; not a real payment benchmark."""
import argparse,json,platform,time
from pathlib import Path
import joblib,numpy as np,pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import average_precision_score,roc_auc_score
FEATURES=['log_amount','hour_sin','hour_cos','customer_count','amount_ratio']
def generate(seed=42,days=45,per_day=200):
    rng=np.random.default_rng(seed); rows=[]
    for day in range(days):
        for i in range(per_day):
            customer=int(rng.integers(0,250)); hour=float(rng.uniform(0,24)); fraud=bool(rng.random()<.025)
            amount=float(rng.lognormal(3.4+(.9 if fraud else 0),1.0))
            if fraud and rng.random()<.65: hour=float(rng.uniform(0,5))
            stamp=day*86400+hour*3600
            rows.append({'transaction_id':f'{seed}-{day}-{i}','time_step':stamp,'card_id':str(customer),'amount':round(amount,2),'label':int(fraud),'label_available':stamp+2*86400})
    return pd.DataFrame(rows).sort_values(['time_step','transaction_id']).reset_index(drop=True)
def single_features(amount,stamp,count=0,total=0.):
    hour=(stamp%86400)/3600; mean=total/count if count else 50.
    return np.array([[np.log1p(amount),np.sin(2*np.pi*hour/24),np.cos(2*np.pi*hour/24),np.log1p(count),amount/max(mean,1)]])
def features(frame):
    rows=[]; history={}
    for tx in frame.sort_values(['time_step','transaction_id']).itertuples():
        count,total=history.get(tx.card_id,(0,0.))
        rows.append(single_features(tx.amount,tx.time_step,count,total)[0])
        history[tx.card_id]=(count+1,total+tx.amount)
    return np.array(rows)
def budget_metrics(frame,scores,budget):
    rows=frame.copy(); rows['score']=scores; rows['day']=(rows.time_step//86400).astype(int)
    chosen=rows.sort_values(['score','transaction_id'],ascending=[False,True]).groupby('day',sort=True).head(budget)
    tp=int(chosen.label.sum()); total=int(rows.label.sum())
    return {'budget_per_day':budget,'reviewed':len(chosen),'fraud_found':tp,'precision':tp/len(chosen) if len(chosen) else None,'recall':tp/total if total else None,'false_alerts':int(len(chosen)-tp),'reviewed_fraud_amount':float(chosen.loc[chosen.label.eq(1),'amount'].sum())}
def run(output,seed=42,days=45,per_day=200):
    start=time.perf_counter(); out=Path(output); out.mkdir(parents=True,exist_ok=True)
    df=generate(seed,days,per_day); x=features(df); y=df.label.to_numpy()
    cutoff=int(days*.6)*86400; test_start=int(days*.8)*86400
    tr=(df.time_step<cutoff)&(df.label_available<=cutoff)
    val=(df.time_step>=cutoff)&(df.time_step<test_start)&(df.label_available<=test_start)
    te=df.time_step>=test_start
    models={'logistic':make_pipeline(StandardScaler(),LogisticRegression(max_iter=600,random_state=seed)),
            'gradient_boosting':HistGradientBoostingClassifier(max_iter=80,max_leaf_nodes=15,random_state=seed)}
    validation={}
    for name,m in models.items():
        m.fit(x[tr],y[tr]); validation[name]=float(average_precision_score(y[val],m.predict_proba(x[val])[:,1]))
    selected=max(validation,key=validation.get); tests={}; test=df[te]
    rules=(test.amount>100).astype(float).to_numpy()+(((test.time_step%86400)<5*3600).astype(float).to_numpy()*.5)
    for name,scores in [('rules',rules)]+[(name,m.predict_proba(x[te])[:,1]) for name,m in models.items()]:
        tests[name]={'average_precision':float(average_precision_score(y[te],scores)),'roc_auc':float(roc_auc_score(y[te],scores)),'budgets':[budget_metrics(test,scores,k) for k in [5,10,25]]}
    report={'mode':'synthetic','generator':'Local stylized amount/time simulator v1; not the Fraud Detection Handbook generator',
            'seed':seed,'rows':len(df),'train_rows':int(tr.sum()),'validation_rows':int(val.sum()),'test_rows':int(te.sum()),
            'label_delay_days':2,'train_cutoff_seconds':cutoff,'test_start_seconds':test_start,'selected_model':selected,
            'validation_average_precision':validation,'test_prevalence':float(y[te].mean()),'test':tests,'features':FEATURES,
            'duration_seconds':time.perf_counter()-start,'platform':platform.platform(),
            'limitations':['Synthetic mechanisms favor amount/time patterns','No bank-data validation','No realized financial savings','No drift experiment yet']}
    joblib.dump({'schema_version':1,'model':models[selected],'mode':'synthetic','report':report,'features':FEATURES},out/'model.joblib')
    (out/'evaluation.json').write_text(json.dumps(report,indent=2,allow_nan=False));df.to_csv(out/'transactions.csv',index=False)
    print(json.dumps({'model':selected,'test':tests[selected],'seconds':report['duration_seconds']}));return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',default='research_lab/artifacts');p.add_argument('--seed',type=int,default=42);a=p.parse_args();run(a.output,a.seed)
