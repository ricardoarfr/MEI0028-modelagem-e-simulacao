"""02_auditoria.py — Etapa 1 do WP1A (§9.1): auditoria da base A PARTIR DOS PARQUETS, em lotes (memória constante)."""
import os, json, numpy as np, pandas as pd, pyarrow.parquet as pq, pyarrow.compute as pc
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
RAW=os.path.join(ROOT,"data","raw"); PROC=os.path.join(ROOT,"data","processed")
TAB=os.path.join(ROOT,"results","tables"); META=os.path.join(ROOT,"results","metadata"); REP=os.path.join(ROOT,"reports")
FILES=["TEP_FaultFree_Training","TEP_FaultFree_Testing","TEP_Faulty_Training","TEP_Faulty_Testing"]; ID=["faultNumber","simulationRun","sample"]
aud={}; rows=[]
for name in FILES:
    pf=pq.ParquetFile(os.path.join(PROC,name+".parquet")); cols=pf.schema_arrow.names; xcols=[c for c in cols if c not in ID]
    nulos=0; infs=0; ids=[]
    for b in pf.iter_batches(batch_size=500_000):
        for c in xcols: nulos+=b.column(c).null_count
        X=np.column_stack([b.column(c).to_numpy(zero_copy_only=False) for c in xcols]); infs+=int(np.isinf(X).sum()); nulos+=int(np.isnan(X).sum())
        ids.append(b.select(ID).to_pandas())
    ids=pd.concat(ids,ignore_index=True); g=ids.groupby(ID[:2]).size()
    a=dict(arquivo=name,linhas=int(len(ids)),colunas=len(cols),n_variaveis_processo=len(xcols),variaveis=xcols,
           classes=sorted(int(x) for x in ids.faultNumber.unique()),n_classes=int(ids.faultNumber.nunique()),
           runs_por_classe={int(k):int(v) for k,v in ids.groupby("faultNumber").simulationRun.nunique().items()},
           amostras_por_run=dict(min=int(g.min()),max=int(g.max())),sample_min=int(ids["sample"].min()),sample_max=int(ids["sample"].max()),
           run_min=int(ids.simulationRun.min()),run_max=int(ids.simulationRun.max()),nulos_ou_nan=int(nulos),infinitos=int(infs),
           duplicatas_chave=int(ids.duplicated(subset=ID).sum()),
           rdata_bytes=os.path.getsize(os.path.join(RAW,name+".RData")) if os.path.exists(os.path.join(RAW,name+".RData")) else None,
           parquet_bytes=os.path.getsize(os.path.join(PROC,name+".parquet")))
    aud[name]=a; rp=set(a["runs_por_classe"].values())
    rows.append(dict(Arquivo=name,Linhas=a["linhas"],Colunas=a["colunas"],Classes=a["n_classes"],Runs_por_classe=(rp.pop() if len(rp)==1 else "varia"),
                     Amostras_por_run=(a["amostras_por_run"]["min"] if a["amostras_por_run"]["min"]==a["amostras_por_run"]["max"] else "varia"),
                     Nulos=a["nulos_ou_nan"],Infinitos=a["infinitos"],Duplicatas=a["duplicatas_chave"])); print(name,a["linhas"],a["n_classes"],flush=True)
v=aud["TEP_Faulty_Training"]["variaveis"]
aud["_consistencia"]=dict(mesmas_variaveis_treino_teste=(v==aud["TEP_Faulty_Testing"]["variaveis"]),n_xmeas=sum(c.startswith("xmeas") for c in v),n_xmv=sum(c.startswith("xmv") for c in v),
    sementes_treino_teste_nao_sobrepostas="por construção do dataset (Rieth et al., 2017); arquivos distintos")
json.dump(aud,open(os.path.join(META,"auditoria.json"),"w"),indent=2,default=str); pd.DataFrame(rows).to_csv(os.path.join(TAB,"tab01_caracterizacao_base.csv"),index=False)
c=aud["_consistencia"]
with open(os.path.join(REP,"01-auditoria.md"),"w") as f:
    f.write("# Relatório de auditoria da base — WP1A Etapa 1 (§9.1)\n\nFonte: Rieth et al. (2017), Harvard Dataverse, DOI 10.7910/DVN/6C3JR1. MD5 de cada .RData verificado no download.\n\n## Tabela 1 — Caracterização da base\n\n"+pd.DataFrame(rows).to_markdown(index=False)+"\n\n")
    f.write(f"## Variáveis de processo\n\n- Total: **{aud['TEP_Faulty_Training']['n_variaveis_processo']}** (XMEAS: {c['n_xmeas']} · XMV: {c['n_xmv']})\n- Mesmas variáveis em treino e teste: **{c['mesmas_variaveis_treino_teste']}**\n\n## Verificações por arquivo\n\n")
    for name in FILES:
        a=aud[name]; f.write(f"### {name}\n- classes: {a['classes']}\n- runs por classe: {sorted(set(a['runs_por_classe'].values()))} · simulationRun {a['run_min']}–{a['run_max']}\n- amostras por run: {a['amostras_por_run']['min']}–{a['amostras_por_run']['max']} · sample {a['sample_min']}–{a['sample_max']}\n- nulos/NaN {a['nulos_ou_nan']} · infinitos {a['infinitos']} · duplicatas de chave {a['duplicatas_chave']}\n- .RData {(a['rdata_bytes'] or 0)/1e6:.0f} MB → parquet float32 {a['parquet_bytes']/1e6:.0f} MB\n\n")
print("AUDITORIA COMPLETA",flush=True)
