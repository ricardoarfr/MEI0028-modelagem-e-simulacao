# Tabela mestra de referências — artigo WP1A / Sodebras

**Última atualização:** 2026-09-05
**Verificação de metadados:** Crossref API, consulta direta por DOI, executada nesta sessão.
Cada DOI abaixo retornou autores, ano, veículo e título coincidentes com o registrado.

## Legenda de status

| Símbolo | Significado |
|---|---|
| **M✅** | Metadados verificados (autores, ano, veículo, título, DOI resolvido no Crossref) |
| **C✅** | Conteúdo verificado — valores numéricos citados foram efetivamente vistos |
| **C⚠️** | Conteúdo parcial — só o resumo foi acessado; valores adicionais não verificados |
| **C❌** | Conteúdo não verificado — apenas metadados bibliográficos confirmados |

**Regra:** uma referência com **C❌** pode ser citada para posicionamento temático, mas
**nenhum número dela pode aparecer no nosso texto** sem abrir o artigo completo antes.

---

## Eixo E1 — TEP + aprendizado de máquina clássico (2021–2026)

| # | Autores | Ano | Título | Veículo | DOI | Status | Relevância para o WP1A | Onde citar |
|---|---|---|---|---|---|---|---|---|
| 1 | KOÇAK, N. F.; SAYGIN, A.; TÜRK, F.; KARADENIZ, A. M. | 2026 | Run-Level Fault Detection and SHAP-Based Diagnosis of Persistent Classification Difficulty in the Tennessee Eastman Process | Processes | 10.3390/pr14162569 | M✅ C⚠️ | **Referência mais próxima do nosso desenho.** Único trabalho localizado que agrega predições em decisão **por execução (run-level)**; XGBoost, 21 condições, F1 macro = 0,9515 | Referencial · Metodologia · Discussão |
| 2 | LYU, N. et al. | 2026 | Benchmarking Machine Learning Fault Detection Methods on the Tennessee Eastman Process Dataset | ChemRxiv (preprint) | 10.26434/chemrxiv.10001628/v1 | M✅ C✅ | ◐ **PARCIALMENTE COMPARÁVEL** — Rieth, 52 vars, **divisão por run**, F1 macro. Mas **18 classes** (exclui IDV3/9/15) e sem MCC. **Código e pesos públicos:** github.com/KitchinHUB/tep-manuscript. XGBoost: acc 93,91% / F1 0,9416 | Introdução · Discussão |
| 3 | ZHANG, Y.; LUO, L.; JI, X.; DAI, Y. | 2021 | Improved Random Forest Algorithm Based on Decision Paths for Fault Diagnosis of Chemical Process with Incomplete Data | Sensors, 21(20):6715 | 10.3390/s21206715 | M✅ C✅ | **Patamar realista de RF no TEP 21 classes / 52 variáveis: OACC 66,07%.** Contraponto aos 99% frequentemente relatados | Referencial · Resultados |
| 4 | HU, M.; HU, X.; DENG, Z.; TU, B. | 2022 | Fault Diagnosis of Tennessee Eastman Process with XGB-AVSSA-KELM Algorithm | Energies | 10.3390/en15093198 | M✅ C⚠️ | ⚠️ **CORRIGIDO:** origem da base **não declarada**; XGBoost usado só como **seletor**, não classificador; "FDR" é **acurácia** renomeada; **dados fabricados** na tabela comparativa. Ver `05-TABELA-COMPARABILIDADE.md` | Referencial · Resultados |
| 5 | REINARTZ, C.; KULAHCI, M.; RAVN, O. | 2021 | An extended Tennessee Eastman simulation dataset for fault-detection and decision support systems | Computers & Chemical Engineering | 10.1016/j.compchemeng.2021.107281 | M✅ C⚠️ | Dataset estendido com **simulações repetidas**, seis modos de produção, múltiplas magnitudes — base para justificar divisão por execução | Metodologia |
| 6 | NASIF, S.; TASNIM, A.; SANZIDA, N. | 2026 | Enhanced fault detection in the Tennessee Eastman Process using Mahalanobis distance based maximum likelihood estimation | Chemical Product and Process Modeling | 10.1515/cppm-2025-0291 | M✅ C✅ | Score médio de detecção 74,1%; 79,4% na IDV19, onde PCA falha. Útil na discussão de **falhas difíceis** | Referencial · Resultados |
| 7 | LI, D. et al. | 2026 | An evolutionary weighted feature influence factor feature selection method for fault detection in the Tennessee Eastman complex chemical process | Scientific Reports | 10.1038/s41598-026-49874-5 | M✅ C✅ | ⚠️ **CORRIGIDO após leitura do texto completo:** dataset **Braatz**, não Rieth; **21 detectores binários**, não multiclasse; divisão **por amostra com embaralhamento aleatório**. O F1 de 0,9579 é média de F1 **binários** — não comparável a F1 macro. Ver `05-TABELA-COMPARABILIDADE.md` | Referencial · Metodologia · Discussão |
| 8 | MELO, A.; CÂMARA, M. M.; PINTO, J. C. | 2024 | Data-Driven Process Monitoring and Fault Diagnosis: A Comprehensive Survey | Processes, 12(2):251 | 10.3390/pr12020251 | M✅ C⚠️ | Survey de enquadramento: estatística multivariada vs. ML; discute disponibilidade de benchmarks | Introdução · Referencial |
| 9 | LEITE, D.; ANDRADE, E.; RÁTIVA, D.; MACIEL, A. M. A. | 2024 | Fault Detection and Diagnosis in Industry 4.0: A Review on Challenges and Opportunities | Sensors, 25(1):60 | 10.3390/s25010060 | M✅ C✅ | Revisão sistemática (805 → 29 estudos). **Recomenda explicitamente datasets padronizados, tratamento de desbalanceamento e XAI** — sustenta a motivação do WP1A | Introdução · Discussão |
| 10 | POZDNYAKOV, V. et al. | 2024 | Adversarial Attacks and Defenses in Fault Detection and Diagnosis: A Comprehensive Benchmark on the Tennessee Eastman Process | IEEE Open Journal of the Industrial Electronics Society | 10.1109/OJIES.2024.3401396 | M✅ C❌ | Fragilidade de redes neurais no TEP sob perturbação — argumento de robustez a favor de modelos clássicos | Discussão |
| 11 | REZGUI, W.; REZKI, N.; KERROUCHI, S. | 2024 | Predicting and monitoring faults in intricate processes through the utilization of an ensemble of machine learning regression models: a case study on the Tennessee Eastman Process | Studies in Engineering and Exact Sciences | 10.54021/seesv5n2-541 | 🔴 **RETIRADO** | ⚠️⚠️ **ARTIGO REMOVIDO DO PERIÓDICO** em 25/02/2025 (registro OAI `status="deleted"`, DOI 404, sem cópia em Wayback/DOAJ). Além disso é **regressão**, não classificação. **NÃO CITAR EM HIPÓTESE ALGUMA** | ❌ removido do corpus |
| 12 | XU, H.; REN, T.; MO, Z.; YANG, X. | 2022 | A Fault Diagnosis Model for Tennessee Eastman Processes Based on Feature Selection and Probabilistic Neural Network | Applied Sciences, 12(17):8868 | 10.3390/app12178868 | M✅ C❌ | ⚠️ **CORRIGIDO:** dataset **Braatz/MIT**; reduz a **5 variáveis por falha**; avaliação **binária N vs. F**; SVM baseline **colapsado** (0,00 no normal em 14 de 21 categorias). Ver `05-TABELA-COMPARABILIDADE.md` | Referencial · Metodologia |
| 13 | MÁRQUEZ-VERA, M. A. et al. | 2026 | A Wavelet-Based Evolving Fuzzy Framework for Fault Diagnosis in the Tennessee Eastman Process | Algorithms, 19(6):485 | 10.3390/a19060485 | M✅ C✅ | ⚠️ **CORRIGIDO:** **simulação própria** (nem Rieth nem Braatz), 7 variáveis, 10 falhas one-vs-rest, divisão temporal na mesma run, e contradições numéricas internas. Ver `05-TABELA-COMPARABILIDADE.md` | Discussão · Resultados |
| 14 | AVANASHILINGAM, J. B.; VELAYUDHAN, B. P. | 2026 | Explainable and Trustworthy AI for Fault Classification in the Tennessee Eastman Process: A Step Toward Industrial Autonomy | PHM Society Asia-Pacific Conference | 10.36001/phmap.2025.v5i1.4633 | M✅ C✅ | ◐ **PARCIALMENTE COMPARÁVEL** — Rieth, **21 classes**, **divisão por run**, F1 macro. Mas declara **53 variáveis** e usa janelas de 60. LightGBM baseline: acc 93,19% / F1 macro 0,9283 | Referencial · Discussão |
| 15 | LOMOV, I.; LYUBIMOV, M.; MAKAROV, I.; ZHUKOV, L. E. | 2021 | Fault detection in Tennessee Eastman process with temporal deep learning models | Journal of Industrial Information Integration | 10.1016/j.jii.2021.100216 | M✅ C❌ | Contraste clássico vs. profundo. **Não citar número algum sem abrir o artigo** | Referencial |

