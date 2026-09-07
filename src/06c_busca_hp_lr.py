"""06c_busca_hp_lr.py — repete a busca de C da regressão logística com max_iter alto (correção: a busca original
parou no teto de 300 iterações sem convergir). Mesmo treino (50 runs/classe) e validação (50 runs/classe) de 06.
Atualiza SÓ a entrada 'regressao_logistica' de configs/hiperparametros_escolhidos.json."""
import os, json, time, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, matthews_corrcoef, balanced_accuracy_score, accuracy_score
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); CFG=os.path.join(ROOT,"configs")
N_TR=int(os.environ.get("HP_N_TREINO",50)); N_VA=50; MAXIT=int(os.environ.get("LR_MAX_ITER",5000)); ONSET_TR=20
man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv"))
tr_runs=man[man.conjunto=="treino"].groupby("faultNumber").head(N_TR); va_runs=man[man.conjunto=="validacao"].groupby("faultNumber").head(N_VA)
def load(nome,runs): return pd.read_parquet(os.path.join(PROC,nome+".parquet")).merge(runs[["faultNumber","simulationRun"]],on=["faultNumber","simulationRun"])
tr=pd.concat([load("TEP_FaultFree_Training",tr_runs),load("TEP_Faulty_Training",tr_runs)]); va=pd.concat([load("TEP_FaultFree_Training",va_runs),load("TEP_Faulty_Training",va_runs)])
X_cols=[c for c in tr.columns if c not in ("faultNumber","simulationRun","sample")]
for d in (tr,va): d["y"]=np.where(d["sample"]<=ONSET_TR,0,d["faultNumber"]).astype(np.int32)
sc=StandardScaler().fit(tr[X_cols]); Xtr=sc.transform(tr[X_cols]).astype(np.float32); ytr=tr.y.to_numpy(); Xva=sc.transform(va[X_cols]).astype(np.float32); yva=va.y.to_numpy()
print(f"treino {len(ytr):,} | validação {len(yva):,} | max_iter={MAXIT}",flush=True)
res=[]
for C in (0.01,0.1,1.0,10.0):
    t=time.time(); m=LogisticRegression(max_iter=MAXIT,C=C).fit(Xtr,ytr); tt=time.time()-t; p=m.predict(Xva)
    r=dict(params=dict(C=C),f1_macro=float(f1_score(yva,p,average="macro")),mcc=float(matthews_corrcoef(yva,p)),acuracia_balanceada=float(balanced_accuracy_score(yva,p)),
           acuracia=float(accuracy_score(yva,p)),tempo_treino_s=round(tt,1),n_iter=int(np.max(m.n_iter_)),max_iter=MAXIT,convergiu=bool(np.max(m.n_iter_)<MAXIT))
    res.append(r); print(json.dumps(r),flush=True)
json.dump(res,open(os.path.join(META,"busca_hp_regressao_logistica_convergida.json"),"w"),indent=1)
best=max(res,key=lambda r:r["f1_macro"]); cfgp=os.path.join(CFG,"hiperparametros_escolhidos.json"); cfg=json.load(open(cfgp))
cfg["regressao_logistica_maxiter300"]=cfg.get("regressao_logistica_maxiter300",cfg["regressao_logistica"]); cfg["regressao_logistica"]=best
json.dump(cfg,open(cfgp,"w"),indent=2); print("MELHOR:",best,"\nBUSCA LR COMPLETA",flush=True)
