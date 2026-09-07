"""06b_merge_hp.py — mescla os resultados da busca de hiperparâmetros (Mac: 5 modelos CPU; Colab: logreg + xgboost GPU),
escolhe a melhor configuração por modelo pelo F1 macro na validação e grava configs/hiperparametros_escolhidos.json."""
import os, json
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),".."); META=os.path.join(ROOT,"results","metadata"); CFG=os.path.join(ROOT,"configs")
fontes={"mac":os.path.join(META,"busca_hp_resultados.json"),"colab":os.path.join(META,"busca_hp_resultados_COLAB.json")}
merged={}
for origem,f in fontes.items():
    if not os.path.exists(f): print("ausente:",f); continue
    for m,rs in json.load(open(f)).items():
        for r in rs:
            k=json.dumps(r["params"],sort_keys=True); merged.setdefault(m,{})
            if k not in merged[m]: merged[m][k]=dict(r,origem=origem)
out={m:list(v.values()) for m,v in merged.items()}; json.dump(out,open(os.path.join(META,"busca_hp_resultados_MERGED.json"),"w"),indent=1)
best={m:max(v,key=lambda r:r["f1_macro"]) for m,v in out.items()}; json.dump(best,open(os.path.join(CFG,"hiperparametros_escolhidos.json"),"w"),indent=2)
esperados=["regressao_logistica","arvore_decisao","random_forest","gradient_boosting","xgboost","svm_nystroem"]; falt=[m for m in esperados if m not in best]
for m in esperados:
    if m in best: print(f"{m:<22} {len(out[m]):>2} configs  melhor F1m={best[m]['f1_macro']:.4f} ({best[m]['origem']})  {best[m]['params']}")
if falt: raise SystemExit(f"FALTAM modelos na busca: {falt}")
print("MERGE HP COMPLETO")