### Notas de cautela do eixo E1

- **#2 é preprint** (ChemRxiv), não revisado por pares. Usar com a ressalva explícita, ou
  substituir se sair a versão publicada.
- **#10, #12 e #15 estão em C❌** — só metadados. São citáveis para posicionamento, mas
  nenhum valor numérico deles pode entrar no texto.
- **Anos 2026** são consistentes com a data corrente (setembro de 2026) e foram reproduzidos
  exatamente como constam no Crossref, sem ajuste.

---

## Eixo E2 — Fontes canônicas do TEP, datasets e benchmarks

**Verificação:** 16/16 DOIs confirmados no Crossref + 2 DOIs de dataset confirmados no
DataCite. Nenhuma falha. Ficha completa do dataset em `03-FICHA-DATASET-TEP.md`.

### E2.1 — Fontes canônicas e datasets

| # | Autores | Ano | Título | Veículo | DOI | Papel |
|---|---|---|---|---|---|---|
| 54 | DOWNS, J. J.; VOGEL, E. F. | 1993 | A plant-wide industrial process control problem | Computers & Chemical Engineering, 17(3), p. 245-255 | 10.1016/0098-1354(93)80018-I | **Fonte primária do TEP.** Define o processo, as 20 perturbações IDV1-20, 41 medições e 12 válvulas |
| 55 | RIETH, C. A.; AMSEL, B. D.; TRAN, R.; COOK, M. B. | 2017 | Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation | Harvard Dataverse, V1 | 10.7910/DVN/6C3JR1 | **O dataset do WP1A.** 500 runs por classe, 21 classes, 52 variáveis. Domínio público |
| 56 | RIETH, C. A.; AMSEL, B. D.; TRAN, R.; COOK, M. B. | 2017 | Issues and Advances in Anomaly Detection Evaluation for Joint Human-Automated Systems | Advances in Human Factors in Robots and Unmanned Systems, AISC 595, p. 52-63 | 10.1007/978-3-319-60384-1_6 | **Publicação que acompanha o dataset** — cita-se junto com o DOI de dados |
| 57 | CHIANG, L. H.; RUSSELL, E. L.; BRAATZ, R. D. | 2001 | Fault Detection and Diagnosis in Industrial Systems | Springer London, Advanced Textbooks in Control and Signal Processing | 10.1007/978-1-4471-0347-9 | Referência canônica dos métodos clássicos (PCA, PLS, FDA, CVA) sobre o TEP |
| 58 | RUSSELL, E. L.; CHIANG, L. H.; BRAATZ, R. D. | 2000 | Tennessee Eastman Process (cap.) | Data-driven Methods for Fault Detection and Diagnosis in Chemical Processes, p. 99-108 | 10.1007/978-1-4471-0409-4_8 | Origem do protocolo de facto (480 treino / 960 teste, falha na amostra 160) |
| 59 | BATHELT, A.; RICKER, N. L.; JELALI, M. | 2015 | Revision of the Tennessee Eastman Process Model | IFAC-PapersOnLine, 48(8), p. 309-314 | 10.1016/j.ifacol.2015.08.199 | Simulador Matlab/Simulink revisado; corrige a repetibilidade do código original |
| 60 | REINARTZ, C. C.; KULAHCI, M.; RAVN, O. | 2021 | Tennessee Eastman Reference Data for Fault-Detection and Decision Support Systems | DTU Data (Figshare), CC0 | 10.11583/DTU.13385936.v1 | Dataset estendido. **Fora do escopo do tópico 7** — citar como trabalho futuro |

