"""07_treino_final.py — Etapa 6 do WP1A (§9.6): treino final com configuração CONGELADA e avaliação no teste.
Roda EXCLUSIVAMENTE no Mac (única fonte dos tempos oficiais — objetivo específico 5).
Cada (modelo, semente) executa em subprocesso isolado → pico de memória (ru_maxrss) por modelo.
Treino: 100 runs/classe (manifesto 'treino'). Teste: TODOS os 500 runs/classe do Testing, em lotes.
Sementes {42,123,2024,7,555} (mesmas de Koçak et al., 2026). Runs de treino fixos; varia a semente do modelo."""
import os, sys, json, time, argparse, resource, subprocess, numpy as np, pandas as pd, joblib, warnings; warnings.filterwarnings("ignore")
import pyarrow.parquet as pq
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); CFG=os.path.join(ROOT,"configs")
MOD=os.path.join(ROOT,"models"); PRED=os.path.join(ROOT,"results","predictions"); OUT=os.path.join(META,"treino_final"); os.makedirs(OUT,exist_ok=True)
SEEDS=[42,123,2024,7,555]; MODELOS=["regressao_logistica","arvore_decisao","random_forest","gradient_boosting","xgboost","svm_nystroem"]
NJ=int(os.environ.get("NJOBS",4)); ID=["faultNumber","simulationRun","sample"]
ONSET_TR,ONSET_TE=20,160  # Rieth: falha introduzida em 1 h (Training) e 8 h (Testing); amostras <= onset são fisicamente normais

def build(nome,p,seed):
    from sklearn.linear_model import LogisticRegression; from sklearn.tree import DecisionTreeClassifier
    from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
    sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); from nystroem_sgd import NystroemSGD
    from sklearn.pipeline import make_pipeline; from sklearn.preprocessing import StandardScaler; from xgboost import XGBClassifier
    sc=StandardScaler()
    if nome=="regressao_logistica": m=LogisticRegression(max_iter=int(os.environ.get("LR_MAX_ITER",300)),n_jobs=NJ,**p)
    elif nome=="arvore_decisao":    m=DecisionTreeClassifier(random_state=seed,**p)
    elif nome=="random_forest":     m=RandomForestClassifier(random_state=seed,n_jobs=NJ,**p)
    elif nome=="gradient_boosting": m=HistGradientBoostingClassifier(random_state=seed,early_stopping=False,**p)
    elif nome=="xgboost":           m=XGBClassifier(random_state=seed,tree_method="hist",device="cpu",n_jobs=NJ,subsample=0.8,colsample_bytree=0.8,**p)
    elif nome=="svm_nystroem":      m=NystroemSGD(n_components=p["n_components"],alpha=p["alpha"],epochs=5,random_state=seed,n_jobs=NJ)
    return make_pipeline(sc,m)

def load_treino(runs):
    def one(n): return pd.read_parquet(os.path.join(PROC,n+".parquet")).merge(runs[ID[:2]],on=ID[:2])
    return pd.concat([one("TEP_FaultFree_Training"),one("TEP_Faulty_Training")],ignore_index=True)

def predict_test(pipe,xcols,batch=400_000):
    """Predição em lotes sobre TODO o Testing (10,08 M linhas) — memória constante."""
    ids,preds=[],[]; t_inf=0.0; n=0
    for name in ("TEP_FaultFree_Testing","TEP_Faulty_Testing"):
        pf=pq.ParquetFile(os.path.join(PROC,name+".parquet"))
        for b in pf.iter_batches(batch_size=batch,columns=ID+xcols):
            df=b.to_pandas(); X=df[xcols].to_numpy(dtype=np.float32)
            t=time.perf_counter(); p=pipe.predict(X); t_inf+=time.perf_counter()-t; n+=len(X)
            ids.append(df[ID].to_numpy(dtype=np.int32)); preds.append(p.astype(np.int8))
    return np.vstack(ids),np.concatenate(preds),t_inf,n

def run_one(nome,seed):
    from sklearn.metrics import f1_score,matthews_corrcoef,balanced_accuracy_score,accuracy_score
    hp=json.load(open(os.path.join(CFG,"hiperparametros_escolhidos.json")))[nome]["params"]
    man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv")); tr=load_treino(man[man.conjunto=="treino"])
    xcols=[c for c in tr.columns if c not in ID]; X=tr[xcols].to_numpy(dtype=np.float32)
    y=np.where(tr["sample"]<=ONSET_TR,0,tr.faultNumber).astype(np.int32); del tr  # rótulo físico
    pipe=build(nome,hp,seed); m0=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    t=time.perf_counter(); pipe.fit(X,y); t_fit=time.perf_counter()-t
    pico=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/2**20  # MB (macOS: bytes)
    del X; mp=os.path.join(MOD,f"{nome}_seed{seed}.joblib"); joblib.dump(pipe,mp,compress=3); size=os.path.getsize(mp)
    ids,p,t_inf,n=predict_test(pipe,xcols); y_run=ids[:,0]; yt=np.where(ids[:,2]<=ONSET_TE,0,y_run).astype(np.int8)
    out=pd.DataFrame(ids,columns=ID); out["y_pred"]=p; out.to_parquet(os.path.join(PRED,f"{nome}_seed{seed}.parquet"),index=False)
    r=dict(modelo=nome,seed=seed,params=hp,n_treino=int(len(y)),n_teste=int(n),tempo_treino_s=round(t_fit,2),
           tempo_inferencia_total_s=round(t_inf,2),tempo_inferencia_por_amostra_us=round(1e6*t_inf/n,3),tamanho_modelo_bytes=size,
           pico_memoria_MB=round(pico,1),acuracia=float(accuracy_score(yt,p)),acuracia_balanceada=float(balanced_accuracy_score(yt,p)),
           f1_macro=float(f1_score(yt,p,average="macro")),f1_ponderada=float(f1_score(yt,p,average="weighted")),mcc=float(matthews_corrcoef(yt,p)),
           rotulo_run_acuracia=float(accuracy_score(y_run,p)),rotulo_run_f1_macro=float(f1_score(y_run,p,average="macro")),rotulo_run_mcc=float(matthews_corrcoef(y_run,p)),
           hardware="Apple M3 8GB (4P+4E)",n_jobs=NJ,
           n_iter=(int(np.max(pipe[-1].n_iter_)) if hasattr(pipe[-1],"n_iter_") else None),max_iter=(int(pipe[-1].max_iter) if hasattr(pipe[-1],"max_iter") else None))
    json.dump(r,open(os.path.join(OUT,f"{nome}_seed{seed}.json"),"w"),indent=2); print(json.dumps(r),flush=True)

if __name__=="__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--modelo"); ap.add_argument("--seed",type=int); a=ap.parse_args()
    if a.modelo: run_one(a.modelo,a.seed); sys.exit(0)
    for nome in MODELOS:
        for seed in SEEDS:
            f=os.path.join(OUT,f"{nome}_seed{seed}.json")
            if os.path.exists(f): print(f"skip {nome} seed{seed}",flush=True); continue
            print(f"[{time.strftime('%H:%M')}] {nome} seed{seed} ...",flush=True); t=time.time()
            rc=subprocess.run([sys.executable,"-u",__file__,"--modelo",nome,"--seed",str(seed)],env={**os.environ,"WP1A_ROOT":ROOT}).returncode
            print(f"   rc={rc} em {(time.time()-t)/60:.1f} min",flush=True)
    print("TREINO FINAL COMPLETO",flush=True)
