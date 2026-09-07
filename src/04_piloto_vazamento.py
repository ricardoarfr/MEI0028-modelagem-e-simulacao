"""04_piloto_vazamento.py — Etapa 5 do plano: piloto com 25 runs/classe + experimento do vazamento.
Treina Árvore de Decisão duas vezes com o MESMO volume de dados:
  (A) divisão por run   — protocolo do WP1A
  (B) divisão aleatória por amostra — prática dominante na literatura (embaralha e sorteia linhas)
A diferença (B − A) é a medida direta do vazamento nos nossos dados."""
import os, json, time, numpy as np, pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, matthews_corrcoef
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); TAB=os.path.join(ROOT,"results","tables")
SEED=42; N_RUNS=25
man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv"))
tr_runs=man[man.conjunto=="treino"].groupby("faultNumber").head(N_RUNS)
va_runs=man[man.conjunto=="validacao"].groupby("faultNumber").head(N_RUNS)
def load(nome,runs):
    df=pd.read_parquet(os.path.join(PROC,nome+".parquet"))
    return df.merge(runs[["faultNumber","simulationRun"]],on=["faultNumber","simulationRun"])
tr=pd.concat([load("TEP_FaultFree_Training",tr_runs),load("TEP_Faulty_Training",tr_runs)])
va=pd.concat([load("TEP_FaultFree_Training",va_runs),load("TEP_Faulty_Training",va_runs)])
X_cols=[c for c in tr.columns if c not in ("faultNumber","simulationRun","sample")]
ONSET_TR=20
for d in (tr,va): d["y"]=np.where(d["sample"]<=ONSET_TR,0,d["faultNumber"]).astype(np.int32)
print(f"treino {len(tr):,} linhas | validação {len(va):,} linhas | {len(X_cols)} variáveis",flush=True)
def metr(y,p): return dict(acuracia=accuracy_score(y,p),acuracia_balanceada=balanced_accuracy_score(y,p),
                           f1_macro=f1_score(y,p,average="macro"),mcc=matthews_corrcoef(y,p))
res={}
MODELOS={"DT_leaf50":lambda: DecisionTreeClassifier(random_state=SEED,min_samples_leaf=50),
         "DT_leaf1_sem_poda":lambda: DecisionTreeClassifier(random_state=SEED,min_samples_leaf=1),
         "RF50_leaf50":lambda: RandomForestClassifier(n_estimators=50,min_samples_leaf=50,random_state=SEED,n_jobs=4),
         "RF50_leaf1_sem_poda":lambda: RandomForestClassifier(n_estimators=50,min_samples_leaf=1,random_state=SEED,n_jobs=4)}
sc=StandardScaler().fit(tr[X_cols]); Xtr_s=sc.transform(tr[X_cols]); Xva_s=sc.transform(va[X_cols])
todos=pd.concat([tr,va]); frac=len(tr)/len(todos)
Xa,Xb,ya,yb=train_test_split(todos[X_cols],todos.y,train_size=frac,random_state=SEED,shuffle=True,stratify=todos.y)
sc2=StandardScaler().fit(Xa); Xa_s=sc2.transform(Xa); Xb_s=sc2.transform(Xb)
for nome,mk in MODELOS.items():
    t=time.time(); m=mk().fit(Xtr_s,tr.y); A=metr(va.y,m.predict(Xva_s)); A["tempo_s"]=time.time()-t
    t=time.time(); m2=mk().fit(Xa_s,ya); B=metr(yb,m2.predict(Xb_s)); B["tempo_s"]=time.time()-t
    res[nome]=dict(A_por_run=A,B_por_amostra=B,diferenca_B_menos_A={k:B[k]-A[k] for k in ("acuracia","acuracia_balanceada","f1_macro","mcc")})
    print(nome,"por_run F1m=%.4f  por_amostra F1m=%.4f  Δ=%.4f"%(A["f1_macro"],B["f1_macro"],B["f1_macro"]-A["f1_macro"]),flush=True)
res["config"]=dict(runs_por_classe=N_RUNS,linhas_treino=int(len(tr)),linhas_validacao=int(len(va)),seed=SEED,rotulo="fisico (sample<=20 → normal)")
json.dump(res,open(os.path.join(META,"piloto_vazamento.json"),"w"),indent=2)
rows=[dict(modelo=n,condicao=c,**res[n][c]) for n in MODELOS for c in ("A_por_run","B_por_amostra")]+[dict(modelo=n,condicao="diferenca_B_menos_A",**res[n]["diferenca_B_menos_A"]) for n in MODELOS]
pd.DataFrame(rows).round(4).to_csv(os.path.join(TAB,"tab_piloto_vazamento.csv"),index=False)
print(json.dumps(res,indent=2)); print("PILOTO COMPLETO",flush=True)