### E2.2 — Benchmarks e análises críticas

| # | Autores | Ano | Título | Veículo | DOI | Papel |
|---|---|---|---|---|---|---|
| 61 | MELO, A.; CÂMARA, M. M.; CLAVIJO, N.; PINTO, J. C. | 2022 | Open benchmarks for assessment of process monitoring and fault diagnosis techniques: A review and critical analysis | Computers & Chemical Engineering, 165 | 10.1016/j.compchemeng.2022.107964 | **A referência mais direta para justificar o WP1A**: análise crítica da falta de comparabilidade entre trabalhos. ⚠️ abstract não lido — ler antes de citar afirmação específica |
| 62 | YIN, S.; DING, S. X.; HAGHANI, A.; HAO, H.; ZHANG, P. | 2012 | A comparison study of basic data-driven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process | Journal of Process Control, 22(9), p. 1567-1581 | 10.1016/j.jprocont.2012.06.009 | **Antecedente direto do WP1A** — o benchmark clássico que este trabalho atualiza. Fora da janela 2021-2026, mas indispensável para posicionamento |
| 63 | BI, X.; QIN, R.; WU, D.; ZHENG, S.; ZHAO, J. | 2022 | One step forward for smart chemical process fault detection and diagnosis | Computers & Chemical Engineering, 164 | 10.1016/j.compchemeng.2022.107884 | Limitações do TEP como benchmark único. ⚠️ abstract não lido |
| 64 | HARTUNG, F.; MURALEEDHARAN, A.; KLOFT, M.; BURGER, J. | 2026 | Beyond Tennessee Eastman: Benchmarking Deep Anomaly Detection on Real-World Pilot-Scale Continuous Distillation Data | Systems and Control Transactions, 6, p. 1728-1736 (ESCAPE-36) | 10.69997/sct.127956 | Crítica à avaliação restrita a benchmarks sintéticos — usar em Ameaças à validade |
| 65 | MONTESUMA, E. F. et al. | 2023 | Benchmarking Domain Adaptation for Chemical Processes on the Tennessee Eastman Process | arXiv:2308.11247 (workshop ECML-PKDD 2024) | 10.48550/arXiv.2308.11247 | ⚠️ **preprint** — marcar como tal |

