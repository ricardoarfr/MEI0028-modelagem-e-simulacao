# Lacunas na literatura recente — insumo para a justificativa do artigo

Levantadas a partir do eixo E1 (TEP + ML clássico, 2021–2026). Cada lacuna é um argumento
disponível para a Introdução e para a Discussão, e **cada uma delas o WP1A já está desenhado
para preencher**.

## L1 — Divisão por execução é praticamente inexistente

Apenas Koçak et al. (2026) trata explicitamente da agregação em nível de *run*. A maioria dos
trabalhos divide amostra a amostra dentro da mesma simulação, o que vaza informação temporal
entre treino e teste.

**O que o WP1A oferece:** o protocolo do tópico 7 fixa a execução como unidade indivisível.
É possível ainda *quantificar* a diferença entre split por amostra e split por execução —
um resultado próprio, forte e barato de produzir.

## L2 — Acurácia como métrica dominante

Boa parte da literatura reporta apenas "taxa de detecção" ou acurácia global, inadequadas em
cenário multiclasse desbalanceado com 21 classes. Falta padronização em F1 macro com
intervalo de confiança.

**O que o WP1A oferece:** métricas já previstas — F1 macro, acurácia balanceada, MCC
multiclasse, métricas por classe (§10 do WP1A), com média, desvio-padrão e IC (§11).

## L3 — Custo computacional quase nunca reportado

Só Rezgui et al. (2024) trata tempo de execução como critério explícito. Nenhum dos trabalhos
verificados reporta tempo de treino, tempo de inferência e tamanho do modelo de forma
comparável entre as famílias de algoritmos.

**O que o WP1A oferece:** está no objetivo específico 5 e nas métricas do §10 — tempo de
treinamento, tempo de inferência, tamanho do modelo salvo, consumo de memória.

## L4 — Generalização fora do conjunto de simulação

Lyu et al. (2026) é o único que mostra explicitamente a queda em conjunto independente.

**Ressalva:** avaliar entre modos de operação exigiria o dataset estendido de Reinartz et al.
(2021), o que **extrapola a restrição do tópico 7**. Registrar como trabalho futuro, não
como escopo deste artigo.

## L5 — Baselines clássicos rasos

Muitos artigos usam RF/SVM/KNN apenas como "comparação" mal ajustada, sem busca de
hiperparâmetros documentada. Não foi localizado estudo recente que compare de forma justa e
reprodutível as famílias clássicas no TEP 21 classes sob o mesmo protocolo.

**O que o WP1A oferece:** exatamente isso — seis algoritmos, protocolo único, seleção de
hiperparâmetros só na validação, teste consultado uma vez. **Esta é a lacuna central e a
principal justificativa do artigo.**

## L6 — Regressão logística ausente da literatura recente do TEP

Não foi encontrado trabalho de 2021–2026 que aplique regressão logística multinomial como
classificador principal no TEP 21 classes.

**O que o WP1A oferece:** a regressão logística é o baseline linear previsto na Tabela 1 do
WP1A, e a hipótese H3 é justamente sobre sua competitividade em custo e interpretabilidade.
Lacuna concreta e barata de preencher.

## L7 — Falhas difíceis tratadas de forma inconsistente

IDV3, IDV9, IDV15 e IDV19 aparecem como problema em Li et al. (2026), Nasif et al. (2026) e
Koçak et al. (2026), mas sem consenso sobre se devem ser excluídas, agrupadas ou reportadas
separadamente.

**O que o WP1A oferece:** objetivo específico 6 — identificar falhas com maior grau de
confusão — e a questão de pesquisa QP3. Reportar as 21 classes sem exclusão, com matriz de
confusão, já é uma posição metodológica defensável e distinta da prática corrente.

---

## Como isso se traduz na Introdução do artigo

O funil da introdução (§6 do modelo genérico) tem a lacuna como terceiro parágrafo. As
lacunas **L1, L2, L3 e L5** compõem essa lacuna de forma direta e sustentada por referências
verificadas — não há necessidade de inventar novidade.
