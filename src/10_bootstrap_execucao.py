"""10_bootstrap_execucao.py — incerteza de generalização para novas execuções: bootstrap pareado, estratificado por classe,
sobre as 10.500 execuções do teste (500/classe), a partir das predições salvas (5 sementes somadas por execução).
Para cada reamostra (mesmos índices de execução para todos os modelos) recalcula F1 macro e MCC da matriz de confusão
agregada; reporta IC 95% percentil por modelo e das diferenças entre pares. B=2000."""
import os, glob, json, itertools, numpy as np, pandas as pd
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PRED=os.path.join(ROOT,"results","predictions"); TAB=os.path.join(ROOT,"results","tables"); META=os.path.join(ROOT,"results","metadata")
MODELOS=["regressao_logistica","arvore_decisao","random_forest","gradient_boosting","xgboost","svm_nystroem"]
NOME={"regressao_logistica":"Regressão Logística","arvore_decisao":"Árvore de Decisão","random_forest":"Random Forest","gradient_boosting":"Gradient Boosting","xgboost":"XGBoost","svm_nystroem":"SVM (Nyström)"}
K=21; ONSET_TE=160; B=int(os.environ.get("BOOT_B",2000)); rng=np.random.RandomState(42)
CM={}; run_class=None
for m in MODELOS:
    acc=None
    for f in sorted(glob.glob(os.path.join(PRED,f"{m}_seed*.parquet"))):
        d=pd.read_parquet(f); yt=np.where(d["sample"].to_numpy()<=ONSET_TE,0,d.faultNumber.to_numpy()).astype(np.int64); yp=d.y_pred.to_numpy().astype(np.int64)
        rid=(d.faultNumber.to_numpy().astype(np.int64)*1000+d.simulationRun.to_numpy().astype(np.int64))
        if run_class is None:
            uniq=np.unique(rid); run_class=uniq//1000; pos={r:i for i,r in enumerate(uniq)}
        ridx=np.searchsorted(uniq,rid)
        c=np.bincount(ridx*K*K+yt*K+yp,minlength=len(uniq)*K*K).reshape(len(uniq),K,K)
        acc=c if acc is None else acc+c
    CM[m]=acc; print(m,"execuções",acc.shape[0],"amostras×sementes",int(acc.sum()),flush=True)
def f1_mcc(cm):
    cm=cm.astype(np.float64); tp=np.diag(cm); fp=cm.sum(0)-tp; fn=cm.sum(1)-tp
    f1=np.where(2*tp+fp+fn>0,2*tp/np.maximum(2*tp+fp+fn,1),0.0); n=cm.sum(); c=tp.sum(); t=cm.sum(1); p=cm.sum(0)
    mcc=(c*n-(t*p).sum())/np.sqrt(max((n*n-(p*p).sum())*(n*n-(t*t).sum()),1e-12))
    return f1.mean(),mcc
byc=[np.where(run_class==k)[0] for k in range(K)]
point={m:f1_mcc(CM[m].sum(0)) for m in MODELOS}
boots={m:np.zeros((B,2)) for m in MODELOS}
for b in range(B):
    idx=np.concatenate([g[rng.randint(0,len(g),len(g))] for g in byc])
    for m in MODELOS: boots[m][b]=f1_mcc(CM[m][idx].sum(0))
    if b%500==0: print("bootstrap",b,flush=True)
rows=[]
for m in MODELOS:
    for j,met in enumerate(("f1_macro","mcc")):
        lo,hi=np.percentile(boots[m][:,j],[2.5,97.5]); rows.append(dict(modelo=NOME[m],metrica=met,estimativa=point[m][j],ic95_inf=lo,ic95_sup=hi,largura=hi-lo))
pd.DataFrame(rows).round(4).to_csv(os.path.join(TAB,"tab10_bootstrap_execucao.csv"),index=False)
pairs=[]
for a,bm in itertools.combinations(MODELOS,2):
    for j,met in enumerate(("f1_macro","mcc")):
        d=boots[a][:,j]-boots[bm][:,j]; lo,hi=np.percentile(d,[2.5,97.5]); pairs.append(dict(metrica=met,comparacao=f"{NOME[a]} vs {NOME[bm]}",diferenca=point[a][j]-point[bm][j],ic95_inf=lo,ic95_sup=hi,exclui_zero=bool(lo>0 or hi<0)))
pd.DataFrame(pairs).round(4).to_csv(os.path.join(TAB,"tab10b_bootstrap_pares.csv"),index=False)
json.dump(dict(B=B,n_execucoes=int(len(run_class)),estratificado_por_classe=True,sementes_somadas=True),open(os.path.join(META,"bootstrap_execucao.json"),"w"),indent=2)
print(pd.DataFrame(rows).round(4).to_string()); print(pd.DataFrame(pairs).round(4).to_string()); print("BOOTSTRAP COMPLETO",flush=True)