### E2.3 — Deep learning no TEP (contexto, não escopo)

Usadas apenas para justificar por que uma linha de base clássica ainda é necessária.

| # | Autores | Ano | Título | Veículo | DOI |
|---|---|---|---|---|---|
| 66 | GOLYADKIN, M.; POZDNYAKOV, V.; ZHUKOV, L.; MAKAROV, I. | 2023 | SensorSCAN: Self-supervised learning and deep clustering for fault diagnosis in chemical processes | Artificial Intelligence, 324 | 10.1016/j.artint.2023.104012 |
| 67 | ZHANG, L.; SONG, Z.; ZHANG, Q.; PENG, Z. | 2022 | Generalized transformer in fault diagnosis of Tennessee Eastman process | Neural Computing and Applications, 34(11), p. 8575-8585 | 10.1007/s00521-021-06711-2 |
| 68 | XIAO, Z.; KORDON, A.; SEN, S. | 2023 | Fault Detection and Diagnosis in Tennessee Eastman Process with Deep Autoencoder | Annual Conference of the PHM Society, 15(1) | 10.36001/phmconf.2023.v15i1.3578 |
| 69 | HARTUNG, F.; FRANKS, B. J.; MICHELS, T. et al. | 2023 | Deep Anomaly Detection on Tennessee Eastman Process Data | Chemie Ingenieur Technik, 95(7), p. 1077-1082 | 10.1002/cite.202200238 |
| 70 | KOVALENKO, A.; POZDNYAKOV, V.; MAKAROV, I. | 2024 | Graph Neural Networks With Trainable Adjacency Matrices for Fault Diagnosis on Multivariate Sensor Data | IEEE Access, 12, p. 152860-152872 | 10.1109/ACCESS.2024.3481331 |
| 71 | KAI, T. C. Y. et al. | 2025 | Supervised deep learning algorithms for process fault detection and diagnosis under different temporal subsequence length of process data | Applied Intelligence, 55(12) | 10.1007/s10489-025-06711-y |
| 72 | LI, Y. et al. | 2026 | A lightweight hybrid temporal representation network with gated attention aggregation... : A Tennessee Eastman Process study | Process Safety and Environmental Protection, 213 | 10.1016/j.psep.2026.109022 |

