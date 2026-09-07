# Ficha técnica do dataset público do TEP

**Verificação:** DataCite API (`api.datacite.org/dois/10.7910%2FDVN%2F6C3JR1`) e Crossref,
consultadas em 2026-09-05. Onde o valor não veio da fonte oficial, isso está marcado.

---

## Conclusão que importa: qual é a base do WP1A

O WP1A §7 diz: **52 variáveis de processo e 21 classes (normal + 20 falhas)**.

| Versão do dataset | Classes | Bate com o WP1A? |
|---|---|---|
| **Rieth et al. (2017), Harvard Dataverse** | normal + **20** falhas = **21** | ✅ **sim** |
| Braatz / UIUC (clássico) | normal + **21** falhas = 22 | ❌ não |
| Reinartz et al. (2021), DTU | 28 falhas, 6 modos | ❌ não |

**A base do WP1A é o dataset Rieth et al. (2017), DOI 10.7910/DVN/6C3JR1.** A identificação
é unívoca pelo número de classes. Isso deve ser declarado explicitamente na seção de
materiais do artigo — nenhum dos quatro artigos-modelo da Sodebras omite a procedência dos
dados.

> **Correção factual importante:** o dataset "clássico" é da **UIUC** (Board of Trustees of
> the University of Illinois, Large Scale Systems Research Laboratory), **não da UCSB**.
> Braatz estava na UIUC à época e hoje está no MIT. Citar "Braatz/UCSB" seria erro factual.

---

## Ficha do dataset Rieth et al. (2017)

| Item | Valor | Fonte |
|---|---|---|
| Autores | RIETH, C. A.; AMSEL, B. D.; TRAN, R.; COOK, M. B. | DataCite |
| Afiliação | Pacific Science & Engineering Group, Inc. | DataCite |
| Editor / ano / versão | Harvard Dataverse / 2017 / V1.0 | DataCite |
| Datas | submetido 2017-03-10; disponível 2017-07-06 | DataCite |
| Licença | **Domínio público** (dedicação explícita), open access | DataCite |
| DOI | `10.7910/DVN/6C3JR1` | DataCite ✅ |
| Publicação a citar junto | RIETH et al. (2017), *Advances in Human Factors in Robots and Unmanned Systems*, AISC v. 595, p. 52-63. DOI `10.1007/978-3-319-60384-1_6` | Crossref ✅ |
| **Nº de arquivos** | **4**, formato `.RData` (data frames de R, `load()`) | DataCite |
| Nomes dos arquivos | `TEP_FaultFree_Training.RData`, `TEP_FaultFree_Testing.RData`, `TEP_Faulty_Training.RData`, `TEP_Faulty_Testing.RData` | ⚠️ código do TimeSeAD — **não** confirmado na listagem do Dataverse |
| Tamanho total | ~1,4 GB (24.678.017 / 47.327.663 / 494.063.194 / 836.882.037 bytes) | DataCite. ⚠️ **pareamento nome↔tamanho não confirmado** |
| **Colunas** | **55**: `faultNumber`, `simulationRun`, `sample`, + **52 variáveis de processo** | DataCite ✅ |
| **Classes** | **21** — falha 0 (normal, arquivos "FaultFree") + falhas 1 a 20 (arquivos "Faulty") | DataCite ✅ |
| **Runs por classe** | **500** (`simulationRun` 1 a 500), cada um com semente distinta. **Sementes de treino e teste não se sobrepõem** | DataCite ✅ |
| Amostras por run — treino | **500** → 25 horas simuladas | DataCite ✅ |
| Amostras por run — teste | **960** → 48 horas simuladas | DataCite ✅ |
| Taxa de amostragem | **3 minutos** | DataCite ✅ |
| Introdução da falha | **1 hora** nos arquivos Faulty *Training*; **8 horas** nos Faulty *Testing* | DataCite ✅ |
| Composição 41 XMEAS + 11 XMV | ⚠️ **não afirmado** na descrição do Rieth (que diz apenas "52 variáveis, nomes originais preservados"). A decomposição vem do `readme.txt` do Braatz | **Se o artigo afirmar "41+11", citar Braatz / Downs & Vogel, não Rieth** |

### Volume de dados — cálculo derivado

