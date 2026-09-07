"""04b_piloto_vazamento_repeticoes.py — repete o piloto de vazamento (04) em R seleções independentes de execuções.
Em cada repetição: sorteiam-se 25 runs/classe do 'treino' e 25 do 'validacao' do manifesto (semente da repetição);
(A) divisão por execução vs. (B) divisão por amostra com o mesmo volume; reporta a diferença pareada (B−A) por modelo,
com média, desvio-padrão e IC 95% t(df=R−1). Sementes do modelo = semente da repetição."""
import os, json, time, numpy as np, pandas as pd
from scipy import stats
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, balanced_accuracy_score, matthews_corrcoef
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); TAB=os.path.join(ROOT,"results","tables")
SEEDS=[42,123,2024,7,555,11,29,73,101,202]; N_RUNS=25; ONSET_TR=20
man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv"))
FF=pd.read_parquet(os.path.join(PROC,"TEP_FaultFree_Training.parquet")); FT=pd.read_parquet(os.path.join(PROC,"TEP_Faulty_Training.parquet"))
ALL=pd.concat([FF,FT],ignore_index=True); del FF,FT
X_cols=[c for c in ALL.columns if c not in ("faultNumber","simulationRun","sample")]
def metr(y,p): return dict(acuracia=accuracy_score(y,p),acuracia_balanceada=balanced_accuracy_score(y,p),f1_macro=f1_score(y,p,average="macro"),mcc=matthews_corrcoef(y,p))
def pick(conj,seed):
    g=man[man.conjunto==conj]; rng=np.random.RandomState(seed)
    parts=[d.iloc[rng.permutation(len(d))[:N_RUNS]] for _,d in g.groupby("faultNumber")]  # pandas 3: apply omite a coluna de grupo
    return pd.concat(parts)[["faultNumber","simulationRun"]]
rows=[]
for seed in SEEDS:
    tr=ALL.merge(pick("treino",seed),on=["faultNumber","simulationRun"]); va=ALL.merge(pick("validacao",seed),on=["faultNumber","simulationRun"])
    for d in (tr,va): d["y"]=np.where(d["sample"]<=ONSET_TR,0,d["faultNumber"]).astype(np.int32)
    MOD={"DT_leaf50":lambda: DecisionTreeClassifier(random_state=seed,min_samples_leaf=50),
         "DT_leaf1_sem_poda":lambda: DecisionTreeClassifier(random_state=seed,min_samples_leaf=1),
         "RF50_leaf50":lambda: RandomForestClassifier(n_estimators=50,min_samples_leaf=50,random_state=seed,n_jobs=4),
         "RF50_leaf1_sem_poda":lambda: RandomForestClassifier(n_estimators=50,min_samples_leaf=1,random_state=seed,n_jobs=4)}
    sc=StandardScaler().fit(tr[X_cols]); Xtr=sc.transform(tr[X_cols]).astype(np.float32); Xva=sc.transform(va[X_cols]).astype(np.float32)
    todos=pd.concat([tr,va]); frac=len(tr)/len(todos)
    Xa,Xb,ya,yb=train_test_split(todos[X_cols],todos.y,train_size=frac,random_state=seed,shuffle=True,stratify=todos.y)
    sc2=StandardScaler().fit(Xa); Xa=sc2.transform(Xa).astype(np.float32); Xb=sc2.transform(Xb).astype(np.float32)
    for nome,mk in MOD.items():
        t=time.time(); A=metr(va.y,mk().fit(Xtr,tr.y).predict(Xva)); B=metr(yb,mk().fit(Xa,ya).predict(Xb))
        rows.append(dict(seed=seed,modelo=nome,**{f"A_{k}":v for k,v in A.items()},**{f"B_{k}":v for k,v in B.items()},**{f"delta_{k}":B[k]-A[k] for k in A},tempo_s=round(time.time()-t,1)))
        print(f"seed {seed} {nome:<20} A={A['f1_macro']:.4f} B={B['f1_macro']:.4f} Δ={B['f1_macro']-A['f1_macro']:+.4f}",flush=True)
    pd.DataFrame(rows).round(4).to_csv(os.path.join(TAB,"tab_piloto_vazamento_repeticoes.csv"),index=False)
R=pd.DataFrame(rows); out=[]
for nome,g in R.groupby("modelo",sort=False):
    for k in ("f1_macro","mcc","acuracia_balanceada"):
        d=g[f"delta_{k}"].to_numpy(); n=len(d); m=d.mean(); s=d.std(ddof=1); h=stats.t.ppf(0.975,n-1)*s/np.sqrt(n)
        out.append(dict(modelo=nome,metrica=k,R=n,A_media=g[f"A_{k}"].mean(),B_media=g[f"B_{k}"].mean(),delta_media=m,delta_dp=s,ic95_inf=m-h,ic95_sup=m+h,delta_min=d.min(),delta_max=d.max(),p_wilcoxon=float(stats.wilcoxon(d).pvalue)))
pd.DataFrame(out).round(4).to_csv(os.path.join(TAB,"tab_piloto_vazamento_resumo.csv"),index=False); print(pd.DataFrame(out).round(4).to_string()); print("PILOTO REPETIÇÕES COMPLETO",flush=True)