> **#68 (Xiao et al., 2023)** é o mais útil deste bloco: compara autoencoder profundo
> **diretamente com PCA**, ou seja, já faz o confronto DL × clássico que o nosso artigo
> estende para as seis famílias.
> **#72 (Li et al., 2026)** registra que "leveza" virou preocupação em 2026 — reforça o
> valor de baselines baratos.

---

## Eixo E4 — Métricas, vazamento de dados, comparação estatística e reprodutibilidade

**Verificação:** 34/34 DOIs confirmados no Crossref nesta sessão. Nenhuma falha.

### E4.1 — Métricas para classificação multiclasse desbalanceada

| # | Autores | Ano | Título | Veículo | DOI | O que permite afirmar |
|---|---|---|---|---|---|---|
| 16 | CHICCO, D.; JURMAN, G. | 2020 | The advantages of the Matthews correlation coefficient (MCC) over F1 score and accuracy in binary classification evaluation | BMC Genomics, 21(1) | 10.1186/s12864-019-6413-7 | **Citação de base para eleger MCC como métrica principal.** Acurácia e F1 inflacionam em base desbalanceada; MCC só é alto quando as 4 células da matriz são boas |
| 17 | GORODKIN, J. | 2004 | Comparing two K-category assignments by a K-category correlation coefficient | Computational Biology and Chemistry, 28(5-6), p. 367-374 | 10.1016/j.compbiolchem.2004.09.006 | **Obrigatória.** Única fonte que define matematicamente o MCC para K classes. Sem ela, "MCC multiclasse" fica sem lastro formal |
| 18 | CHICCO, D.; TÖTSCH, N.; JURMAN, G. | 2021 | The Matthews correlation coefficient (MCC) is more reliable than balanced accuracy, bookmaker informedness, and markedness... | BioData Mining, 14(1) | 10.1186/s13040-021-00244-z | Justifica por que a acurácia balanceada entra como métrica **secundária**, não principal |
| 19 | BRODERSEN, K. H.; ONG, C. S.; STEPHAN, K. E.; BUHMANN, J. M. | 2010 | The Balanced Accuracy and Its Posterior Distribution | ICPR 2010, p. 3121-3124 | 10.1109/ICPR.2010.764 | Definição da acurácia balanceada e existência de sua distribuição posterior (intervalos de confiança) |
| 20 | SOKOLOVA, M.; LAPALME, G. | 2009 | A systematic analysis of performance measures for classification tasks | Information Processing & Management, 45(4), p. 427-437 | 10.1016/j.ipm.2009.03.002 | Definições formais de macro-média e micro-média; a escolha da métrica altera a conclusão |
| 21 | OPITZ, J. | 2024 | A Closer Look at Classification Evaluation Metrics and a Critical Reflection of Common Evaluation Practice | TACL, 12, p. 820-836 | 10.1162/tacl_a_00675 | Justifica **por escrito** a escolha de F1 macro em vez de F1 ponderada, em vez de só declará-la |
| 22 | CHICCO, D.; WARRENS, M. J.; JURMAN, G. | 2021 | The MCC is More Informative Than Cohen's Kappa and Brier Score... | IEEE Access, 9, p. 78368-78381 | 10.1109/ACCESS.2021.3084050 | Opcional — justifica não reportar kappa nem Brier |
| 23 | CHICCO, D.; JURMAN, G. | 2023 | The MCC should replace the ROC AUC as the standard metric... | BioData Mining, 16(1) | 10.1186/s13040-023-00322-4 | Reserva — se um revisor exigir AUC como critério de ranqueamento |

