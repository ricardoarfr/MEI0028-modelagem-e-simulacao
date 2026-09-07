# Tabela de comparabilidade experimental

**Objetivo:** verificar quais trabalhos publicados têm condições experimentais próximas o
bastante das nossas para que seus resultados sirvam de benchmark de comparação.

**Método:** leitura do **texto completo** de cada trabalho (não do resumo), extração de 12
parâmetros metodológicos, e classificação em COMPARÁVEL / PARCIALMENTE COMPARÁVEL / NÃO
COMPARÁVEL.

**Regra de extração — sem inferência.** Todo campo traz apenas o que o artigo declara
explicitamente. Onde o artigo não declara, o registro é literalmente
**"não informado no artigo"**. Nenhum valor foi deduzido, calculado ou completado.

**Nosso protocolo de referência:** dataset Rieth et al. (2017) · 52 variáveis · 21 classes
multiclasse · **divisão por run** · F1 macro + MCC · repetições com dispersão.

---

## Quadro-resumo

| # | Trabalho | Ano | Dataset | Variáveis | Classes | Unidade de divisão | F1 macro | MCC | Repetições | Veredito |
|---|---|---|---|---|---|---|---|---|---|---|
| **5** | **KOÇAK et al., *Processes*** | **2026** | ✅ **Rieth** | ✅ 52 (→312 features) | ✅ **21** multiclasse | ✅ **POR RUN** | ✅ | ✗ | ✅ 5 sementes + IC | ✅ **COMPARÁVEL** |
| 8 | LYU et al., *ChemRxiv* 🔴preprint | 2026 | ✅ Rieth | ✅ 52 | ❌ **18** (exclui IDV3/9/15) | ✅ **POR RUN** | ✅ | ✗ | ✗ | ◐ **PARCIAL** |
| 9 | AVANASHILINGAM et al., *PHMAP* | 2026 | ✅ Rieth | ❌ **53** declaradas | ✅ **21** multiclasse | ✅ **POR RUN** | ✅ | ✗ | ⚠️ só K=5 | ◐ **PARCIAL** |
| 1 | HU et al., *Energies* | 2022 | **não informado** | 52 → 4-35 por falha | 21, formulação não declarada | **não informado** | ✗ | ✗ | ✗ | ✗ **NÃO** |
| 2 | XU et al., *Applied Sciences* | 2022 | Braatz/MIT | 52 → **5 por categoria** | 21, binário N vs. F | **não informado** | ✗ | ✗ | ✗ | ✗ **NÃO** |
| 3 | LI et al., *Scientific Reports* | 2026 | Braatz (GitHub) | 52 → média **5** | **21 binários** | ❌ **embaralhado** | ✗ | ✗ | ✅ 10 execuções | ✗ **NÃO** |
| 4 | MÁRQUEZ-VERA et al., *Algorithms* | 2026 | **simulação própria** | **7 fixas** | **10 falhas** one-vs-rest | ❌ mesma run | ✗ | ✗ | ✗ | ✗ **NÃO** |
| 6 | ZHANG et al., *Sensors* | 2021 | Braatz/MIT | ✅ 52 | 21 falhas (inclui IDV21) | **não informado** | ✗ (OACC) | ✗ | ✗ | ✗ **NÃO** |
| 7 | ~~REZGUI et al., *SEES*~~ | 2024 | — | — | — | — | — | — | — | 🔴 **RETIRADO DO PERIÓDICO** |

## Placar: 1 comparável · 2 parcialmente comparáveis · 5 não comparáveis · 1 retirado

## Padrão transversal — os cinco fatos que sustentam o artigo

1. **NENHUM dos nove trabalhos reporta MCC.**
2. **NENHUM reporta custo computacional de todas as famílias comparadas no mesmo equipamento** — Lyu (2026) reporta o tempo de treinamento de todos os modelos sem declarar o equipamento; Koçak (2026) mede latência e tamanho só do XGBoost (verificação literal em `08-AUDITORIA-TABELA1.md`, 06/09/2026).
3. **Apenas três dos nove dividem por run** — e os três são de 2026. Dos nove, só Koçak, Lyu e Li declaram o tratamento das amostras anteriores à falha (critério e trechos em `08-AUDITORIA-TABELA1.md`).
4. **Quatro dos nove não fazem classificação multiclasse** — são coleções de detectores
   binários, cujo F1 médio é estruturalmente inflado (nunca penalizam confusão entre falhas).
5. **Dos três que dividem por run, nenhum publica os números dos baselines clássicos:**
   Koçak afirma que o XGBoost superou RF e SVM sem mostrar os valores; Lyu compara XGBoost
   contra arquiteturas profundas, não contra a família clássica; Avanashilingam usa só
   LightGBM.

## Valores utilizáveis como referência de comparação

Únicos números publicados que podem ser confrontados com os nossos — sempre com as ressalvas
registradas na ficha de cada trabalho:

| Trabalho | Modelo | Classes | Métrica | Valor | Ressalva obrigatória |
|---|---|---|---|---|---|
| Koçak (2026) | XGBoost | 21 | F1 macro **sample-level** | **0,8823** | 312 features engenheiradas, W=50 |
| Koçak (2026) | XGBoost | 21 | F1 macro **run-level** | **0,9522 ± 0,0035** | agregação por voto majoritário de run |
| Lyu (2026) | XGBoost | **18** | F1 macro | **0,9416** | preprint; exclui as 3 falhas difíceis |
| Avanashilingam (2026) | LightGBM | 21 | F1 macro | **0,9283** | 53 variáveis declaradas; janelas de 60 |

**Nenhum valor de Random Forest, SVM, Regressão Logística, Árvore de Decisão ou Gradient
Boosting está publicado sob protocolo comparável.** Essa é a lacuna que o WP1A preenche.

---

## 1. HU, M.; HU, X.; DENG, Z.; TU, B. (2022) — *Energies* 15(9):3198

