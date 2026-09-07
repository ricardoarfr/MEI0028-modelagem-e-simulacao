# Checklist de exigências do WP1A — validação final

> Cada item do MEI0028_WP1A é listado com a evidência que o satisfaz. Status: ✅ atendido ·
> ⏳ em execução · ⬜ pendente · ⚠️ atendido com ressalva. **Validação final: 06/09/2026, após conclusão de todas as fases.**
>
> **Pendências que só o grupo pode resolver:** (1) nomes, titulações e e-mails dos autores e minibiografias em nota de rodapé (template Sodebras); (2) A9 apresentação; (3) decisão sobre publicar o repositório (GitHub) — hoje os notebooks estão no Drive.

## §6.2 Objetivos específicos

| # | Objetivo | Evidência | Status |
|---|---|---|---|
| 1 | Auditar e documentar a base | `reports/01-auditoria.md`, `results/tables/tab01_caracterizacao_base.csv`, `results/metadata/auditoria.json`; MD5 dos 4 arquivos verificados (`download_manifest.json`) | ✅ |
| 2 | Protocolo único de divisão treino/validação/teste sem vazamento entre execuções | `results/metadata/manifesto_divisao.csv` (unidade = run; interseção verificada = 0); `configs/split.json`; manifesto **idêntico byte a byte** entre Mac e Colab | ✅ |
| 3 | Treinar Regressão Logística, Árvore de Decisão, Random Forest, Gradient Boosting, SVM e XGBoost | `src/07_treino_final.py`; SVM via aproximação de Nyström (§8 do WP1A: "implementação escalável") | ✅ |
| 4 | Avaliar por métricas globais e por classe | `tab03_metricas_globais.csv`, `tab04_metricas_por_classe.csv` | ✅ |
| 5 | Comparar tempos de treinamento, inferência e tamanho dos modelos | `tab05_custo_computacional.csv`, `fig02_custo_computacional.png` — mesmo hardware, 5 sementes | ✅ |
| 6 | Identificar falhas com maior grau de confusão | `tab06_falhas_confundidas.csv`, `tab06b_dificuldade_por_classe.csv`, matrizes de confusão | ✅ |
| 7 | Produzir tabelas, figuras, resultados e documentação reproduzível | `results/`, `apresentacao/REGISTRO-FIGURAS-TABELAS.xlsx`, `requirements.txt`, sementes fixas, scripts numerados | ✅ |
| 8 | Elaborar artigo científico | `artigo/ARTIGO-FINAL.md` + `ARTIGO-FINAL.docx` (2.997 palavras no corpo; 22 refs; 4 tab.; 4 fig.) | ✅ |

## §9 Protocolo experimental

| Etapa | Exigência | Evidência | Status |
|---|---|---|---|
| 9.1 Auditoria | arquivos; linhas/colunas; nomes/tipos/significado; distribuição das classes; execuções por classe; ausentes/infinitos/inconsistentes; duplicações; relação arquivos×classes×runs | todos os 8 itens em `auditoria.json` e `01-auditoria.md` | ✅ |
| 9.2 Exploratória | descritivas; distribuição das classes; variabilidade; correlações; PCA; normal vs. falha | `tab_eda_*.csv`, `fig_eda_pca.png`, `fig_eda_correlacao.png`, `fig_eda_separacao.png`, `eda_sumario.json` | ✅ |
| 9.3 Divisão | por execução completa; treino/validação/teste; semente, lista e manifesto salvos | `manifesto_divisao.csv`, `split.json` (seed 42) | ✅ |
| 9.4 Pré-processamento | padronização ajustada só no treino | `StandardScaler().fit(treino)` em 04/06/07 | ✅ |
| 9.5 Treinamento e seleção | hiperparâmetros só na validação; teste após congelamento | `06_busca_hp.py` (validação), `hiperparametros_escolhidos.json` congelado antes de `07` | ✅ |
| 9.6 Avaliação final | precisão/revocação/F1 por classe; F1 macro (eq. 1); acurácia balanceada (eq. 2); MCC multiclasse | `08_avaliacao.py` | ✅ |

## §10 Métricas (13 itens)

| Métrica | Onde | Status |
|---|---|---|
| acurácia · acurácia balanceada · precisão macro · revocação macro · F1 macro · F1 ponderada · MCC | `tab03_metricas_globais.csv` (precisão/revocação macro derivadas de `tab04`) | ✅ |
| matriz de confusão | `tab_matriz_confusao_<modelo>.csv`, `fig03_*` | ✅ |
| métricas por classe | `tab04_metricas_por_classe.csv` | ✅ |
| tempo de treinamento · tempo de inferência · tamanho do modelo salvo | `tab05_custo_computacional.csv` | ✅ |
| consumo de memória, quando disponível | `pico_memoria_MB` (ru_maxrss por subprocesso) em `tab05` | ✅ |