### E4.2 — Vazamento de dados e validação em dados correlacionados

**Este é o eixo que sustenta a restrição R4/R5 do tópico 7.**

| # | Autores | Ano | Título | Veículo | DOI | O que permite afirmar |
|---|---|---|---|---|---|---|
| 24 | WHEAT, L.; MOHRENSCHILDT, M. V.; HABIBI, S.; AL-ANI, D. | 2024 | Impact of Data Leakage in Vibration Signals Used for Bearing Fault Diagnosis | IEEE Access, 12, p. 169879-169895 | 10.1109/ACCESS.2024.3497716 | **Maior peso retórico.** Vazamento demonstrado no próprio domínio de diagnóstico de falhas: métodos de divisão diferentes produzem desempenhos radicalmente diferentes |
| 25 | SAEB, S.; LONINI, L.; JAYARAMAN, A.; MOHR, D. C.; KORDING, K. P. | 2017 | The need to approximate the use-case in clinical machine learning | GigaScience, 6(5) | 10.1093/gigascience/gix019 | **Demonstração empírica mais citada** de que dividir por registro em vez de por sujeito/execução produz acurácia artificialmente alta. Sustenta diretamente R4 |
| 26 | KAPOOR, S.; NARAYANAN, A. | 2023 | Leakage and the reproducibility crisis in machine-learning-based science | Patterns, 4(9) | 10.1016/j.patter.2023.100804 | Vazamento é falha sistêmica documentada em 294 artigos de 17 disciplinas. Taxonomia de 8 tipos |
| 27 | KAUFMAN, S.; ROSSET, S.; PERLICH, C.; STITELMAN, O. | 2012 | Leakage in data mining: formulation, detection, and avoidance | ACM TKDD, 6(4), p. 1-21 | 10.1145/2382577.2382579 | Definição formal e tipologia — permite escrever "define-se vazamento como..." com fonte primária |
| 28 | ROBERTS, D. R. et al. | 2017 | Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure | Ecography, 40(8), p. 913-929 | 10.1111/ecog.02881 | *Block cross-validation* / divisão por grupo em dados com estrutura temporal |
| 29 | HAMMERLA, N. Y.; PLÖTZ, T. | 2015 | Let's (not) stick together: pairwise similarity biases cross-validation in activity recognition | ACM UbiComp 2015, p. 1041-1051 | 10.1145/2750858.2807551 | **Citação exata para R5:** janelas adjacentes de um sinal contínuo são quase idênticas; se cruzarem a divisão, produzem viés |
| 30 | BERGMEIR, C.; HYNDMAN, R. J.; KOO, B. | 2018 | A note on the validity of cross-validation for evaluating autoregressive time series prediction | Comput. Statistics & Data Analysis, 120, p. 70-83 | 10.1016/j.csda.2017.11.003 | **Contra-argumento honesto.** Mostra quando a CV aleatória *é* válida — citá-la impede que um revisor acuse o artigo de simplificar |
| 31 | BERGMEIR, C.; BENÍTEZ, J. M. | 2012 | On the use of cross-validation for time series predictor evaluation | Information Sciences, 191, p. 192-213 | 10.1016/j.ins.2011.12.028 | CV convencional exige cuidado quando as amostras são temporalmente ordenadas |
| 32 | VIEIRA, J. P.; BAULER, V. A.; ROSA, R. K.; SILVA, D. | 2026 | Towards a more realistic evaluation of machine learning models for bearing fault diagnosis | Mechanical Systems and Signal Processing, 258 | 10.1016/j.ymssp.2026.114640 | Particionamento por unidade física; **grupo brasileiro (UFSC)**. O número de unidades distintas no treino, não o de amostras, determina a generalização |
| 33 | KNAP, P.; JACHYMCZYK, U.; LALIK, K. | 2026 | Leakage-Safe, Reproducible Benchmarking for Vibration-Based Fault Diagnosis | PHM Society European Conference, 9(1) | 10.36001/phme.2026.v9i1.4924 | Conecta E4.2 a E4.3: separação em nível de gravação **e** repetições com múltiplas sementes |
| 34 | LITTLE, M. A. et al. | 2017 | Using and understanding cross-validation strategies. Perspectives on Saeb et al. | GigaScience, 6(5) | 10.1093/gigascience/gix020 | Ressalva equilibrada: o esquema de CV depende do caso de uso; não há esquema universalmente correto |
| 35 | WHALEN, S.; SCHREIBER, J.; NOBLE, W. S.; POLLARD, K. S. | 2021 | Navigating the pitfalls of applying machine learning in genomics | Nature Reviews Genetics, 23(3), p. 169-181 | 10.1038/s41576-021-00434-9 | Contexto de introdução: a comunidade aplicada já mapeou essas armadilhas |
| 36 | HENDRIKS, J.; DUMOND, P.; KNOX, D. A. | 2022 | Towards better benchmarking using the CWRU bearing fault dataset | MSSP, 169 | 10.1016/j.ymssp.2021.108732 | Crítica ao uso ingênuo de dataset de referência; necessidade de protocolos rigorosos |

