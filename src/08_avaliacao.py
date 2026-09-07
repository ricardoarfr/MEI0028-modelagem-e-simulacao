"""08_avaliacao.py — Etapa 6 (§9.6), Métricas (§10), Análise estatística (§11) e Insumos (§12) do WP1A.
Lê results/metadata/treino_final/*.json e results/predictions/*.parquet; gera tabelas (CSV) e figuras (PNG).
Rótulo PRIMÁRIO no teste = físico (sample<=160 → normal); secundário = rótulo do run (comparabilidade)."""
import os, glob, json, itertools, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy import stats
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support, f1_score, matthews_corrcoef
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
META=os.path.join(ROOT,"results","metadata"); PRED=os.path.join(ROOT,"results","predictions"); TAB=os.path.join(ROOT,"results","tables"); FIG=os.path.join(ROOT,"results","figures"); CFG=os.path.join(ROOT,"configs")
ONSET_TE=160; CL=list(range(21)); NOME={"regressao_logistica":"Regressão Logística","arvore_decisao":"Árvore de Decisão","random_forest":"Random Forest","gradient_boosting":"Gradient Boosting","xgboost":"XGBoost","svm_nystroem":"SVM (Nyström)"}
ORD=list(NOME); SEEDS=[42,123,2024,7,555]
runs=[json.load(open(f)) for f in sorted(glob.glob(os.path.join(META,"treino_final","*.json")))]
R=pd.DataFrame(runs); R["modelo_nome"]=R.modelo.map(NOME); R.to_csv(os.path.join(TAB,"tab03b_metricas_por_seed.csv"),index=False)
modelos=[m for m in ORD if m in set(R.modelo)]; print("modelos com resultados:",modelos,"| execuções:",len(R),flush=True)
tq=stats.t.ppf(0.975,df=4)
def agg(col): 
    g=R.groupby("modelo")[col]; return pd.DataFrame({"media":g.mean(),"dp":g.std(ddof=1),"ic95":tq*g.std(ddof=1)/np.sqrt(g.count()),"n":g.count()}).reindex(modelos)
# ---- Tab 2: hiperparâmetros
hp=json.load(open(os.path.join(CFG,"hiperparametros_escolhidos.json")))
pd.DataFrame([dict(Modelo=NOME[m],Hiperparametros=json.dumps(hp[m]["params"]),F1_macro_validacao=round(hp[m]["f1_macro"],4)) for m in modelos]).to_csv(os.path.join(TAB,"tab02_hiperparametros.csv"),index=False)
# ---- Tab 3: métricas globais (média ± dp, IC95) e Tab 5: custo
MET=["acuracia","acuracia_balanceada","f1_macro","f1_ponderada","mcc"]
CUSTO=["tempo_treino_s","tempo_inferencia_total_s","tempo_inferencia_por_amostra_us","tamanho_modelo_bytes","pico_memoria_MB"]
t3=pd.concat({c:agg(c) for c in MET},axis=1); t3.index=[NOME[m] for m in t3.index]; t3.round(4).to_csv(os.path.join(TAB,"tab03_metricas_globais.csv"))
t5=pd.concat({c:agg(c) for c in CUSTO},axis=1); t5.index=[NOME[m] for m in t5.index]; t5.round(3).to_csv(os.path.join(TAB,"tab05_custo_computacional.csv"))
# ---- por classe, matrizes de confusão, run-level (lê predições)
pc_rows=[]; cms={m:np.zeros((21,21),dtype=np.int64) for m in modelos}; rl_rows=[]
for m in modelos:
    for s in SEEDS:
        f=os.path.join(PRED,f"{m}_seed{s}.parquet")
        if not os.path.exists(f): continue
        d=pd.read_parquet(f); yt=np.where(d["sample"]<=ONSET_TE,0,d.faultNumber).astype(np.int8); yp=d.y_pred.to_numpy()
        p,r,f1,sup=precision_recall_fscore_support(yt,yp,labels=CL,zero_division=0)
        for c in CL: pc_rows.append(dict(modelo=m,seed=s,classe=c,precisao=p[c],revocacao=r[c],f1=f1[c],suporte=int(sup[c])))
        cms[m]+=confusion_matrix(yt,yp,labels=CL)
        # run-level: voto majoritário por (faultNumber, simulationRun); rótulo do run
        cnt=d.groupby(["faultNumber","simulationRun","y_pred"]).size().reset_index(name="n")
        vote=cnt.sort_values("n",ascending=False).drop_duplicates(["faultNumber","simulationRun"])
        y_run=d.faultNumber.to_numpy()
        rl_rows.append(dict(modelo=m,seed=s,run_level_f1_macro=f1_score(vote.faultNumber,vote.y_pred,average="macro"),run_level_acuracia=(vote.faultNumber==vote.y_pred).mean(),run_level_mcc=matthews_corrcoef(vote.faultNumber,vote.y_pred),n_runs=len(vote),
                            rotulo_run_acuracia=float((y_run==yp).mean()),rotulo_run_f1_macro=float(f1_score(y_run,yp,average="macro")),rotulo_run_mcc=float(matthews_corrcoef(y_run,yp))))
        del d; print(f"  {m} seed{s} ok",flush=True)
