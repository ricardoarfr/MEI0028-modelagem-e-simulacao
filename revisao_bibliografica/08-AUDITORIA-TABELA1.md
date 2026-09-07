# Auditoria literal das três afirmações da Tabela 1 (13 trabalhos, texto completo)

**Data:** 06/09/2026. **Método:** os 13 PDFs foram convertidos em texto (`pdftotext -layout`) e
submetidos à mesma busca por expressões regulares (`pdfs/tabela1/busca_literal.py`); cada
ocorrência foi lida em contexto. Regra: só conta o que o texto declara; descrição do conjunto de
dados não equivale a declaração de rótulo. Arquivos em `pdfs/tabela1/`.

## A. Coeficiente de correlação de Matthews — 0 de 13 (CONFIRMADO)

Padrões: `matthews`, `\bMCC\b`, `phi coefficient`. Zero ocorrências em todos os 13 textos
(inclusive Çancıoğlu, em turco, e Sokolov).

## B. Custo computacional — a afirmação precisa ser reescrita

| Trabalho | O que mede | Para quem | Equipamento declarado | Trecho literal |
|---|---|---|---|---|
| Koçak 2026 | latência de inferência (6,16 ms CPU / 35,28 ms GPU), extração (0,0654 ms), tamanho do modelo | **só o XGBoost W=50**; RF e SVM linear não medidos; SVM RBF excluído por custo | i7-10750H, RTX 2060 | "the computational cost of the trained model was benchmarked… The trained W = 50 XGBoost classifier" |
| Lyu 2026 (preprint) | **tempo de treinamento de todos os 7 modelos** (XGBoost 40m0s; LSTM 20m5s; LSTM-FCN 26m14s; CNN-Transformer 67m33s; TransKal 31m53s; Conv-AE 56s; LSTM-AE 11m47s) e tempo de ajuste | todos | **não declarado no texto principal** (0 ocorrências de hardware/GPU/workstation) | "Training times varied substantially across models…"; Tabela 5 coluna "Training Time" |
| Khan 2026 | tempo total de treinamento 1,6 h; 36 s/época | **só o CRNN proposto** (Tabela 4); baselines LR/SVM/RF/LightGBM/LSTM/CNN-LSTM sem custo | Tabela 6 (requisitos mínimos) | "the observed training time on the hardware platform summarized in Table 6" |
| Zhang 2021 | menção qualitativa | — | — | "the computational time of DPRF is longer compared to the other four FDD algorithms" |
| Sokolov 2019 | menção qualitativa de RAM, sobre outro conjunto (Gas Pipeline) | — | — | "the amount of RAM needed for training… depends polynomially" |
| Márquez-Vera 2026 | menção qualitativa | — | — | "significantly lower computational complexity compared to deep learning" |
| Hu 2022; Avanashilingam 2026 | "latency" = atraso de detecção, não custo | — | — | — |
| Peter 2024; Çancıoğlu 2021; Miraliakbar 2024; Xu 2022; Li 2026 | nada | — | — | 0 ocorrências |

**Conclusão B:** a frase "nenhum mede o custo computacional de todas as famílias comparadas em
condições comparáveis" só se sustenta pelo qualificador "condições comparáveis" (Lyu não declara
o equipamento). Formulação verificável: **um trabalho reporta o tempo de treinamento de todos os
modelos comparados, sem declarar o equipamento (Lyu); dois medem custo apenas do modelo proposto
(Koçak, Khan); nenhum reporta tempo de inferência e memória para todas as famílias comparadas no
mesmo equipamento.**

## C. Rótulo das amostras anteriores à falha — 3 de 13 (CONFIRMADO, com critério explícito)

Critério: o texto declara o que faz com as amostras anteriores à falha nas execuções de teste
(rótulo atribuído ou exclusão). Descrever que "as primeiras 160 amostras são normais" não conta.

| Trabalho | Declara? | Trecho literal |
|---|---|---|
| Li 2026 | **Sim** | "For d0k_te, the first 160 timesteps are labeled as 0, and the subsequent timesteps are labeled as 1." |
| Lyu 2026 | **Sim** | "the corresponding label is assigned based on the fault state at the final time step of that window" |
| Koçak 2026 | **Sim** | janelas de execuções com falha avaliadas a partir do início da falha: "sampling was further restricted to post-fault-onset observations only, consistent with the protocol described in Section 2.1"; verificação "excluding any window whose underlying history included pre-fault samples" (Δ F1 = 0,0010) |
| Khan 2026 | Limítrofe | declara a regra do rótulo, derivada da execução ("Class in {FaultFree, Faulty}, derived from faultNumber"), sem tratar do segmento pré-falha; usa t0 só para atraso de alarme |
| Zhang 2021 | Não | descreve o conjunto: "the first 160 samples are in the normal state and the last 800 samples are in the corresponding fault state [53]" — sem dizer o rótulo usado |
| Xu 2022 | Não | descreve: "the first 160 were captured during normal operation, and the remaining 800 were collected after the failure" |
| Hu 2022 | Não | descreve: "the 161st sample is when they all start to fail" |
| Avanashilingam 2026 | Não | "allowing models to learn both pre-fault and fault evolution patterns" — sem regra de rótulo |
| Márquez-Vera 2026 | Não | simulação própria; declara segmentos (500 normais, 511 falha, 990 pós-falha) sem regra de rótulo para o pós-falha |
| Sokolov 2019; Peter 2024; Çancıoğlu 2021; Miraliakbar 2024 | Não | 0 ocorrências |

**Conclusão C:** 3/13 sob o critério estrito (Koçak, Lyu, Li); 4/13 se a regra de Khan for
aceita. O artigo deve enunciar o critério na linha da Tabela 1.