**"Fault Diagnosis of Tennessee Eastman Process with XGB-AVSSA-KELM Algorithm"** · DOI 10.3390/en15093198
Texto completo obtido do PDF oficial de produção da MDPI.

| # | Parâmetro | O que o artigo declara |
|---|---|---|
| 1 | Versão/origem da base | **não informado no artigo.** Sem menção a Rieth, Harvard Dataverse, Braatz ou UIUC. Cita apenas Downs & Vogel (1993) como referência do modelo. *Data Availability: "Not applicable."* |
| 2 | Variáveis | 52 — *"12 manipulated variables and 41 process measurements... all 52 variables except for agitator speed"*. **Mas a seleção reduz para número diferente por falha** (Tabela 4): falha 17 → 4 variáveis; falha 5 → 35 |
| 3 | Classes | 21 falhas, IDV(1) a IDV(21), nenhuma excluída. Se é multiclasse de 21 ou 21 binários: **não informado no artigo** |
| 4 | Divisão | 480 amostras de treino por falha, 500 normal, 960 de teste, falha na amostra 161, amostragem de 3 min. **Validação separada: não informado. Proporções: não informado. Origem dos arquivos: não informado** |
| 5 | **Unidade de divisão** | **não informado no artigo.** Nenhuma frase sobre divisão por amostra ou por run |
| 6 | Vazamento | **não informado no artigo.** Zero menções a leakage ou correlação temporal. Reporta FDR de treino 0,9992 e de teste 0,9100 sem analisar o gap |
| 7 | Pré-processamento | **não informado no artigo.** A única normalização citada (MAX-MIN) é para os gráficos de convergência, não para os dados. Janelamento, balanceamento, remoção do período pré-falha: todos não informados |
| 8 | Modelos e hiperparâmetros | XGBoost (seletor): `max_depth=7`, `n_estimators=80`, `learning_rate=0.1`, `subsample=1.0`, `colsample_bytree=0.5`. KELM: valores ótimos de `c` e `S` **não informados**; tipo de kernel **não informado**. AVSSA: população, iterações e função de fitness **não informados** |
| 9 | Métricas | **Uma só: "FDR"**, definida como `(TP+TN)/(TP+TN+FN+FP)` — ou seja, **acurácia**, apesar do nome. Sem F1, sem MCC, sem matriz de confusão |
| 10 | Resultados | Média FDR: KELM 0,7118 · XGB-KELM 0,7539 · AVSSA-KELM 0,8081 · **XGB-AVSSA-KELM 0,9100** |
| 11 | Repetições | **não informado no artigo.** Sem sementes, k-fold, desvio-padrão ou teste estatístico. Todos os valores são números únicos |
| 12 | Reprodutibilidade | Código: **não disponível**. Software, versões, hardware, tempos, tamanho do modelo: **todos não informados** |

### ⚠️ Achado grave — dado fabricado na tabela comparativa

Os próprios autores declaram, sobre a Tabela 8:

> *"Because EDBN-2 does not include diagnostic rate data for faults 3, 9, and 15... the FDR
> for all three is set to 60% in this work."*

**Três valores da coluna de um método concorrente foram arbitrados pelos autores** e entram
na média publicada (0,9009). Isso é exatamente o tipo de preenchimento que nosso protocolo
proíbe. **Nenhum número da Tabela 8 deste artigo pode ser citado.**

Segundo alerta: a média de 0,8745 da coluna NSVM é calculada sobre **18 falhas**, não 21
(*"NSVM did not provide feature extraction for faults 3, 9 and 15"*), e portanto não é
comparável às demais médias da mesma tabela.

### Veredito: **NÃO COMPARÁVEL**

| Divergência | Detalhe |
|---|---|
| Dataset | Origem não declarada — impossível afirmar Rieth ou Braatz |
| Variáveis | Subconjuntos variáveis (4 a 35) por falha, contra 52 fixas |
| Formulação | Multiclasse vs. binário por falha não declarado |
| **Unidade de divisão** | **Não informada — bloqueador** |
| Métricas | Sem F1, sem MCC. "FDR" é acurácia renomeada |
| Estatística | Sem repetições, sem dispersão, sem teste |
| Integridade | Dados fabricados na tabela comparativa |

**Baselines aproveitáveis:** o artigo **não reporta RF, SVM ou XGBoost puros como
classificadores** — os três aparecem apenas como seletores de atributos, e os de RF e NSVM
são resultados **citados de terceiros**. Os únicos baselines internamente consistentes são
KELM (0,7118), XGB-KELM (0,7539) e AVSSA-KELM (0,8081) — todos em acuródia, sem dispersão.

---

## 2. XU, H.; REN, T.; MO, Z.; YANG, X. (2022) — *Applied Sciences* 12(17):8868

**"A Fault Diagnosis Model for Tennessee Eastman Processes Based on Feature Selection and Probabilistic Neural Network"** · DOI 10.3390/app12178868
Texto completo obtido do PDF oficial de produção da MDPI.

