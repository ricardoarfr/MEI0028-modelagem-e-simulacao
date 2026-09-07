# Busca dirigida — trabalhos que usam o dataset Rieth com métodos clássicos

**Método:** busca em texto completo no OpenAlex pelos marcadores distintivos do dataset
(`6C3JR1`, `simulationRun`, `faultNumber`, `TEP_Faulty_Training`), varredura das 101 obras
que citam o dataset e das 31 que citam o artigo AHFE de Rieth et al., mais Crossref,
DataCite, Europe PMC, Unpaywall e Semantic Scholar. PDFs baixados e inspecionados quando
acessíveis. **11/11 DOIs confirmados no Crossref.**

**Resultado do recorte:** apenas **5 trabalhos revisados por pares** usam o dataset Rieth com
métodos clássicos, e só 4 em tarefa multiclasse. O nicho é genuinamente escasso — a
esmagadora maioria dos ~101 artigos que citam o dataset usa deep learning.

---

## ★★★ CORREÇÃO IMPORTANTE À NOSSA ANÁLISE ANTERIOR

Eu havia afirmado que **"não há um único valor publicado de Random Forest, SVM, Regressão
Logística, Árvore de Decisão ou Gradient Boosting sob protocolo comparável"**.

**Isso estava incorreto.** Existe — e é justamente o trabalho que faltava.

### SOKOLOV, A. N.; PYATNITSKY, I. A.; ALABUGIN, S. K. (2019)

**"Applying methods of machine learning in the task of intrusion detection based on the
analysis of industrial process state and ICS networking"**
*FME Transactions*, 47(4), p. 782-789 · DOI 10.5937/fmet1904782s · acesso aberto

Usa o **dataset Rieth completo** (>15 milhões de registros), **21 classes**, e publica
acurácia de **sete métodos clássicos** lado a lado:

| Modelo | Acurácia |
|---|---|
| Árvore de Decisão | **0,23** |
| AdaBoost | 0,34 |
| Regressão Logística | 0,46 |
| Lasso | 0,46 |
| Gradient Boosting | 0,46 |
| SVM | 0,57 |
| **Random Forest** | **0,67** |
| Rede densa (FCNN) | 0,82 |

Evidência do dataset (Seção 3): *"Additional Tennessee Eastman Process Simulation Data for
Anomaly Detection Evaluation [18] is a modified version of the classical dataset"*, com
referência [18] = Rieth et al. e menção a *"5.000.000 records"* de treino.

### Por que este achado é bom para o artigo, e não ruim

Os valores são **muito mais baixos** que os 0,88-0,95 dos trabalhos com boosting e features
engenheiradas. Isso estabelece um **patamar realista** dos métodos clássicos sobre variáveis
brutas no Rieth com 21 classes — e diz que, se nossos resultados ficarem entre 0,5 e 0,7,
isso é o esperado, não fracasso.

### Ressalvas que impedem "COMPARÁVEL"

| # | Divergência |
|---|---|
| 1 | Métrica é **acurácia**, não F1 macro nem MCC |
| 2 | **Não há divisão por run** — usa os arquivos de treino/teste como vieram |
| 3 | O próprio artigo observa que o dataset *"turned out to be highly subject to overtraining"* |
| 4 | Hiperparâmetros e repetições: não verificados |

**Veredito: PARCIALMENTE COMPARÁVEL** — utilizável como referência de patamar, com a métrica
qualificada.

---

## Demais confirmados — Rieth + métodos clássicos

| # | Autores | Ano | Veículo | DOI | Modelos clássicos | Divisão por run? |
|---|---|---|---|---|---|---|
| 1 | PETER, M. J. et al. (21 autores) | 2024 | ML4CCE Workshop @ ECML PKDD | ⚠️ **sem DOI** | XGBoost, RF, SVM vs. LSTM-FCN, DeepCNN, TCN, RNN, WaveNet | ✗ arquivos originais |
| 2 | SOKOLOV et al. | 2019 | FME Transactions 47(4) | 10.5937/fmet1904782s | LR, Lasso, SVM, DT, AdaBoost, GB, RF | ✗ arquivos originais |
| 3 | SOKOLOV et al. | 2018 | GloSIC (IEEE) | 10.1109/glosic.2018.8570073 | "classical ML methods" — **não verificado** (paywall) | não verificado |
| 4 | ÇANCIOĞLU, E.; ŞAHIN, S.; İŞLER, Y. | 2021 | European Journal of Science and Technology | 10.31590/ejosat.952761 | Boosted/Bagged/RUSBoosted Trees, Subspace Discriminant, Subspace KNN | ✗ **split aleatório** |
| 5 | MIRALIAKBAR, A.; JIANG, Z. | 2024 | Systems and Control Transactions 3 | 10.69997/sct.184473 | SVM modificado, ridge classifier, PGA | ✗ **10-fold sobre amostras** |
| 6 | KHAN, A. et al. | 2026 | Scientific Reports 16 | 10.1038/s41598-026-48227-6 | LR, SVM, RF, LightGBM (baselines) | ✅ **"run level 70/20/10 split"** |

### ★ Notas sobre os mais relevantes

