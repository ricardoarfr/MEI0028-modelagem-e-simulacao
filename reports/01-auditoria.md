# Relatório de auditoria da base — WP1A Etapa 1 (§9.1)

Fonte: Rieth et al. (2017), Harvard Dataverse, DOI 10.7910/DVN/6C3JR1. MD5 de cada .RData verificado no download.

## Tabela 1 — Caracterização da base

| Arquivo                |   Linhas |   Colunas |   Classes |   Runs_por_classe |   Amostras_por_run |   Nulos |   Infinitos |   Duplicatas |
|:-----------------------|---------:|----------:|----------:|------------------:|-------------------:|--------:|------------:|-------------:|
| TEP_FaultFree_Training |   250000 |        55 |         1 |               500 |                500 |       0 |           0 |            0 |
| TEP_FaultFree_Testing  |   480000 |        55 |         1 |               500 |                960 |       0 |           0 |            0 |
| TEP_Faulty_Training    |  5000000 |        55 |        20 |               500 |                500 |       0 |           0 |            0 |
| TEP_Faulty_Testing     |  9600000 |        55 |        20 |               500 |                960 |       0 |           0 |            0 |

## Variáveis de processo

- Total: **52** (XMEAS: 41 · XMV: 11)
- Mesmas variáveis em treino e teste: **True**

## Verificações por arquivo

### TEP_FaultFree_Training
- classes: [0]
- runs por classe: [500] · simulationRun 1–500
- amostras por run: 500–500 · sample 1–500
- nulos/NaN 0 · infinitos 0 · duplicatas de chave 0
- .RData 25 MB → parquet float32 21 MB

### TEP_FaultFree_Testing
- classes: [0]
- runs por classe: [500] · simulationRun 1–500
- amostras por run: 960–960 · sample 1–960
- nulos/NaN 0 · infinitos 0 · duplicatas de chave 0
- .RData 47 MB → parquet float32 39 MB

### TEP_Faulty_Training
- classes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
- runs por classe: [500] · simulationRun 1–500
- amostras por run: 500–500 · sample 1–500
- nulos/NaN 0 · infinitos 0 · duplicatas de chave 0
- .RData 494 MB → parquet float32 434 MB

### TEP_Faulty_Testing
- classes: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
- runs por classe: [500] · simulationRun 1–500
- amostras por run: 960–960 · sample 1–960
- nulos/NaN 0 · infinitos 0 · duplicatas de chave 0
- .RData 837 MB → parquet float32 801 MB