| # | Parâmetro | O que o artigo declara |
|---|---|---|
| 1 | Versão/origem da base | **Braatz Group / MIT, declarado com URL:** *"they can be found at the following address: http://web.mit.edu/braatzgroup/links.html"*. **Não é Rieth/Harvard Dataverse** |
| 2 | Variáveis | 52 (41 medições + 11 manipuladas) → **reduzidas a exatamente 5 por categoria de falha** (Tabela 5). Ex.: categoria 1 → variáveis 40, 42, 13, 44, 18 |
| 3 | Classes | 21 categorias, nenhuma excluída. Avaliação estruturada como **N (normal) vs. F (falha) por categoria** (legenda da Tabela 8). Se é multiclasse ou 21 binários: **não informado no artigo** |
| 4 | Divisão | 960 amostras por execução, falha após 8 h, primeiras 160 normais, amostragem de 3 min. **Tamanhos de treino e teste: não informados. Proporções: não informadas. Validação separada: não informada** |
| 5 | **Unidade de divisão** | **não informado no artigo.** A frase mais próxima é *"The simplified data samples are preprocessed and then randomly input to PNN"* — que qualifica a entrada na rede, não a partição |
| 6 | Vazamento | **não informado no artigo.** Discute overfitting como comportamento de classificador, não como contaminação treino/teste |
| 7 | Pré-processamento | **não informado no artigo** — apenas a palavra *"preprocessed"*, sem especificar o quê nem se ajustado só no treino. Reconhece o desbalanceamento sem tratá-lo: *"TE datasets are high-dimensional, small imbalanced samples"* |
| 8 | Modelos e hiperparâmetros | KNN: `k=7`. PNN não otimizada: `σ=0.8`. PSO: espaço [−5,5], fator de aprendizado 1,49445. GA: crossover 0,7, mutação 0,01. **SVM, LDA, QDA: *"default values of MATLAB tools"*** — kernel e C **não informados** |
| 9 | Métricas | "Diagnosis rate" (**fórmula nunca dada no artigo**), Accuracy (Eq. 23) e F1 (Eq. 24). **Macro/micro/ponderada: não informado.** O F1 é por par normal-vs-falha, **não é F1 macro sobre 21 classes**. Sem MCC |
| 10 | Resultados | Médias — MSSA-PNN: Acc 0,88 / F1 0,91 · **SVM: Acc 0,75 / F1 0,84** · KNN: 0,70 / 0,79 · QDA: 0,81 / 0,83 · LDA: 0,69 / 0,74 · CS-BP: 0,84 / 0,88 · MaxEnt: 0,52 / 0,46 |
| 11 | Repetições | **não informado no artigo.** As "20 populações / 30 iterações" são da metaheurística, não repetições do experimento. Valores únicos, sem dispersão |
| 12 | Reprodutibilidade | Código: **não disponível**. Software: apenas *"MATLAB"*, **sem versão**. Hardware, tempos, tamanho: **não informados**. Reconhece: *"the influence of operation time is ignored in the experiments"* |

### ⚠️ Achado — o SVM baseline está colapsado

Na Tabela 8, a coluna SVM registra **0,00 de acerto no estado normal em 14 das 21
categorias**, com 1,00 na classe de falha. Os autores reconhecem: *"SVM has 'false positives'
in 14 fault categories"*. É um classificador que degenerou em prever sempre "falha", rodando
com hiperparâmetros default do MATLAB.

**Consequência:** o F1 de 0,84 do SVM neste artigo **não representa um SVM bem ajustado** e
não serve como referência de desempenho do algoritmo.

### Veredito: **NÃO COMPARÁVEL**

| Divergência | Detalhe |
|---|---|
| Dataset | Braatz/MIT (1 run por classe), não Rieth (500 runs por classe) |
| Variáveis | **5 por categoria**, e conjuntos diferentes para cada falha, contra 52 fixas |
| Formulação | F1 por par normal-vs-falha, não F1 macro sobre 21 classes |
| **Unidade de divisão** | **Não informada — bloqueador** |
| Métricas | Sem MCC; esquema de agregação do F1 não declarado |
| Estatística | Sem repetições, sem dispersão, sem teste |
| Baseline SVM | Colapsado, com hiperparâmetros default |

**Baselines aproveitáveis:** este artigo é melhor que o anterior — reporta classificadores
puros com resultados separados em três métricas. Mas **não há RF nem XGBoost como
classificadores** (RF aparece só como seletor, reaproveitado de terceiros). Se citados, os
números precisam vir com a qualificação explícita: *regime binário por falha, 5 atributos,
dataset Braatz, execução única*.

---

## 3. LI, D. et al. (2026) — *Scientific Reports* 16:19405

**"An evolutionary weighted feature influence factor feature selection method for fault detection in the Tennessee Eastman complex chemical process"** · DOI 10.1038/s41598-026-49874-5
Texto completo obtido (HTML da Nature, incluindo tabelas).

| # | Parâmetro | O que o artigo declara |
|---|---|---|
| 1 | Versão/origem da base | **Braatz/UIUC via mirror GitHub** — *"available for download at the URL GitHub—camaramm/tennessee-eastman-profBraatz"*. **Não é Rieth** |
| 2 | Variáveis | 52 originais → **média de 5,00 por falha** (9,5% de 52). Por falha (Tabela 5): d04/d06/d07/d21 → 1 variável; d17 → 22; d09 → 9 |
| 3 | Classes | **NÃO é multiclasse.** São **21 problemas binários independentes** (normal vs. falha k). Declarado: *"optimizes independent fault-specific feature subsets for each fault mode rather than a unified subset for simultaneous multi-fault detection"* |
| 4 | Divisão | 90% treino/teste + 10% validação, com 10-fold interno. **Contradição interna:** os resultados dizem *"a random 7:3 split for training and test sets"*, conflitando com o 9:1 do pré-processamento |
| 5 | **Unidade de divisão** | **POR AMOSTRA, com embaralhamento aleatório explícito:** *"each fault dataset is randomly shuffled. This removes the influence of temporal order"*. **Agravante:** os arquivos `d0k` (treino) e `d0k_te` (teste) são **fundidos antes** do embaralhamento, destruindo a separação original do benchmark |
| 6 | Vazamento | **não informado no artigo.** A correlação temporal é removida **deliberadamente**, e a implicação não é discutida |
| 7 | Pré-processamento | Min-max com buffer: `x' = (x − xmin)/(1,2·(xmax − xmin))`. **Escopo do ajuste (só treino ou tudo): não informado no artigo.** Balanceamento: **não informado** — desbalanceamento reconhecido mas tratado só pela escolha da métrica |
| 8 | Modelos e hiperparâmetros | Classificador principal: árvore de decisão. Também SVM, RF e KNN na generalização cruzada. **Hiperparâmetros de todos os classificadores: não informados no artigo.** Parâmetros do AG remetidos ao Apêndice A (material suplementar em ZIP, não acessado) |
| 9 | Métricas | AUC (na função de fitness) e F1 (avaliação final). **Agregação macro/micro/ponderada: não informado no artigo.** Cada F1 é **binário**. **Sem MCC** |
| 10 | Resultados | **F1 média 0,9579** (WFIF) · d03 0,8780 · d09 0,9103 · d15 0,9334. Comparativos: PCA 0,9346 · Treebagger 0,9577 · MI 0,9555 |
| 11 | Repetições | **10 execuções independentes**, com desvio-padrão reportado — **o melhor dos analisados neste quesito**. Desvio médio do F1: 0,04. Sementes: não informadas |
| 12 | Reprodutibilidade | Código: **não informado no artigo** (só o dataset é linkado). Linguagem, hardware, tempos, tamanho: **não informados** |