**PETER et al. (2024)** — o benchmark mais próximo do nosso recorte: XGBoost, RF e SVM contra
seis arquiteturas profundas, 20 falhas do Rieth, 27 combinações de método × redução de
dimensionalidade, ranqueadas por F1. Conclusão: LSTM-FCN em 1º com F1 0,98; clássicos
*"competitivos mas geralmente superados"*.
⚠️ **Sem DOI** — anais de workshop, sem registro no Crossref ou dblp. Citável como anais, com
essa ressalva. PDF: `ml4cce-ecml.com/papers/177.pdf`

**KHAN et al. (2026)** — o **único** trabalho localizado, em toda a busca, que declara
divisão em nível de execução: *"On a run level 70/20/10 split of Tennessee Eastman Process
runs"*. A tarefa é **binária** (normal vs. todas as falhas agrupadas), portanto não serve como
referência de desempenho multiclasse — mas é a melhor citação disponível para **fundamentar
metodologicamente** a divisão por `simulationRun`.
⚠️ Cita Downs & Vogel e o arquivo de Ricker, **não cita Rieth** — a atribuição do dataset é
inferência do agente a partir da Tabela 1 (500 runs, `faultNumber` 0..21). Registrar como
*versão do dataset não confirmada pelos autores*.

**ÇANCIOĞLU et al. (2021)** — descreve explicitamente as colunas do Rieth (`faultNumber` 0-20,
`sample` 1-500/1-960, 25 h / 48 h, figura com `simulationRun=1`), embora o resumo atribua a
base ao IEEE DataPort (que hospeda um espelho). Melhor resultado: Subspace Discriminant 89,5%.
Publicado em turco, com resumo em inglês.

---

## Contraste — versão Braatz ou simulação própria

| Autores | Ano | Veículo | DOI | Observação |
|---|---|---|---|---|
| GONZALEZ-ARCE, E. | 2023 | Journal of Engineering Research (Atena, **brasileiro**) | 10.22533/at.ed.3173332325091 | **RF, SVM-RBF e Regressão Logística** multiclasse — mesmos modelos, mas base gerada pelo autor (40 runs, 480.040 linhas). Útil como referência de **estilo e escopo** para veículo brasileiro |
| BASHA, N. et al. | 2020 | Computers & Chemical Engineering 136 | 10.1016/j.compchemeng.2020.106786 | Multiclasse no TEP contra DNNs. **Versão do dataset não confirmada** — sem acesso aberto |

---

## Rieth confirmado, mas sem clássicos como classificador principal

Úteis para caracterizar o dataset, não para comparar desempenho.

| Autores | Ano | DOI | O que faz |
|---|---|---|---|
| BOLBOACĂ, R.; HALLER, P.; GENGE, B. | 2024 | 10.1007/s00521-024-10551-1 | Ensemble LSTM + CUSUM, detecção binária. RF só como seletor de atributos. **Link explícito ao DOI do Rieth** |
| DZAFERAGIC, M.; MARCHETTI, N.; MACALUSO, I. | 2022 | 10.1109/jiot.2021.3116785 | Multiclasse com DNN. Exclui falha 21 *"since it was not part of the extended data set"* — **confirma que o Rieth tem 20 falhas** |
| ZHANG, Z. et al. | 2025 | 10.3390/e27020181 | Vision Transformer. Nenhum baseline clássico |
| YUSUPOVA, N. et al. | 2020 | 10.2991/aisr.k.201029.026 | LSTM multiclasse. Descreve as colunas do Rieth |

---

## Não confirmadas — não citar sem leitura

| Obra | Situação |
|---|---|
| PERALES GÓMEZ et al. (2023), *IET Information Security*, 10.1049/ise2.12115 | Índice de texto completo casa Rieth + XGBoost, mas Wiley bloqueado. **Versão do dataset não confirmada** |
| PERALES GÓMEZ et al. (2022), *IEEE Access*, 10.1109/access.2022.3224930 | Idem — PDF inacessível |
| LEONI, J. et al. (2023), *Eng. Appl. of AI*, 10.1016/j.engappai.2023.107510 | Casa `6C3JR1` + RF + SVM + LR, mas ScienceDirect retornou 403 |
| MILLOT, B. et al. (2021), IEEE CSR | Fechado, sem cópia OA |
| KAUSAR, M. A. (2025), *Int. Journal of Computer Applications* | ⚠️ **Não citar** — veículo de reputação editorial fraca, e PDF não obtido |

---

## Conclusão metodológica desta busca

Dos seis trabalhos confirmados que usam Rieth com métodos clássicos, **apenas um
(Khan et al., 2026) declara divisão por execução — e sua tarefa é binária.**

Peter et al., Sokolov et al., Çancıoğlu et al. e Miraliakbar & Jiang usam os arquivos
originais de treino/teste ou validação cruzada *k*-fold sobre amostras individuais, **sem
agrupar por `simulationRun`**. Nenhum deles discute a questão.

> **Isto é um argumento defensável e verificável para o artigo:** a literatura que usa o
> dataset Rieth com métodos clássicos majoritariamente não controla a dependência entre
> amostras da mesma execução, e nenhum dos trabalhos localizados discute explicitamente esse
> ponto.