> ⚠️ Os números abaixo são **cálculo próprio** a partir dos parâmetros oficiais, não valores
> citados na fonte. Devem ser confirmados na auditoria (objetivo específico 1) antes de
> entrarem no artigo.

| Arquivo | Runs | Amostras/run | Linhas |
|---|---|---|---|
| FaultFree_Training | 500 | 500 | 250.000 |
| FaultFree_Testing | 500 | 960 | 480.000 |
| Faulty_Training | 20 × 500 = 10.000 | 500 | 5.000.000 |
| Faulty_Testing | 20 × 500 = 10.000 | 960 | 9.600.000 |
| **Total** | | | **≈ 15,3 milhões de linhas** |

**Implicação computacional direta:** com ~5,25 milhões de linhas de treino × 52 variáveis, o
SVM com kernel RBF é inviável sem amostragem ou aproximação. O WP1A já antecipa isso ao
especificar "uma implementação escalável" para o SVM (Tabela 1). Essa decisão precisa ser
documentada e justificada na metodologia — e o custo computacional é justamente um dos
resultados do benchmark (objetivo específico 5).

---

## Outras versões públicas — para a discussão, não para os dados

| Versão | Estrutura | Observação |
|---|---|---|
| **Braatz / UIUC** | 22 arquivos treino (`d00.dat`…`d21.dat`) + 22 teste (`d00_te.dat`…`d21_te.dat`). Treino 480×52; teste 960×52, falha na amostra 161. ASCII delimitado por espaço. **21 falhas**, **uma execução por falha — sem replicação** | Usado em boa parte da literatura pré-2017. Sem replicação, não permite intervalo de confiança |
| ⚠️ **Armadilha do `d00.dat`** | `d00.dat` está **transposto**: 52 linhas × 500 colunas, enquanto `d01.dat`…`d21.dat` são 480 × 52 | Erro clássico de pipeline. Registrado aqui mesmo não usando essa versão — vale como item de auditoria |
| **Reinartz / DTU** (`10.11583/DTU.13385936.v1`) | 6 arquivos HDF5 (~23,9 GB cada), 28 falhas, 6 modos operacionais, 500 réplicas, 100 h por simulação, transições de modo. CC0. Gerado com o simulador revisado de Bathelt et al. (2015) | **Fora do escopo** pela restrição do tópico 7. Citar como trabalho futuro |
| **Espelhos Kaggle** | `averkij/tennessee-eastman-process-simulation-dataset` (.RData) e `afrniomelo/tep-csv` (CSV) | Espelhos do Rieth, **sem DOI e sem garantia de integridade**. Se usados por conveniência, citar o DOI original e mencionar o espelho em nota |
| **`fddbenchmark`** (AIRI Institute) | Biblioteca Python que empacota `rieth_tep`, `reinartz_tep`, `small_tep` com métricas padronizadas | ⚠️ O README **não indica artigo próprio a citar**. Citar a URL do repositório, nunca um artigo inexistente |

---

## Lacunas de verificação — resolver antes da submissão

| # | Lacuna | Como resolver |
|---|---|---|
| 1 | Pareamento nome↔tamanho dos 4 arquivos do Rieth | A API do Dataverse retornou HTTP 504 em todas as tentativas. **Abrir a página no navegador** e travar os números |
| 2 | Checksums MD5 dos arquivos | Mesma causa; obter ao baixar |
| 3 | ~~Composição 41 XMEAS + 11 XMV no dataset Rieth~~ | ✅ **RESOLVIDA na auditoria (2026-09-06):** colunas `xmeas_1`…`xmeas_41` e `xmv_1`…`xmv_11` — 41 + 11 = 52, idênticas em treino e teste |
| 4 | Por que Rieth tem 20 falhas e Braatz tem 21 | Não há justificativa em fonte primária. **Não afirmar o motivo no artigo** |
| 5 | ISBN e nº de páginas do livro de Chiang, Russell & Braatz (2001) | Crossref não expõe; buscar na página da Springer |
| 6 | Abstracts de Melo et al. (2022) e Bi et al. (2022) | Não depositados no Crossref; ScienceDirect bloqueia. Metadados confirmados, conteúdo inferido do título — **ler antes de citar afirmação específica** |
| 7 | Se Lyu et al. (2026) já saiu em periódico | Hoje é preprint ChemRxiv. Citar preprint enfraquece o argumento — reconferir antes da submissão |