### ⚠️ Correção importante à nossa própria leitura anterior

Na tabela mestra, este trabalho constava como *"F1 média de 95,79% nas 21 falhas"*. A leitura do
texto completo mostra que esse **0,9579 é a média de 21 F1 binários**, não um F1 macro de 21
classes. **São grandezas diferentes e o número não é comparável ao nosso.**

Segundo ponto: o ganho do método proposto sobre o Treebagger puro é marginal —
**0,9579 contra 0,9577** — e nulo em d03 e d15, onde os valores são idênticos.

### Veredito: **NÃO COMPARÁVEL**

O bloqueador é duplo e explícito: **dataset Braatz** e **embaralhamento aleatório por amostra
após fundir treino e teste**. É o caso mais claro de vazamento potencial entre os analisados —
embora o artigo não o discuta.

---

## 4. MÁRQUEZ-VERA, M. A. et al. (2026) — *Algorithms* 19(6):485

**"A Wavelet-Based Evolving Fuzzy Framework for Fault Diagnosis in the Tennessee Eastman Process"** · DOI 10.3390/a19060485
Texto completo obtido, com todas as tabelas.

| # | Parâmetro | O que o artigo declara |
|---|---|---|
| 1 | Versão/origem da base | **Simulação própria em Simulink.** *"The data used were obtained from simulations"*. Cada run tem 2001 amostras, falha na 501 e **removida na 1011**. Nem Rieth nem Braatz — e **nenhum desses datasets tem fase de remoção de falha** |
| 2 | Variáveis | Descreve 41 medidas + **12** manipuladas (não 11) → **reduzidas a 7 fixas** (x1, x4, x18, x21, x23, x25, x28) por LARS, aplicado só às 41 medidas |
| 3 | Classes | **One-vs-rest binário para 10 falhas**: IDV1, 2, 4, 5, 6, 7, 8, 10, 13, 14. Faltam IDV3, 9, 11, 12, 15-21. Declarado: *"requires training separate classifiers for each fault"* |
| 4 | Divisão | **85% / 15% dentro da mesma execução** — primeiras 1700 amostras evoluem o sistema, últimas 301 validam. **Não há conjunto de teste separado** |
| 5 | **Unidade de divisão** | **POR AMOSTRA**, corte temporal dentro da mesma run de 2001 amostras. Como a falha ocorre entre 501 e 1011, as 301 amostras de validação caem **inteiramente no regime pós-falha** |
| 6 | Vazamento | **não informado no artigo.** Treino e validação vêm da mesma execução, sem discussão |
| 7 | Pré-processamento | z-score **com parâmetros estimados nos dados de operação normal** — único escopo declarado explicitamente entre todos os artigos analisados. Wavelet db4 nível 4 — mas os autores admitem que **não é a DWT db4 clássica**, e sim diferenças de médias móveis. Undersampling 2:1 |
| 8 | Modelos e hiperparâmetros | Evolving Fuzzy System (Takagi-Sugeno). **12 hiperparâmetros totalmente declarados** (Tabela 2) — o melhor dos analisados. Mas: *"selected empirically based on preliminary experiments"* — **sem busca sistemática** |
| 9 | Métricas | Sensibilidade, especificidade, F1. **Sem acurácia, sem AUC, sem MCC.** Agregação do F1: **não informado no artigo** |
| 10 | Resultados | **F1 73,68%** / sens. 97,37% / espec. 59,25% (Daubechies) · sem pré-proc. 70,67% · Haar 68,67% · Coiflet 57,56% |
| 11 | Repetições | **Nenhuma repetição, nenhum fold, nenhuma semente.** Nenhum desvio-padrão em qualquer tabela |
| 12 | Reprodutibilidade | Código em **Octave, no Google Drive** (não repositório versionado, não DOI) e descrito como *"example code"*. **Contradição de versão:** Seção 2 diz "Octave 5.1.0", Seção 2.4 diz "7.1.0". Hardware, tempos, tamanho: não informados |

### ⚠️ Contradições numéricas internas

A Introdução e os Resultados do mesmo artigo divergem sobre os próprios números:

| Item | Introdução | Tabela 4 (Resultados) |
|---|---|---|
| F1 do Daubechies | 75,50% | **73,68%** |
| Sensibilidade | 97,17% | **97,37%** |
| Especificidade do Haar | 44,37% | **55,37%** |
| F1 do Coiflet | 65,15% | **57,56%** |

