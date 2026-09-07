# Restrição invariável — Base de dados (WP1A, tópico 7)

> **Regra fundamental desta sessão: nada vem de fora desta base.**

## Texto literal do WP1A, seção 7

> O experimento utilizará os dados do Tennessee Eastman Process disponibilizados em arquivos
> de treinamento e teste, contendo execuções sem falha e execuções com falhas induzidas.
> A versão atualmente empregada no laboratório contém **52 variáveis de processo** e
> **21 classes**, considerando a condição normal e 20 condições de falha.
>
> A unidade independente de divisão dos dados deverá ser **a execução do processo,
> denominada run**. Amostras pertencentes à mesma execução não poderão aparecer
> simultaneamente nos conjuntos de treinamento e teste. Essa restrição é essencial para
> impedir vazamento de informação temporal e superestimação do desempenho.

## O que isso impõe, operacionalmente

| # | Restrição | Consequência prática |
|---|---|---|
| R1 | **Base única: Tennessee Eastman Process.** | Nenhum outro dataset entra no artigo — nem para comparação, nem para ilustração, nem como "validação externa". |
| R2 | **52 variáveis de processo.** | Não incluir variáveis derivadas de fora da base. Qualquer engenharia de atributos deve ser função apenas dessas 52. |
| R3 | **21 classes** (normal + 20 falhas). | Não agregar, não colapsar nem excluir classes sem justificar explicitamente no texto. |
| R4 | **Unidade de divisão = run.** | Divisão treino/validação/teste por execução completa. Nunca por amostra, nunca por linha temporal. |
| R5 | **Nenhuma amostra da mesma run em conjuntos diferentes.** | O manifesto de divisão precisa ser salvo e verificável. Esta é a defesa contra vazamento. |
| R6 | **Sem vazamento temporal.** | Padronização e qualquer transformação dependente dos dados ajustadas **só** no treino. Seleção de hiperparâmetros **só** na validação. Teste consultado uma única vez, após congelamento. |

## Consequência para a revisão bibliográfica

As referências levantadas servem para **posicionar e justificar** — contexto, estado da arte,
fundamentação metodológica das métricas e do protocolo. Elas **não** entram como fonte de
resultados. Nenhum valor numérico de desempenho vindo da literatura pode ser apresentado
como resultado deste trabalho.

Quando a literatura for citada com números (ex.: "trabalho X reporta F1 macro de Y"), isso
só pode aparecer:

- na Introdução ou no Referencial, como caracterização do estado da arte; **ou**
- na Discussão, explicitamente marcado como resultado de terceiro, com a ressalva de que o
  protocolo experimental difere (divisão por run vs. divisão aleatória, subconjunto de
  classes, versão do dataset).

**Nunca** em tabela de resultados própria, nunca sem atribuição, nunca como se fosse
comparável ponto a ponto.

## Consequência para a redação do artigo

Todo número que aparecer nas seções de Resultados e Conclusão deve ser rastreável a uma
execução própria sobre a base TEP, registrada em CSV no repositório do projeto. Não há
exceção. Se um valor for necessário e não existir, a lacuna é declarada e a simulação é
executada — não estimada, não inferida, não tomada de empréstimo da literatura.
