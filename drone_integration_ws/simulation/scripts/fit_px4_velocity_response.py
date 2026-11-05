"""Fit effective velocity response from recorded Offboard flight.
First 65% fits coefficients; final 35% selects among delay/model candidates.
This selection segment is not an independent test of the selected model.
"""
from pathlib import Path
import json,numpy as np
from scipy.signal import savgol_filter
root=Path(__file__).resolve().parents[3]
out=root/'sils_sim/results/terminal_drift_20261102'
out.mkdir(exist_ok=True)
p=root/'sils_sim/results/drone_20261102T111202Z_qmxyadtp.jsonl'
a={}
for l in open(p):
 try:r=json.loads(l)
 except:continue
 if not r.get('missing') and r.get('data'):a.setdefault(r['topic'],[]).append((r['received_ns']/1e9,r['data']))
s=a['/fmu/in/trajectory_setpoint'];st=np.array([x[0] for x in s]);u=np.array([x[1]['velocity'][:2] for x in s]);n=a['/navigation/state'];nt=np.array([x[0] for x in n]);v=np.array([[d['twist']['linear'][k] for k in ('x','y')] for _,d in n]);t=np.arange(st[0]+2,min(nt[-1],st[-1]),.05);v=np.column_stack([np.interp(t,nt,v[:,k]) for k in range(2)]);acc=savgol_filter(v,11,2,deriv=1,delta=.05,axis=0);cut=int(len(t)*.65)
rows=[]
for delay in [0,.05,.1,.15,.2]:
 cmd=u[np.clip(np.searchsorted(st,t-delay,side='right')-1,0,len(st)-1)];err=cmd-v
 for integral in [False,True]:
  integ=np.cumsum(err,axis=0)*.05
  X=np.column_stack([err[:cut].ravel()]+([integ[:cut].ravel()] if integral else []));coef=np.linalg.lstsq(X,acc[:cut].ravel(),rcond=None)[0]
  pred=np.zeros_like(v);pred[cut]=v[cut];z=integ[cut].copy()
  for i in range(cut,len(t)-1):
   e=cmd[i]-pred[i];pred[i+1]=pred[i]+.05*(coef[0]*e+(coef[1]*z if integral else 0));z+=.05*e
  rmse=float(np.sqrt(np.mean((pred[cut:]-v[cut:])**2)));rows.append(dict(delay=delay,integral=integral,coef=coef.tolist(),validation_rmse=rmse))
print(json.dumps(rows,indent=2))
np.savez(out/'px4_response_samples.npz',t=t,v=v,st=st,u=u,cut=cut)
open(out/'response_fits.json','w').write(json.dumps(rows,indent=2))
