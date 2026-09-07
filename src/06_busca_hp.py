"""06_busca_hp.py — Etapa 5 do WP1A (§9.5): seleção de hiperparâmetros SÓ na validação.
Treino: 50 runs/classe (subconjunto do 'treino' do manifesto) · Validação: 50 runs/classe.
Critério de seleção: F1 macro na validação. O TESTE NÃO É TOCADO.
Grade fatorial reduzida (4 a 12 configurações por modelo), avaliada só na validação.
Roda local ou no Colab (WP1A_ROOT aponta para a raiz do projeto)."""
import os, sys, json, time, itertools, numpy as np, pandas as pd, warnings; warnings.filterwarnings("ignore")
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
import sys; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.path.join(os.environ.get("WP1A_ROOT","."),"src"))
from nystroem_sgd import NystroemSGD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score, matthews_corrcoef, balanced_accuracy_score, accuracy_score
from xgboost import XGBClassifier
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); CFG=os.path.join(ROOT,"configs")
SEED=42; N_TR=int(os.environ.get("HP_N_TREINO",50)); N_VA=50
SOMENTE=os.environ.get("HP_MODELOS")  # ex.: "xgboost,svm" para rodar só alguns
try:
    import subprocess; GPU=subprocess.run(["nvidia-smi","-L"],capture_output=True,text=True).returncode==0
except Exception: GPU=False
print(f"ROOT={ROOT} GPU={GPU} treino={N_TR} runs/classe",flush=True)
man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv"))
tr_runs=man[man.conjunto=="treino"].groupby("faultNumber").head(N_TR); va_runs=man[man.conjunto=="validacao"].groupby("faultNumber").head(N_VA)
def load(nome,runs):
    return pd.read_parquet(os.path.join(PROC,nome+".parquet")).merge(runs[["faultNumber","simulationRun"]],on=["faultNumber","simulationRun"])
tr=pd.concat([load("TEP_FaultFree_Training",tr_runs),load("TEP_Faulty_Training",tr_runs)])
va=pd.concat([load("TEP_FaultFree_Training",va_runs),load("TEP_Faulty_Training",va_runs)])
X_cols=[c for c in tr.columns if c not in ("faultNumber","simulationRun","sample")]
ONSET_TR=20  # Rieth: falha introduzida 1 h (=20 amostras de 3 min) após o início nos runs de Training → sample<=20 é fisicamente normal
for d in (tr,va): d["y"]=np.where(d["sample"]<=ONSET_TR,0,d["faultNumber"]).astype(np.int32)
sc=StandardScaler().fit(tr[X_cols])  # ajustado SÓ no treino (§9.4)
Xtr=sc.transform(tr[X_cols]).astype(np.float32); ytr=tr.y.to_numpy(); Xva=sc.transform(va[X_cols]).astype(np.float32); yva=va.y.to_numpy()
print(f"treino {len(ytr):,} | validação {len(yva):,} | {len(X_cols)} vars",flush=True)
NJ=int(os.environ.get("NJOBS",4))
GRADES={
 "regressao_logistica": (lambda p: LogisticRegression(max_iter=300,n_jobs=NJ,**p),
    [dict(C=c) for c in (0.01,0.1,1.0,10.0)]),
 "arvore_decisao": (lambda p: DecisionTreeClassifier(random_state=SEED,**p),
    [dict(min_samples_leaf=l,max_depth=d) for l in (20,50,100,200) for d in (None,20)]),
 "random_forest": (lambda p: RandomForestClassifier(random_state=SEED,n_jobs=NJ,**p),
    [dict(n_estimators=n,min_samples_leaf=l,max_features=f) for n in (100,200) for l in (20,50,100) for f in ("sqrt",0.3)]),
 "gradient_boosting": (lambda p: HistGradientBoostingClassifier(random_state=SEED,early_stopping=False,**p),
    [dict(learning_rate=lr,max_iter=it,max_leaf_nodes=ln) for lr in (0.05,0.1) for it in (200,400) for ln in (31,63)]),
 "xgboost": (lambda p: XGBClassifier(random_state=SEED,tree_method="hist",device=("cuda" if GPU else "cpu"),n_jobs=NJ,subsample=0.8,colsample_bytree=0.8,**p),
    [dict(n_estimators=n,max_depth=d,learning_rate=lr) for n in (300,500) for d in (4,6) for lr in (0.05,0.1)]),
 "svm_nystroem": (lambda p: NystroemSGD(n_components=p["n_components"],alpha=p["alpha"],epochs=5,random_state=SEED,n_jobs=NJ),
    [dict(n_components=nc,alpha=a) for nc in (200,500,1000) for a in (1e-5,1e-4)]),
}
if SOMENTE: GRADES={k:v for k,v in GRADES.items() if k in SOMENTE.split(",")}
out_path=os.path.join(META,"busca_hp_resultados.json"); res=json.load(open(out_path)) if os.path.exists(out_path) else {}
for nome,(build,grade) in GRADES.items():
    res.setdefault(nome,[]); feitos={json.dumps(r["params"],sort_keys=True) for r in res[nome]}
    for params in grade:
        k=json.dumps(params,sort_keys=True)
        if k in feitos: continue
        t=time.time(); m=build(params); m.fit(Xtr,ytr); tt=time.time()-t; p=m.predict(Xva)
        r=dict(params=params,f1_macro=float(f1_score(yva,p,average="macro")),mcc=float(matthews_corrcoef(yva,p)),
               acuracia_balanceada=float(balanced_accuracy_score(yva,p)),acuracia=float(accuracy_score(yva,p)),tempo_treino_s=round(tt,1))
        res[nome].append(r); json.dump(res,open(out_path,"w"),indent=1)
        print(f"{nome:<22} {k:<70} F1m={r['f1_macro']:.4f} MCC={r['mcc']:.4f} {tt:6.0f}s",flush=True)
best={n:max(v,key=lambda r:r["f1_macro"]) for n,v in res.items() if v}
json.dump(best,open(os.path.join(CFG,"hiperparametros_escolhidos.json"),"w"),indent=2)
print("\nMELHORES (F1 macro na validação):"); [print(f"  {n:<22} {b['f1_macro']:.4f}  {b['params']}") for n,b in best.items()]
print("BUSCA HP COMPLETA",flush=True)
