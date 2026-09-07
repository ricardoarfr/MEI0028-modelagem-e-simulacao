"""05_eda.py — Etapa 2 do WP1A (§9.2): análise exploratória (entrega A2).
Roda sobre o conjunto de TREINO do manifesto (nunca sobre o teste). Gera figuras e tabelas."""
import os, json, numpy as np, pandas as pd, matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata")
TAB=os.path.join(ROOT,"results","tables"); FIG=os.path.join(ROOT,"results","figures")
man=pd.read_csv(os.path.join(META,"manifesto_divisao.csv")); tr_runs=man[man.conjunto=="treino"]
def load(nome):
    df=pd.read_parquet(os.path.join(PROC,nome+".parquet"))
    return df.merge(tr_runs[["faultNumber","simulationRun"]],on=["faultNumber","simulationRun"])
tr=pd.concat([load("TEP_FaultFree_Training"),load("TEP_Faulty_Training")])
X_cols=[c for c in tr.columns if c not in ("faultNumber","simulationRun","sample")]
print(f"treino: {len(tr):,} linhas, {len(X_cols)} variáveis, {tr.faultNumber.nunique()} classes",flush=True)
# 1. estatísticas descritivas por variável
desc=tr[X_cols].describe().T; desc["cv"]=desc["std"]/desc["mean"].abs()
desc.round(4).to_csv(os.path.join(TAB,"tab_eda_descritivas.csv"))
# 2. distribuição das classes (linhas e runs)
dist=tr.groupby("faultNumber").agg(linhas=("sample","size"),runs=("simulationRun","nunique"))
dist.to_csv(os.path.join(TAB,"tab_eda_distribuicao_classes.csv"))
# 3. correlação
sc=StandardScaler().fit(tr[X_cols]); Z=sc.transform(tr[X_cols])
corr=np.corrcoef(Z,rowvar=False); pd.DataFrame(corr,index=X_cols,columns=X_cols).round(3).to_csv(os.path.join(TAB,"tab_eda_correlacao.csv"))
fig,ax=plt.subplots(figsize=(9,8)); im=ax.imshow(corr,cmap="RdBu_r",vmin=-1,vmax=1)
ax.set_xticks(range(len(X_cols))); ax.set_xticklabels(X_cols,rotation=90,fontsize=5); ax.set_yticks(range(len(X_cols))); ax.set_yticklabels(X_cols,fontsize=5)
plt.colorbar(im,ax=ax,fraction=0.03); ax.set_title("Correlação de Pearson entre as 52 variáveis (treino, padronizado)")
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig_eda_correlacao.png"),dpi=200); plt.close()
# 4. PCA
pca=PCA(n_components=10,random_state=42).fit(Z); ev=pca.explained_variance_ratio_
pd.DataFrame({"componente":range(1,11),"variancia_explicada":ev,"acumulada":np.cumsum(ev)}).round(4).to_csv(os.path.join(TAB,"tab_eda_pca_variancia.csv"),index=False)
# amostra p/ scatter: 2000 pontos por classe
idx=tr.groupby("faultNumber").sample(n=2000,random_state=42).index
P=pca.transform(Z[tr.index.get_indexer(idx)] if False else sc.transform(tr.loc[idx,X_cols]))
fig,ax=plt.subplots(figsize=(9,7)); y=tr.loc[idx,"faultNumber"].to_numpy()
for c in sorted(np.unique(y)):
    m=y==c; ax.scatter(P[m,0],P[m,1],s=2,alpha=0.35,label=f"{c}",color=("black" if c==0 else None))
ax.set_xlabel(f"PC1 ({ev[0]*100:.1f}%)"); ax.set_ylabel(f"PC2 ({ev[1]*100:.1f}%)"); ax.set_title("Projeção PCA das 21 classes (2.000 amostras/classe; 0 = normal em preto)")
ax.legend(markerscale=6,fontsize=6,ncol=3,title="faultNumber"); plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig_eda_pca.png"),dpi=200); plt.close()
# 5. normal vs falha: distância padronizada média por variável, por falha
norm=tr[tr.faultNumber==0][X_cols].mean(); sd=tr[tr.faultNumber==0][X_cols].std()
sep=pd.DataFrame({f: ((tr[tr.faultNumber==f][X_cols].mean()-norm)/sd).abs() for f in range(1,21)}).T
sep.round(3).to_csv(os.path.join(TAB,"tab_eda_separacao_normal_vs_falha.csv"))
fig,ax=plt.subplots(figsize=(10,6)); im=ax.imshow(sep.to_numpy(),aspect="auto",cmap="viridis")
ax.set_yticks(range(20)); ax.set_yticklabels([f"IDV{f}" for f in range(1,21)],fontsize=7); ax.set_xticks(range(len(X_cols))); ax.set_xticklabels(X_cols,rotation=90,fontsize=5)
plt.colorbar(im,ax=ax,label="|média_falha − média_normal| / dp_normal"); ax.set_title("Afastamento de cada falha em relação ao regime normal, por variável")
plt.tight_layout(); plt.savefig(os.path.join(FIG,"fig_eda_separacao.png"),dpi=200); plt.close()
sumario=dict(linhas=int(len(tr)),variaveis=len(X_cols),classes=int(tr.faultNumber.nunique()),
             pca_var_2comp=float(np.cumsum(ev)[1]),pca_var_10comp=float(np.cumsum(ev)[9]),
             pares_corr_abs_maior_0_9=int(((np.abs(corr)>0.9).sum()-len(X_cols))//2),
             falhas_mais_proximas_do_normal=sep.mean(axis=1).nsmallest(5).round(3).to_dict(),
             falhas_mais_distantes_do_normal=sep.mean(axis=1).nlargest(5).round(3).to_dict())
json.dump(sumario,open(os.path.join(META,"eda_sumario.json"),"w"),indent=2)
print(json.dumps(sumario,indent=2)); print("EDA COMPLETA",flush=True)
