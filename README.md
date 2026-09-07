# MEI0028 – Modelagem e Simulação · WP1A

**Benchmark reproduzível de métodos clássicos de aprendizado de máquina para diagnóstico de falhas no Tennessee Eastman Process**

Disciplina MEI0028 – Modelagem e Simulação, Programa de Pós-Graduação, Pontifícia Universidade Católica de Goiás, 2026. Professor responsável: Clarimar José Coelho. Subprojeto WP1A (Grupo A).

Este repositório contém o código, o protocolo, os resultados e as predições que sustentam o artigo submetido à Revista Sodebras. Ele existe para que qualquer pessoa possa reexecutar o experimento e conferir cada número publicado.

## O que foi feito

Seis famílias clássicas — regressão logística, árvore de decisão, Random Forest, gradient boosting, XGBoost e SVM aproximado — foram treinadas e avaliadas sobre 21 condições do Tennessee Eastman Process, sob um protocolo único e integralmente declarado. Sobre 10,08 milhões de amostras de teste, provenientes de 10.500 execuções nunca vistas:

| Modelo | F1 macro | MCC | Inferência (µs/amostra) | Tamanho (MB) |
|---|---|---|---|---|
| XGBoost | 0,817 | 0,750 | 31,44 | 13,0 |
| Random Forest | 0,794 | 0,729 | 9,68 | 286,2 |
| Árvore de decisão | 0,741 | 0,656 | 0,16 | 1,8 |
| Gradient boosting | 0,706 | 0,645 | 43,28 | 6,6 |
| SVM (Nyström + SGD) | 0,512 | 0,500 | 2,18 | 1,1 |
| Regressão logística | 0,475 | 0,553 | 0,14 | 0,01 |

As falhas 3, 9 e 15 permanecem persistentemente confundidas com a operação normal por todos os métodos.

## Base de dados

Rieth, C. A.; Amsel, B. D.; Tran, R.; Cook, M. B. (2017). *Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation*. Harvard Dataverse, **DOI [10.7910/DVN/6C3JR1](https://doi.org/10.7910/DVN/6C3JR1)**, domínio público. São 4 arquivos `.RData`, 1,40 GB, 15,33 milhões de linhas.

Os dados **não** estão neste repositório: `src/01_download.py` os baixa da fonte original e confere os MD5 publicados. Os modelos treinados (112 MB) também ficam de fora, por serem reproduzíveis a partir do código e das sementes fixadas.

## Como reproduzir

```bash
uv venv --python 3.11 .venv && uv pip install -r requirements.txt
brew install libomp r          # macOS: XGBoost e conversão .RData → Parquet
python src/01_download.py      # baixa a base e confere MD5
python src/convert_rdata.py    # converte para Parquet (float32), por classe
python src/02_auditoria.py     # §9.1 do WP1A
python src/03_split.py         # divisão por execução, semente 42
python src/05_eda.py           # análise exploratória
python src/06_busca_hp.py      # hiperparâmetros, só na validação
python src/06b_merge_hp.py     # congela a configuração
python src/07_treino_final.py  # 6 modelos × 5 sementes
python src/08_avaliacao.py     # métricas, figuras e testes estatísticos
```

Complementos: `04_piloto_vazamento.py` e `04b_piloto_vazamento_repeticoes.py` medem o efeito da unidade de divisão; `10_bootstrap_execucao.py` estima a incerteza sobre novas execuções; `06c_busca_hp_lr.py` refaz a regressão logística até a convergência; `fig00_fluxograma_protocolo.py` gera a figura do protocolo.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `src/` | Scripts numerados na ordem de execução, mais os encadeadores `.sh` |
| `configs/` | Divisão (semente e tamanhos) e hiperparâmetros congelados antes do teste |
| `notebooks/` | Três notebooks Colab que documentam a execução de ponta a ponta |
| `results/tables/` | Todas as tabelas do artigo e as auxiliares, em CSV |
| `results/figures/` | Figuras do artigo e da análise exploratória, em PNG |
| `results/predictions/` | Predição de cada modelo e semente sobre o teste completo, em Parquet |
| `results/metadata/` | Manifesto da divisão, ambiente, busca de hiperparâmetros, registros de execução |
| `reports/` | Relatório de auditoria, registro de desafios e ajustes, checklist do WP1A |
| `revisao_bibliografica/` | Análise de treze trabalhos sobre o TEP: tabela mestra, comparabilidade, auditoria das afirmações e ancoragem das citações |

Os PDFs dos artigos analisados não estão aqui, por serem material protegido por direito autoral das editoras; a tabela mestra traz o DOI de cada um.

## Decisões de protocolo

- **Unidade de divisão = execução completa** (`simulationRun`). Do arquivo de treinamento, 100 execuções por classe para treino e 50 para validação; o arquivo de teste é usado integralmente, 500 por classe. A interseção entre conjuntos é verificada programaticamente e o manifesto, gerado de forma independente em duas máquinas, resultou idêntico byte a byte.
- **Rótulo físico.** Como a falha é introduzida após o início de cada execução, as amostras anteriores (≤ 20 no treino, ≤ 160 no teste) recebem a classe normal. As métricas com o rótulo da execução inteira também são reportadas.
- Padronização ajustada apenas no treinamento. Sem seleção de atributos, engenharia temporal ou reamostragem.
- SVM por aproximação de Nyström do núcleo RBF seguida de SVM linear treinado por gradiente estocástico em lotes (`src/nystroem_sgd.py`); o núcleo exato é inviável na escala do problema.
- Hiperparâmetros por grade fatorial reduzida, 4 a 12 configurações por modelo, avaliados por F1 macro **na validação**. O conjunto de teste é lido uma única vez, depois de a configuração estar congelada.
- Cinco sementes (42, 123, 2024, 7, 555) para a estabilidade do algoritmo; bootstrap por execução (2.000 réplicas) para a incerteza de generalização.
- Custo computacional medido no mesmo computador (Apple M3, 8 GB). O Colab foi usado apenas para a busca de hiperparâmetros do XGBoost, e esses tempos não entram na comparação.

## Ambiente

Python 3.11.15, numpy 2.4.6, pandas 3.0.5, scikit-learn 1.9.0, xgboost 3.2.0, scipy 1.17.1. Detalhes em `results/metadata/ambiente.json` e `requirements.txt`.

## Licença

Código sob licença MIT (`LICENSE`). Tabelas, figuras e predições sob CC BY 4.0. A base de dados original é de Rieth et al. (2017) e está em domínio público.