> **Nota de escopo:** #24, #32, #33 e #36 são de diagnóstico de falhas **por vibração em rolamentos**, não do TEP. São usadas como fundamentação **metodológica** (o argumento do vazamento), não como fonte de dados nem de resultados. Isso é compatível com a restrição do tópico 7, que se aplica aos dados. O achado de valor é poder argumentar dentro do próprio campo de diagnóstico de falhas, em vez de importar o argumento da genômica ou da saúde digital.

### E4.3 — Comparação estatística entre classificadores

| # | Autores | Ano | Título | Veículo | DOI / URL | O que permite afirmar |
|---|---|---|---|---|---|---|
| 37 | DEMŠAR, J. | 2006 | Statistical Comparisons of Classifiers over Multiple Data Sets | JMLR, 7, p. 1-30 | **sem DOI** — jmlr.org/papers/v7/demsar06a.html | **Citação obrigatória do protocolo.** Friedman para k classificadores + Wilcoxon par a par; recomendação contra o t-test pareado |
| 38 | DERRAC, J.; GARCÍA, S.; MOLINA, D.; HERRERA, F. | 2011 | A practical tutorial on the use of nonparametric statistical tests... | Swarm and Evolutionary Computation, 1, p. 3-18 | 10.1016/j.swevo.2011.02.002 | Passo a passo operacional: ranqueamento médio, Friedman, Iman-Davenport, pós-hoc com ajuste |
| 39 | BENAVOLI, A.; CORANI, G.; MANGILI, F. | 2016 | Should We Really Use Post-Hoc Tests Based on Mean-Ranks? | JMLR, 17(5), p. 1-10 | **sem DOI** — jmlr.org/papers/v17/benavoli16a.html | **Crítica direta ao Nemenyi:** o resultado depende dos demais métodos incluídos, o que o torna manipulável. Justifica usar Wilcoxon par a par com Holm |
| 40 | GARCÍA, S.; HERRERA, F. | 2008 | An Extension on "Statistical Comparisons of Classifiers..." for all Pairwise Comparisons | JMLR, 9(89), p. 2677-2694 | **sem DOI** — jmlr.org/papers/v9/garcia08a.html | p-valores ajustados (Holm, Shaffer, Bergmann-Hommel) em comparações n×n |
| 41 | DIETTERICH, T. G. | 1998 | Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms | Neural Computation, 10(7), p. 1895-1923 | 10.1162/089976698300017197 | **O que NÃO fazer:** testes sobre folds de CV violam independência e inflacionam erro tipo I |
| 42 | CARRASCO, J.; GARCÍA, S.; RUEDA, M. M.; DAS, S.; HERRERA, F. | 2020 | Recent trends in the use of statistical tests for comparing swarm and evolutionary computing algorithms | Swarm and Evolutionary Computation, 54 | 10.1016/j.swevo.2020.100665 | Diretrizes recentes revisadas por pares — o mais próximo de "estado da arte em boas práticas" |
| 43 | GARCÍA, S.; FERNÁNDEZ, A.; LUENGO, J.; HERRERA, F. | 2010 | Advanced nonparametric tests for multiple comparisons... | Information Sciences, 180, p. 2044-2064 | 10.1016/j.ins.2009.12.010 | Escolha do pós-hoc por poder estatístico, não por hábito |