Há ainda contradição entre o texto da Tabela 4 (*"The Haar wavelet achieved the best
specificity (55.37%)"*) e a Discussão 3.2 (*"The Daubechies wavelet achieved... the best
specificity (59.25%)"*).

Anomalia adicional: IDV1, IDV2, IDV5 e IDV8 têm **valores idênticos nos três indicadores**
(100,00 / 54,33 / 70,40) — o modelo classificou quase tudo como falha nesses casos.

### Veredito: **NÃO COMPARÁVEL**

Dataset próprio com estrutura incompatível, 10 falhas em vez de 21, one-vs-rest em vez de
multiclasse, 7 variáveis em vez de 52, divisão temporal dentro da mesma run, sem MCC, sem
repetições, e contradições numéricas não resolvidas.

---

# ⚠️ Descoberta transversal — a mais importante até agora

**Nenhum dos quatro trabalhos analisados faz classificação multiclasse de 21 classes.**

Todos são **coleções de detectores binários** — 21 detectores (Hu, Xu, Li) ou 10
(Márquez-Vera). E isso tem uma consequência técnica que invalida a comparação direta:

> Num esquema binário *normal vs. falha k*, o classificador **nunca é penalizado por confundir
> uma falha com outra falha** — que é justamente o erro dominante no TEP multiclasse.
> Além disso, o negativo é dominado por dados normais, que são fáceis de separar.
>
> Por isso, uma "F1 média" de detectores binários é **estruturalmente inflada** em relação a
> um F1 macro de 21 classes. Os números 0,9579 (Li), 0,9100 (Hu) e 0,7368 (Márquez-Vera)
> **não são comparáveis entre si nem com o nosso**.

Somando o quadro dos quatro:

| Critério | Hu 2022 | Xu 2022 | Li 2026 | Márquez-Vera 2026 |
|---|---|---|---|---|
| Dataset Rieth | ✗ (não informado) | ✗ Braatz | ✗ Braatz | ✗ simulação própria |
| 52 variáveis | ✗ (4-35 por falha) | ✗ (5 por falha) | ✗ (média 5) | ✗ (7 fixas) |
| 21 classes multiclasse | ✗ binário | ✗ binário | ✗ binário | ✗ binário, 10 falhas |
| Divisão por run | **não informado** | **não informado** | ✗ embaralhado | ✗ corte na mesma run |
| F1 macro | ✗ | ✗ | ✗ | ✗ |
| MCC | ✗ | ✗ | ✗ | ✗ |
| Repetições com dispersão | ✗ | ✗ | ✓ (10 execuções) | ✗ |
| Código disponível | ✗ | ✗ | ✗ | parcial (Drive) |

---

# ★ 5. KOÇAK, N. F.; SAYGIN, A.; TÜRK, F.; KARADENIZ, A. M. (2026) — *Processes* 14(16):2569

**"Run-Level Fault Detection and SHAP-Based Diagnosis of Persistent Classification Difficulty in the Tennessee Eastman Process"** · DOI 10.3390/pr14162569
Texto completo obtido (HTML + PDF da MDPI, com todas as 12 tabelas).

## ✅ VEREDITO: **COMPARÁVEL** — o único do corpus

| # | Parâmetro | O que o artigo declara | Alinha? |
|---|---|---|---|
| 1 | Versão/origem da base | **Rieth et al., Harvard Dataverse, DOI 10.7910/DVN/6C3JR1** — *"the extended, multi-run TEP dataset generated by Rieth et al., which provides 500 independent simulation runs"*. Usa as partições Training/Testing oficiais | ✅ |
| 2 | Variáveis | **52 = 41 XMEAS + 11 XMV.** Sem seleção redutora — ao contrário, **expande** para 312 features (6 estatísticas de janela × 52 variáveis) | ⚠️ |
| 3 | Classes | **21 = 20 falhas (IDV1-IDV20) + normal.** Nenhuma excluída, e a escolha é deliberada: *"Unlike prior TEP benchmarking studies that exclude Faults 3, 9, and 15... we treat their detectability as an open empirical question"* | ✅ |
| 4 | Divisão | Partições oficiais do Rieth + validação própria: **80/20 dentro do treino, ao nível de run, estratificada por classe.** Teste reservado: *"the official testing partition was not used during feature-design, window-length-selection, or hyperparameter-selection stages"* | ✅ |
| 5 | **Unidade de divisão** | **POR RUN, declarado em cinco pontos distintos:** *"divided, **at the level of individual simulation runs**, into an 80% training subset and a 20% validation subset"*; *"**run-wise** training–validation splitting"*; *"the run-level label was assigned via the majority-vote rule"* | ✅ |
| 6 | Vazamento | **Discutido explicitamente em três frentes:** scaler ajustado só no treino *"thereby preventing information leakage from test data"*; grupo difícil definido a priori na validação, *"data-leakage-free experimental protocol"*; teste de robustez com janelas pós-onset (0,9505 vs 0,9515) | ✅ |
| 7 | Pré-processamento | `StandardScaler` **ajustado só no treino**. Janelamento W=50 (busca em {5,10,20,30,50}). Sem balanceamento — usa amostragem uniforme de 50 vetores/run e macro-média. Sem valores ausentes no dataset | ✅ |
| 8 | Modelos e hiperparâmetros | **XGBoost 3.3.0** totalmente declarado: `n_estimators=500, max_depth=6, learning_rate=0.03, subsample=0.8, colsample_bytree=0.8, min_child_weight=5, reg_alpha=0.1, reg_lambda=1.0`. Busca one-at-a-time, 12 configurações, avaliadas na validação | ✅ |
| 9 | Métricas | **Macro F1 declarado explicitamente:** *"with **macro averaging** applied uniformly across all 21 classes to avoid metric inflation"*. Também acurácia, precisão, recall, MDR, FAR, IAR, atraso de detecção, RSI. **Sem MCC** | ⚠️ |
| 10 | Resultados | **Sample-level: macro F1 = 0,8823, acurácia 87,81%.** **Run-level: macro F1 = 0,9515, acurácia 95,36%.** Framework hierárquico: 0,9585 | ✅ |
| 11 | Repetições | **5 sementes {42, 123, 2024, 7, 555}** → macro F1 run-level **0,9522 ± 0,0035 (IC 95%: ±0,0044)**, via distribuição t. Teste t pareado, p = 0,038 | ✅ |
| 12 | Reprodutibilidade | Hardware: **i7-10750H, RTX 2060, CUDA 12.9**. Inferência: **6,16 ms (CPU)**. Tamanho: **19,61 MB**. Semente `random_state=42`. **Código apenas sob solicitação ao autor** | ⚠️ |

## ★★★ Três achados que validam decisões que já tínhamos tomado

**1. Eles subamostraram os runs — exatamente como recomendamos.**

Tabela 3 do artigo: do pool de 500 runs por classe, usaram **200 para treino** e **200 para
teste**, com 50 índices temporais por run. Nossa proposta de 100 runs/classe está na mesma
ordem de grandeza, e agora tem precedente publicado num artigo que usa a mesma base.

**2. Eles excluíram o SVM com kernel RBF por custo computacional.**

Literal: o SVM RBF foi *"deliberadamente excluído"* pelo custo em ~2×10⁵ amostras × 312
dimensões. É a mesma conclusão a que chegamos por medição direta — e agora ela tem respaldo
na literatura, não só no nosso benchmark de máquina.

**3. Eles limitaram a profundidade do Random Forest.**

Baseline declarado: `300 estimadores, max_depth=15, min_samples_leaf=3, class_weight
balanceado`. Confirma que o controle de crescimento das árvores é prática necessária nessa
escala, não remendo nosso.

## ★★★ E aqui está a lacuna que define o nosso artigo

> **Os autores afirmam que o XGBoost superou os baselines Random Forest e SVM linear — mas
> NÃO PUBLICAM NENHUM NÚMERO desses baselines.**

Verificação exaustiva das 12 tabelas e do corpo do texto: os hiperparâmetros de RF e SVM
estão declarados (Seção 2.6.2), a conclusão afirma qualitativamente que *"The evaluated
XGBoost classifier exceeded the random forest and linear support vector machine baselines"*,
e **não há uma única célula com F1 ou acurácia desses dois modelos**.

Some-se a isso: **nenhum trabalho do corpus reporta MCC**, e os baselines RF/SVM
*"were not separately tuned on the validation subset"* — ou seja, mesmo que os números
existissem, seriam de modelos não ajustados.

**Isso é precisamente o vão que o WP1A preenche:** seis famílias clássicas, mesmo protocolo,
todas ajustadas na validação, com F1 macro **e MCC**, e custo computacional reportado.

## Ressalvas de escopo — a registrar no artigo

| # | Divergência | Consequência |
|---|---|---|
| 1 | **312 features engenheiradas**, não 52 variáveis brutas | Um benchmark sobre amostras instantâneas de 52 variáveis não compara diretamente com 0,9515 |
| 2 | **Duas granularidades** | Para comparação sample-level o valor correto é **0,8823**, não 0,9515. Os próprios autores advertem: *"direct numerical ranking across studies would be misleading"* |
| 3 | Sem MCC | Comparação nessa métrica é impossível |
| 4 | Conjunto de runs de treino **não variou** entre sementes | A dispersão de ±0,0035 mede menos variabilidade do que pareceria |
| 5 | Código apenas sob solicitação | Não verificável independentemente |

---

## 6. ZHANG, Y.; LUO, L.; JI, X.; DAI, Y. (2021) — *Sensors* 21(20):6715

**"Improved Random Forest Algorithm Based on Decision Paths..."** · DOI 10.3390/s21206715
Texto completo obtido via PMC8538123.

| # | Parâmetro | O que o artigo declara |
|---|---|---|
| 1 | Versão/origem da base | **MIT/Braatz**, com link: *"http://web.mit.edu/braatzgroup/links.html"*. **Não é Rieth** |
| 2 | Variáveis | **52** (41 medidas + 11 manipuladas), **sem seleção de atributos** — matriz de teste D₁₆.₈₀₀ₓ₅₂ |
| 3 | Classes | **21 falhas, IDV(1) a IDV(21)** — inclui IDV21, que **não existe no dataset Rieth**. Tratamento da classe normal: **não informado no artigo** |
| 4 | Divisão | Arquivos Training/Testing prontos do MIT/Braatz. **Validação separada: não informado no artigo.** k-fold: **não informado** |
| 5 | **Unidade de divisão** | **não informado no artigo.** Trabalha sobre matriz de amostras; os termos "run"/"simulation run" nunca aparecem como unidade |
| 6 | Vazamento | **não informado no artigo.** O único tipo de contaminação tratado é injeção artificial de valores ausentes no teste |
| 7 | Pré-processamento | Normalização: **não informado no artigo**. Janelamento: **não informado**. Balanceamento: **não informado**. Imputação pela média para os ausentes injetados |
| 8 | Modelos e hiperparâmetros | RF/DPRF (voto rígido e suave), BP, DBN, RBF. **Hiperparâmetros do experimento TEP: NÃO INFORMADOS para nenhum dos sete algoritmos.** Os únicos valores (50 árvores, folha mínima 5) referem-se ao exemplo didático com o dataset *iris* |
| 9 | Métricas | **OACC e LACC** — acurácias por rótulo. **OACC é macro-média de acurácias one-vs-rest**, não acurácia global. **Sem F1, sem MCC**, sem precisão/revocação isoladas |
| 10 | Resultados | **OACC = 0,6607** (voto suave, sem ausentes) e 0,6564 (rígido). Com 40% de ausentes: DPRF_soft 0,5199 |
| 11 | Repetições | **não informado no artigo.** Sem sementes, k-fold, desvio ou teste. Todos os valores pontuais |
| 12 | Reprodutibilidade | Código: **não disponível**. *Data Availability:* "available on request due to restrictions" — incoerente, já que o dataset é público. Software, hardware, tempos, tamanho: **não informados** |

### ⚠️ Correção à nossa leitura anterior

Na tabela mestra este trabalho constava como *"OACC 66,07% — patamar realista de RF no TEP"*.
A leitura completa mostra que **OACC não é acurácia no sentido usual**: é a média aritmética
de acurácias binárias one-vs-rest (Eqs. 13-14), e cada LACC embute os verdadeiros negativos
das outras 20 classes — o que **infla sistematicamente** o valor num problema multiclasse.

Se citado, exige nota de rodapé com a definição. **Não pode ser apresentado como F1 macro nem
comparado ao nosso número.**

### Veredito: **NÃO COMPARÁVEL**

Dataset Braatz (trajetória única, sem múltiplos runs), unidade de divisão não declarada,
métricas não conversíveis para F1 macro, IDV21 inexistente no Rieth, hiperparâmetros do
experimento não declarados, sem repetições, sem código.

---

# 🔴 7. REZGUI, W.; REZKI, N.; KERROUCHI, S. (2024) — ARTIGO RETIRADO DO PERIÓDICO

**"Predicting and monitoring faults... a case study on the Tennessee Eastman Process"**
*Studies in Engineering and Exact Sciences*, v.5, n.2, e10710 · DOI 10.54021/seesv5n2-541

## ⚠️ Este trabalho foi REMOVIDO e não pode ser citado

Evidências levantadas:

| Evidência | Situação |
|---|---|
| URL primária registrada no Crossref | **HTTP 404** |
| PDF (`/article/download/10710/6078`) | **HTTP 404** |
| DOI `10.54021/seesv5n2-541` | resolve para página 404 |
| **OAI-PMH do próprio periódico** | `<header status="deleted">` · datestamp **2025-02-25** |
| Sumário do fascículo v.5 n.2 (827 artigos) | **não contém o artigo** |
| Wayback Machine · DOAJ · fatcat · scholar.archive.org | **sem cópia** |
| OpenAlex | lista `is_oa: true`, mas `oa_url` aponta para o DOI quebrado |

**O artigo foi retirado do repositório em 25/02/2025.** Todos os 12 itens ficam em
*"não acessado — apenas resumo disponível"*.

## Segunda razão, independente: é REGRESSÃO, não classificação

Confirmado pelo resumo: *"MSE for regression through re-substitution, MSE for regression loss
in cross-validation"*. Os quatro modelos são regressores (SVR, GPR, DTR, LSBoost) e o objetivo
é *"predicting operational parameters"*.

**Não existe conversão legítima entre MSE de predição de parâmetro e F1 macro de diagnóstico
de falha.** Não são o mesmo problema.

Agravante metodológico visível já no resumo: a métrica destacada é **MSE por re-substituição**
— avaliação no próprio conjunto de treino.

## Veredito: **NÃO COMPARÁVEL** — e **removido do nosso corpus**

⚠️ **Correção obrigatória:** este trabalho constava na nossa tabela mestra (ref. #11) como
*"um dos pouquíssimos que trata custo computacional como critério explícito"*. Aquela
descrição veio do resumo. O texto completo **não existe mais publicamente**, e a tarefa é
regressão. **Não pode ser citado no artigo, em hipótese alguma.**

---

# ◐ 8. LYU, N. et al. (2026) — ChemRxiv preprint

**"Benchmarking Machine Learning Fault Detection Methods on the Tennessee Eastman Process Dataset"** · DOI 10.26434/chemrxiv.10001628/v1
PDF completo obtido (37 páginas).

## ◐ VEREDITO: **PARCIALMENTE COMPARÁVEL**

> 🔴 **Preprint sem revisão por pares.** Carimbado em todas as páginas do PDF:
> *"This is a preprint and has not been peer reviewed. Data may be preliminary."*

| # | Parâmetro | O que o artigo declara | Alinha? |
|---|---|---|---|
| 1 | Base | **Rieth et al., Harvard Dataverse** — *"the enriched TEP dataset developed by Rieth et al."*. Mais um segundo dataset via simulador `tep-sim` para avaliação independente | ✅ |
| 2 | Variáveis | **52** (11 manipuladas + 41 medidas). Sem seleção de atributos | ✅ |
| 3 | Classes | **18 = normal + 17 falhas.** *"excluding faults IDV3, IDV9, and IDV15 due to their minimal deviation from normal process behavior"* | ❌ |
| 4 | Divisão | **100 runs/classe treino** (864.000 amostras) · **50 validação** (432.000) · **200 teste** (2.880.000) | ✅ |
| 5 | **Unidade de divisão** | **POR RUN, em quatro passagens:** *"windows were generated independently within each simulation run to prevent temporal information leakage"*; *"sampled by complete simulation runs to preserve temporal structure"* | ✅ |
| 6 | Vazamento | Tratado em **quatro** mecanismos: normalização, janelamento, amostragem do tuning, reset do filtro HMM | ✅ |
| 7 | Pré-processamento | z-score **só com parâmetros do treino** — *"This prevents data leakage from the hold-out sets"*. Janela deslizante stride 1, comprimento otimizado (38-40 passos). Classes balanceadas por construção amostral | ✅ |
| 8 | Modelos e hiperparâmetros | 7 arquiteturas. **Busca bayesiana com Optuna/TPE, 50 trials.** Todos os hiperparâmetros ótimos publicados. XGBoost: `n_estimators=499, max_depth=6, lr=0.196, subsample=0.967, colsample_bytree=0.841, min_child_weight=8, gamma=0.564, reg_alpha=0.329, reg_lambda=0.063` | ✅ |
| 9 | Métricas | Acurácia, acurácia balanceada, precisão, recall, F1. **Declaração decisiva:** *"Because our datasets are perfectly balanced across all 18 classes, the weighted and macro F1 scores are equivalent"*. **Sem MCC** | ⚠️ |
| 10 | Resultados | **XGBoost: acc 93,91% · F1 0,9416.** LSTM-FCN 99,37% · CNN-Transformer 99,20% · LSTM 99,14% · TransKal 99,09% | ✅ |
| 11 | Repetições | **não informado no artigo.** Sem sementes de treino, k-fold, desvio ou teste. Os autores admitem: *"the differences are more subtle and may not be significant"* | ❌ |
| 12 | Reprodutibilidade | ★ **Código, pesos treinados e datasets pré-processados públicos:** `github.com/KitchinHUB/tep-manuscript`. Tempos de treino e tuning reportados. Hardware e versões: **não informados** | ✅ |

### ★ O achado mais valioso deste trabalho — e ele é negativo sobre o próprio TEP

Correção à nossa leitura anterior: o artigo **não** mostra que os 99% caem por vazamento entre
partições. Mostra algo mais interessante — que **não sobrevivem a um gerador independente**.

Os mesmos pesos treinados, **sem retreino nem recalibração**, foram avaliados em dados gerados
por outro simulador com sementes distintas:

| Modelo | Original | Independente | Variação |
|---|---|---|---|
| CNN-Transformer | 99,20% | **99,57%** | **+0,38%** |
| LSTM-FCN | 99,37% | 98,93% | −0,44% |
| XGBoost | 93,91% | 89,40% | −4,51% |
| TransKal | 99,09% | **87,57%** | **−11,52%** |
| Conv-Autoencoder | 99,39% | **76,04%** | **−23,35%** |

O colapso concentra-se nos modelos com **parâmetros calibrados fixos** (limiar de autoencoder,
ruído de Kalman) — no Conv-AE a ROC-AUC permaneceu em 0,981: *"the failure lies in the
threshold calibration."*

E a conclusão dos autores contra o próprio benchmark:

> *"It does not appear that this dataset is useful for benchmarking deep learning models as
> many of them achieve similar high performance."*

**Uso para o nosso artigo:** é o argumento mais forte disponível a favor de reportar métodos
clássicos com custo computacional, em vez de perseguir a terceira casa decimal de acurácia
com arquiteturas profundas.

### Divergências que impedem "COMPARÁVEL"

1. **18 classes, não 21** — e as três removidas (IDV3, IDV9, IDV15) são exatamente as difíceis.
   Um F1 macro sobre 18 classes fáceis não é confrontável com F1 macro sobre 21.
2. **Sem MCC.**
3. **Sem repetições, sementes ou teste estatístico.**
4. **Preprint** — sem revisão por pares.
5. Dataset **balanceado artificialmente** por amostragem, ao contrário do perfil natural.

---

# ◐ 9. AVANASHILINGAM, J. B.; PANDIYATH VELAYUDHAN, B. (2026) — PHMAP

**"Explainable and Trustworthy AI for Fault Classification in the Tennessee Eastman Process"** · DOI 10.36001/phmap.2025.v5i1.4633
PDF completo obtido. Conferência com revisão por pares · autores da Yokogawa Engineering Asia.

## ◐ VEREDITO: **PARCIALMENTE COMPARÁVEL**

| # | Parâmetro | O que o artigo declara | Alinha? |
|---|---|---|---|
| 1 | Base | **Rieth / Harvard Dataverse.** Confirma a estrutura: *"faultNumber... simulationRun indicating the simulation seed (1–500 for training, non-overlapping with testing)... sampled every 3 minutes"* | ✅ |
| 2 | Variáveis | ⚠️ **Declara 53 = 41 XMEAS + 12 XMV** (`xmv_1` a `xmv_12`), não 52. Divergência textual **não resolvida pelo artigo** | ❌ |
| 3 | Classes | **21 = normal + IDV1-20.** **Nenhuma excluída** — mantém IDV3, 9 e 15 | ✅ |
| 4 | Divisão | K-fold estratificado com **K=5** dentro do treino. **Proporções: não informado no artigo** | ⚠️ |
| 5 | **Unidade de divisão** | **POR RUN, declarado:** *"Leakage-safe evaluation was ensured by partitioning datasets strictly according to simulationRun identifiers, thereby preventing cross-run contamination"* | ✅ |
| 6 | Vazamento | Tratado explicitamente; a CV é justificada como diagnóstico: *"identify potential overfitting or leakage artifacts"* | ✅ |
| 7 | Pré-processamento | Filtro Hodrick-Prescott (tendência + ciclo). Janelas de **60 amostras com 10 de sobreposição**, por run. **Normalização: não informado no artigo.** **Balanceamento: não informado** | ⚠️ |
| 8 | Modelos e hiperparâmetros | LightGBM em dois ramos, fusão por média das probabilidades. SHAP. **Hiperparâmetros: não informado — e a omissão é declarada:** *"The detailed description of this framework is considered beyond the scope of the present work"* | ❌ |
| 9 | Métricas | **Acurácia, F1 macro, AUC-ROC macro e micro.** **Sem MCC** | ⚠️ |
| 10 | Resultados | **Baseline LightGBM: acc 93,19% · F1 macro 0,9283.** **Dual-branch: acc 94,56% · F1 macro 0,9424.** Ganho médio 4,34% em 7 de 21 falhas | ✅ |
| 11 | Repetições | Só K=5. **Sem desvio entre folds, sem teste estatístico** — para uma diferença de 1,37 p.p. | ❌ |
| 12 | Reprodutibilidade | Código, versões, hardware, tempos, tamanho: **todos não informados no artigo** | ❌ |

### Divergências que impedem "COMPARÁVEL"

1. **53 variáveis declaradas contra 52** — sem saber qual coluna extra entrou, a matriz de
   entrada não é demonstravelmente a mesma.
2. **Unidade de exemplo diferente:** janelas agregadas de 60 amostras com sobreposição de 10,
   não amostras individuais. F1 macro por janela ≠ F1 macro por amostra.
3. **Sem MCC**, sem hiperparâmetros, sem dispersão, sem código.

**Uso recomendado:** os valores 93,19%/0,9283 e 94,56%/0,9424 podem entrar na tabela
comparativa **com nota de rodapé** registrando as 53 variáveis declaradas, as janelas de 60
amostras e a ausência de MCC e dispersão.