## §11 Análise estatística

| Exigência | Evidência | Status |
|---|---|---|
| média, desvio-padrão e IC para múltiplas execuções/sementes | 5 sementes; IC 95% (t, gl=4) em `tab03` | ✅ |
| Friedman + pós-hoc; Wilcoxon com correção | `tab07_estatistica.csv` (Friedman; Wilcoxon pareado + Holm) | ✅ |
| unidade experimental explicitada; não tratar linha temporal como repetição | unidade = repetição de treinamento (semente); divisão por run | ✅ |

## §12 Insumos para o artigo (11 itens)

| # | Insumo | Arquivo | Status |
|---|---|---|---|
| 1 | tabela de caracterização da base | `tab01_caracterizacao_base.csv` | ✅ |
| 2 | tabela dos hiperparâmetros | `tab02_hiperparametros.csv` | ✅ |
| 3 | tabela comparativa das métricas globais | `tab03_metricas_globais.csv` | ✅ |
| 4 | tabela de métricas por classe | `tab04_metricas_por_classe.csv` | ✅ |
| 5 | matrizes de confusão | `fig03_matriz_confusao_*.png` + CSV | ✅ |
| 6 | gráfico comparativo de F1 macro e MCC | `fig01_f1_mcc_comparativo.png` | ✅ |
| 7 | gráfico de custo computacional | `fig02_custo_computacional.png` | ✅ |
| 8 | análise das falhas mais confundidas | `tab06_*.csv` + texto | ✅ |
| 9 | CSV com resultados brutos | `tab03b_metricas_por_seed.csv`, `results/predictions/*.parquet`, `busca_hp_resultados_MERGED.json` | ✅ |
| 10 | metadados do ambiente computacional | `results/metadata/ambiente.json`, `requirements.txt` | ✅ |
| 11 | repositório com scripts numerados e instruções | `ProjetoA_WP1A/src/01…09`, `README.md`; **3 notebooks Colab** no Drive (`WP1A_notebooks_TEP_benchmark/`: dados-auditoria-divisão-EDA · vazamento-hiperparâmetros · treino-avaliação-registro) | ✅ |

## §15 Entregas (A1–A9)

| ID | Entrega | Evidência | Status |
|---|---|---|---|
| A1 | Relatório de auditoria | `reports/01-auditoria.md` | ✅ |
| A2 | Análise exploratória | figuras e tabelas `eda_*` | ✅ |
| A3 | Manifesto da divisão por execução | `manifesto_divisao.csv` | ✅ |
| A4 | Implementação dos seis modelos | `src/07_treino_final.py` | ✅ |
| A5 | Resultados completos | `results/` | ✅ |
| A6 | Figuras e tabelas do artigo | `apresentacao/` + registro Excel | ✅ |
| A7 | Relatório técnico final | `reports/01-auditoria.md` + `artigo/DESAFIOS-E-AJUSTES.md` + `plano/` (relatório consolidado = artigo + estes) | ⚠️ parcial |
| A8 | Manuscrito científico | `artigo/ARTIGO-FINAL.docx` | ✅ (autores/minibiografias a preencher) |
| A9 | Apresentação | fora do escopo desta sessão | ⬜ |

## §18 Riscos e cuidados metodológicos

| Risco | Mitigação adotada | Status |
|---|---|---|
| vazamento entre execuções | divisão por run + manifesto + verificação de interseção; efeito **medido** no piloto | ✅ |
| ajuste de hiperparâmetros no teste | teste jamais lido em `06`; congelamento antes de `07` | ✅ |
| comparação injusta entre modelos | mesmo manifesto, mesmo pré-processamento, mesma busca (grade fatorial reduzida), mesmas 5 sementes | ✅ |
| uso exclusivo de acurácia | F1 macro + MCC como métricas principais | ✅ |
| omissão de custo computacional | tempos/tamanho/memória no mesmo hardware | ✅ |
| inferência estatística sobre amostras correlacionadas | unidade = repetição de treinamento | ✅ |
| interpretação causal indevida de importâncias | não se reportam importâncias como causa | ✅ |
| falta de registro de versões e sementes | `requirements.txt`, `ambiente.json`, sementes fixas | ✅ |

## §20 Estrutura mínima do repositório

`ProjetoA_WP1A/{data/{raw,processed},src,configs,models,results/{tables,figures,predictions,metadata},reports,article→../artigo,README.md,requirements.txt}` — ✅ criada; `README.md` ✅; notebooks Colab ✅.
