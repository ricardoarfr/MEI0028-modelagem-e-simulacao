"""03_split.py — Etapa 3 do WP1A (§9.3): divisão experimental POR RUN.
Gera o manifesto de divisão (entrega A3) e verifica interseção vazia entre conjuntos.
Configuração: treino 100 runs/classe · validação 50 runs/classe (ambos do Training)
              teste = TODOS os 500 runs/classe do Testing (inferência é barata).
Precedente: Koçak et al. (2026) usaram 200/500; Lyu et al. (2026) usaram 100/50/200."""
import os, json, numpy as np, pandas as pd
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
PROC=os.path.join(ROOT,"data","processed"); META=os.path.join(ROOT,"results","metadata"); CFG=os.path.join(ROOT,"configs")
SEED=42; N_TREINO=100; N_VAL=50
rng=np.random.RandomState(SEED)
tr_ff=pd.read_parquet(os.path.join(PROC,"TEP_FaultFree_Training.parquet"),columns=["faultNumber","simulationRun"]).drop_duplicates()
tr_f =pd.read_parquet(os.path.join(PROC,"TEP_Faulty_Training.parquet"),columns=["faultNumber","simulationRun"]).drop_duplicates()
te_ff=pd.read_parquet(os.path.join(PROC,"TEP_FaultFree_Testing.parquet"),columns=["faultNumber","simulationRun"]).drop_duplicates()
te_f =pd.read_parquet(os.path.join(PROC,"TEP_Faulty_Testing.parquet"),columns=["faultNumber","simulationRun"]).drop_duplicates()
training=pd.concat([tr_ff,tr_f]); testing=pd.concat([te_ff,te_f])
rows=[]  # (origem, classe, run, conjunto) — origem distingue Training de Testing (sementes distintas por construção)
for cls,g in training.groupby("faultNumber"):
    runs=g.simulationRun.to_numpy().copy(); rng.shuffle(runs)  # .copy(): pandas>=3 retorna array read-only
    for r in runs[:N_TREINO]: rows.append(("Training",int(cls),int(r),"treino"))
    for r in runs[N_TREINO:N_TREINO+N_VAL]: rows.append(("Training",int(cls),int(r),"validacao"))
    for r in runs[N_TREINO+N_VAL:]: rows.append(("Training",int(cls),int(r),"nao_usado_training"))
for cls,g in testing.groupby("faultNumber"):
    for r in g.simulationRun: rows.append(("Testing",int(cls),int(r),"teste"))
man=pd.DataFrame(rows,columns=["origem","faultNumber","simulationRun","conjunto"])
# --- VERIFICAÇÃO OBRIGATÓRIA: nenhuma (classe,run) em mais de um conjunto usado
usados=man[man.conjunto.isin(["treino","validacao","teste"])]
dup=usados.duplicated(subset=["origem","faultNumber","simulationRun"]).sum()  # dentro do mesmo arquivo de origem
assert dup==0, f"VAZAMENTO: {dup} pares (classe,run) em mais de um conjunto"
res=man.groupby(["conjunto","faultNumber"]).size().unstack(0).fillna(0).astype(int)
man.to_csv(os.path.join(META,"manifesto_divisao.csv"),index=False)
json.dump(dict(seed=SEED,n_treino_por_classe=N_TREINO,n_validacao_por_classe=N_VAL,teste="todos os runs do Testing",
               unidade="simulationRun (execução completa)",verificacao_intersecao_vazia=bool(dup==0),
               totais=man.conjunto.value_counts().to_dict()),open(os.path.join(CFG,"split.json"),"w"),indent=2)
print(res); print(f"\ninterseção entre conjuntos: {dup} → {'OK' if dup==0 else 'FALHA'}"); print("MANIFESTO GRAVADO")