PC=pd.DataFrame(pc_rows); t4=PC.groupby(["modelo","classe"])[["precisao","revocacao","f1"]].mean().reset_index(); t4["modelo"]=t4.modelo.map(NOME)
t4.round(4).to_csv(os.path.join(TAB,"tab04_metricas_por_classe.csv"),index=False)
RL=pd.DataFrame(rl_rows); RL.to_csv(os.path.join(TAB,"tab08b_run_level_por_seed.csv"),index=False)
t8=RL.groupby("modelo")[["run_level_f1_macro","run_level_acuracia","run_level_mcc","rotulo_run_acuracia","rotulo_run_f1_macro","rotulo_run_mcc"]].agg(["mean","std"]).reindex(modelos); t8.index=[NOME[m] for m in t8.index]; t8.round(4).to_csv(os.path.join(TAB,"tab08_run_level.csv"))
# anexa as métricas com rótulo do run à Tabela 3 (média±dp) — calculadas das predições
for c in ["rotulo_run_acuracia","rotulo_run_f1_macro","rotulo_run_mcc"]:
    g=RL.groupby("modelo")[c]; t3x=pd.DataFrame({"media":g.mean(),"dp":g.std(ddof=1)}).reindex(modelos); t3x.index=[NOME[m] for m in t3x.index]
    for k in ("media","dp"): t3[(c,k)]=t3x[k]
t3.round(4).to_csv(os.path.join(TAB,"tab03_metricas_globais.csv"))
# ---- Tab 6: falhas mais confundidas (pares verdadeiro→predito, fora da diagonal, normalizado por linha)
conf=[]
for m in modelos:
    cm=cms[m]; cmn=cm/np.maximum(cm.sum(1,keepdims=True),1)
    for i in CL:
        for j in CL:
            if i!=j and cm[i,j]>0: conf.append(dict(modelo=NOME[m],verdadeira=i,predita=j,fracao_da_classe=cmn[i,j],n=int(cm[i,j])))
    pd.DataFrame(cmn,index=CL,columns=CL).round(4).to_csv(os.path.join(TAB,f"tab_matriz_confusao_{m}.csv"))
CF=pd.DataFrame(conf).sort_values(["modelo","fracao_da_classe"],ascending=[True,False]); CF.groupby("modelo").head(10).round(4).to_csv(os.path.join(TAB,"tab06_falhas_confundidas.csv"),index=False)
# falhas mais difíceis: F1 médio por classe entre modelos
dif=t4.groupby("classe").f1.mean().sort_values(); dif.round(4).to_csv(os.path.join(TAB,"tab06b_dificuldade_por_classe.csv"))
# ---- Tab 7: estatística (§11) — Friedman + Wilcoxon pareado com Holm, sobre seeds
def holm(pvals):
    n=len(pvals); order=np.argsort(pvals); adj=np.empty(n)
    for rank,i in enumerate(order): adj[i]=min(1.0,pvals[i]*(n-rank))
    for k in range(1,n): adj[order[k]]=max(adj[order[k]],adj[order[k-1]])
    return adj
st=[]
for met in ["f1_macro","mcc"]:
    piv=R.pivot(index="seed",columns="modelo",values=met)[modelos].dropna()
    if len(piv)>=2 and piv.shape[1]>=3:
        fr=stats.friedmanchisquare(*[piv[m] for m in modelos]); st.append(dict(metrica=met,teste="Friedman",comparacao="todos",estatistica=fr.statistic,p=fr.pvalue,p_holm=None))
        pares=list(itertools.combinations(modelos,2)); ps=[]
        for a,b in pares:
            try: w=stats.wilcoxon(piv[a],piv[b]); ps.append(w.pvalue)
            except ValueError: ps.append(1.0)
        ph=holm(np.array(ps))
        for (a,b),p,q in zip(pares,ps,ph): st.append(dict(metrica=met,teste="Wilcoxon",comparacao=f"{NOME[a]} vs {NOME[b]}",estatistica=float(piv[a].mean()-piv[b].mean()),p=p,p_holm=q))
    piv.to_csv(os.path.join(TAB,f"tab07b_{met}_por_seed_pivot.csv"))