### E4.4 — Algoritmos e reprodutibilidade

| # | Autores | Ano | Título | Veículo | DOI / URL | Observação |
|---|---|---|---|---|---|---|
| 44 | BREIMAN, L. | 2001 | Random Forests | Machine Learning, 45(1), p. 5-32 | 10.1023/A:1010933404324 | ✅ metadados exatos |
| 45 | FRIEDMAN, J. H. | 2001 | Greedy function approximation: a gradient boosting machine | The Annals of Statistics, 29(5), p. 1189-1232 | 10.1214/aos/1013203451 | ✅ metadados exatos |
| 46 | CHEN, T.; GUESTRIN, C. | 2016 | XGBoost: A Scalable Tree Boosting System | KDD '16, p. 785-794 | 10.1145/2939672.2939785 | ✅ metadados exatos |
| 47 | CORTES, C.; VAPNIK, V. | 1995 | Support-vector networks | Machine Learning, 20(3), p. 273-297 | 10.1007/BF00994018 | ⚠️ **título correto é "Support-vector networks"**, não "Support Vector Machines" — erro comum em listas de referências |
| 48 | PEDREGOSA, F. et al. | 2011 | Scikit-learn: Machine Learning in Python | JMLR, 12(85), p. 2825-2830 | **sem DOI** — jmlr.org/papers/v12/pedregosa11a.html | Declaração do ambiente computacional |
| 49 | KAPOOR, S.; CANTRELL, E. M. et al. | 2024 | REFORMS: Consensus-based Recommendations for Machine-learning-based Science | Science Advances, 10(18) | 10.1126/sciadv.adk3452 | **Checklist mais adequado** para ciência/engenharia aplicada (32 itens) |
| 50 | HEIL, B. J. et al. | 2021 | Reproducibility standards for machine learning in the life sciences | Nature Methods, 18(10), p. 1132-1135 | 10.1038/s41592-021-01256-7 | Níveis bronze/prata/ouro — declarar qual o artigo atinge, em escala publicada |
| 51 | PINEAU, J. et al. | 2021 | Improving Reproducibility in Machine Learning Research | JMLR, 22(164), p. 1-20 | **sem DOI** — jmlr.org/papers/v22/20-303.html | Origem do checklist de reprodutibilidade |
| 52 | DESAI, A.; ABDELHAMID, M.; PADALKAR, N. R. | 2025 | What is reproducibility in artificial intelligence and machine learning research? | AI Magazine, 46(2) | 10.1002/aaai.70004 | Uso preciso de "reprodutibilidade" vs. "replicabilidade" |
| 53 | SEMMELROCK, H. et al. | 2025 | Reproducibility in machine-learning-based research: Overview, barriers, and drivers | AI Magazine, 46(2) | 10.1002/aaai.70002 | Estado da arte 2025 sobre barreiras |

### Alertas de rigor do eixo E4

1. **JMLR não atribui DOI.** Para #37, #39, #40, #48 e #51 o identificador estável é a URL. **Nunca construir DOI para esses itens.**
2. **Números de artigo não confirmados** em: Chicco/Tötsch/Jurman (BioData Mining 14(1)), Kapoor et al. (Sci Adv 10(18)), Saeb e Little (GigaScience 6(5)), Semmelrock e Desai (AI Magazine 46(2)). Os DOIs estão confirmados; o campo "artigo n." precisa ser conferido ou omitido.
3. **Whalen et al.:** Crossref registra 2021 (online); fascículo impresso é 2022. Escolher um e ser consistente.
4. **Preprints** (Grandini et al. 2020, Ismail-Fawaz et al. 2023, Bouthillier et al. 2021, Gundersen et al. 2022) foram levantados mas **não entraram na tabela** — se usados, marcar explicitamente como preprint.

---