pd.DataFrame(st).round(5).to_csv(os.path.join(TAB,"tab07_estatistica.csv"),index=False)
# ---- Tab 9: resumo da busca de hp + trade-off do Nyström
bh=json.load(open(os.path.join(META,"busca_hp_resultados_MERGED.json") if os.path.exists(os.path.join(META,"busca_hp_resultados_MERGED.json")) else os.path.join(META,"busca_hp_resultados.json")))
pd.DataFrame([dict(Modelo=NOME.get(m,m),configs_testadas=len(v),melhor_f1_macro_val=max(r["f1_macro"] for r in v),pior_f1_macro_val=min(r["f1_macro"] for r in v)) for m,v in bh.items()]).round(4).to_csv(os.path.join(TAB,"tab09_busca_hp_resumo.csv"),index=False)
if "svm_nystroem" in bh:
    ny=pd.DataFrame([dict(**r["params"],f1_macro=r["f1_macro"],mcc=r["mcc"],tempo_s=r["tempo_treino_s"]) for r in bh["svm_nystroem"]]); ny.to_csv(os.path.join(TAB,"tab09b_nystroem_tradeoff.csv"),index=False)
    fig,ax=plt.subplots(figsize=(7,4)); ax2=ax.twinx()
    for A,g in ny.groupby("alpha"): g=g.sort_values("n_components"); ax.plot(g.n_components,g.f1_macro,"o-",label=f"F1 macro (alpha={A:g})"); ax2.plot(g.n_components,g.tempo_s/60,"s--",alpha=.6,label=f"tempo (alpha={A:g})")
    ax.set_xlabel("n_components (D) do Nyström"); ax.set_ylabel("F1 macro (validação)"); ax2.set_ylabel("tempo de treino (min)"); ax.set_title("SVM via Nyström: qualidade × custo em função de D"); ax.legend(loc="upper left",fontsize=8); ax2.legend(loc="lower right",fontsize=8)
    plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig06_svm_nystroem_tradeoff.png"),dpi=200); plt.close()
# ---- Fig 1: F1 macro e MCC com IC95
lab=[NOME[m] for m in modelos]; x=np.arange(len(modelos)); fig,ax=plt.subplots(figsize=(9,4.5))
for k,(col,off,cor) in enumerate([("f1_macro",-0.2,"#1f77b4"),("mcc",0.2,"#ff7f0e")]):
    a=agg(col); ax.bar(x+off,a.media,0.38,yerr=a.ic95,capsize=3,label={"f1_macro":"F1 macro","mcc":"MCC"}[col],color=cor)
    for xi,v in zip(x+off,a.media): ax.text(xi,v+0.01,f"{v:.3f}",ha="center",fontsize=7)
ax.set_xticks(x); ax.set_xticklabels(lab,rotation=15); ax.set_ylim(0,1.05); ax.set_ylabel("valor no teste (rótulo físico)"); ax.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig01_f1_mcc_comparativo.png"),dpi=200); plt.close()
# ---- Fig 2: custo computacional (3 painéis, escala log)
fig,axs=plt.subplots(1,3,figsize=(13,4))
for ax,(col,tit,esc) in zip(axs,[("tempo_treino_s","Tempo de treino (s)",1),("tempo_inferencia_por_amostra_us","Inferência por amostra (µs)",1),("tamanho_modelo_bytes","Tamanho do modelo (MB)",1/2**20)]):
    a=agg(col); ax.bar(x,a.media*esc,yerr=a.ic95*esc,capsize=3,color="#2ca02c"); ax.set_yscale("log"); ax.set_xticks(x); ax.set_xticklabels(lab,rotation=30,fontsize=8); ax.set_title(tit)
    for xi,v in zip(x,a.media*esc): ax.text(xi,v*1.15,f"{v:.3g}",ha="center",fontsize=7)
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig02_custo_computacional.png"),dpi=200); plt.close()
# ---- Fig 3: matrizes de confusão normalizadas (agregadas nas 5 sementes) — uma por modelo
for m in modelos:
    cmn=cms[m]/np.maximum(cms[m].sum(1,keepdims=True),1); fig,ax=plt.subplots(figsize=(7.5,6.5)); im=ax.imshow(cmn,cmap="Blues",vmin=0,vmax=1)
    ax.set_xticks(CL); ax.set_yticks(CL); ax.set_xlabel("classe predita"); ax.set_ylabel("classe verdadeira (rótulo físico)"); 
    for i in CL:
        for j in CL:
            if cmn[i,j]>=0.05: ax.text(j,i,f"{cmn[i,j]:.2f}",ha="center",va="center",fontsize=5,color="white" if cmn[i,j]>0.5 else "black")
    plt.colorbar(im,ax=ax,fraction=0.04); plt.tight_layout(); plt.savefig(os.path.join(FIG,f"fig03_matriz_confusao_{m}.png"),dpi=200); plt.close()
# ---- Fig 4: heatmap F1 por classe (modelos × classes)
H=t4.pivot(index="modelo",columns="classe",values="f1").reindex(lab); fig,ax=plt.subplots(figsize=(12,3.8)); im=ax.imshow(H.to_numpy(),cmap="viridis",vmin=0,vmax=1,aspect="auto")
ax.set_xticks(CL); ax.set_yticks(range(len(lab))); ax.set_yticklabels(lab,fontsize=8); ax.set_xlabel("classe (0 = normal; 1–20 = IDV)"); 
for i in range(len(lab)):
    for j in CL: ax.text(j,i,f"{H.iloc[i,j]:.2f}",ha="center",va="center",fontsize=5.5,color="white" if H.iloc[i,j]<0.5 else "black")
plt.colorbar(im,ax=ax,fraction=0.02); plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig04_f1_por_classe_heatmap.png"),dpi=200); plt.close()
# ---- Fig 5: trade-off F1 macro × tempo de inferência
a1=agg("f1_macro"); a2=agg("tempo_inferencia_por_amostra_us"); fig,ax=plt.subplots(figsize=(7,4.5))
for m in modelos: ax.scatter(a2.loc[m,"media"],a1.loc[m,"media"],s=80); ax.annotate(NOME[m],(a2.loc[m,"media"],a1.loc[m,"media"]),textcoords="offset points",xytext=(6,4),fontsize=8)
ax.set_xscale("log"); ax.set_xlabel("tempo de inferência por amostra (µs, escala log)"); ax.set_ylabel("F1 macro (teste)"); plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig05_tradeoff_f1_vs_inferencia.png"),dpi=200); plt.close()
# ---- Fig 7: experimento do vazamento (piloto estendido: 4 variantes × 2 condições)
pv=os.path.join(META,"piloto_vazamento.json")
if os.path.exists(pv):
    v=json.load(open(pv)); vars_=[k for k in v if k!="config"]; lab7={"DT_leaf50":"Árvore (folha≥50)","DT_leaf1_sem_poda":"Árvore sem poda","RF50_leaf50":"RF-50 (folha≥50)","RF50_leaf1_sem_poda":"RF-50 sem poda"}
    fig,axs=plt.subplots(1,2,figsize=(11,4)); xx=np.arange(len(vars_))
    for ax,met,tit in zip(axs,["f1_macro","mcc"],["F1 macro","MCC"]):
        A=[v[k]["A_por_run"][met] for k in vars_]; B=[v[k]["B_por_amostra"][met] for k in vars_]
        ax.bar(xx-0.2,A,0.4,label="divisão por execução (protocolo)"); ax.bar(xx+0.2,B,0.4,label="divisão aleatória por amostra")
        for i in range(len(vars_)): ax.text(i,max(A[i],B[i])+0.015,f"Δ=+{B[i]-A[i]:.3f}",ha="center",fontsize=8)
        ax.set_xticks(xx); ax.set_xticklabels([lab7.get(k,k) for k in vars_],fontsize=8,rotation=10); ax.set_ylim(0.6,0.9); ax.set_title(tit)
    axs[0].legend(fontsize=8,loc="lower right"); fig.suptitle("Efeito da unidade de divisão (piloto, 25 execuções/classe): cresce com a capacidade do modelo"); plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig07_vazamento.png"),dpi=200); plt.close()
# ---- metadados do ambiente (§12 item 10)
import platform, sklearn, xgboost, scipy, subprocess
json.dump(dict(python=platform.python_version(),plataforma=platform.platform(),hardware="Apple M3, 8 núcleos (4P+4E), 8 GB RAM",numpy=np.__version__,pandas=pd.__version__,scikit_learn=sklearn.__version__,xgboost=xgboost.__version__,scipy=scipy.__version__,
               sementes=SEEDS,n_jobs=int(os.environ.get("NJOBS",4)),colab_hp="Google Colab T4 (busca de hiperparâmetros apenas; tempos não usados)"),open(os.path.join(META,"ambiente.json"),"w"),indent=2)
print("AVALIACAO COMPLETA",flush=True)
