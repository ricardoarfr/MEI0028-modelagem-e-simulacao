# Protocolo da revisão bibliográfica — artigo WP1A / Sodebras

## Objetivo

Montar o referencial bibliográfico do artigo derivado do WP1A (benchmark reproduzível de
métodos clássicos de ML para diagnóstico de falhas no Tennessee Eastman Process), com
rastreabilidade total de cada referência.

## Critério de inclusão

| Eixo | Recorte temporal | Justificativa |
|---|---|---|
| E1 — TEP + ML clássico | 2021–2026 | Estado da arte contra o qual o benchmark se posiciona |
| E2 — Fontes canônicas do TEP e datasets | qualquer ano | Downs & Vogel (1993), Chiang et al. (2001), dataset Rieth et al. — indispensáveis |
| E3 — Benchmarks, surveys e deep learning no TEP | 2021–2026 | Justificam por que uma linha de base clássica ainda é necessária |
| E4 — Métricas, vazamento de dados e comparação estatística | qualquer ano p/ seminais; 2021–2026 p/ crítica recente | Sustentam as escolhas metodológicas do protocolo |
| E5 — Referências dos algoritmos | qualquer ano | Breiman, Friedman, Chen & Guestrin, Cortes & Vapnik, Pedregosa et al. |

## Regra de verificação — CRITÉRIO MÁXIMO

Nenhuma referência entra na tabela mestra sem ter sido **confirmada em fonte acessada**.

Três estados possíveis, e nenhum outro:

- **VERIFICADA** — autores, título, veículo, ano e DOI/URL foram vistos em página do editor,
  DOI resolvido, ou repositório oficial. Só estas podem ir para o artigo.
- **PARCIAL** — a obra existe e foi vista, mas algum campo não foi confirmado (tipicamente
  o DOI, ou os valores numéricos que só aparecem no texto completo). Usável mediante
  complementação; o campo faltante fica marcado como tal.
- **NÃO CONFIRMADA** — suspeita de existir, não verificada. **Nunca vai para o artigo.**
  Fica registrada apenas para eventual busca posterior.

**Proibido:** construir DOI plausível, completar autoria de memória, inferir volume/página,
citar a partir de citação de terceiro sem confirmar a fonte primária.

## Restrição editorial

A Sodebras publica artigos com **8 a 16 referências** e limite de ~3.500 palavras / 6
páginas. A tabela mestra pode ter mais entradas do que caberão no artigo — a seleção final
escolherá as de maior peso, mantendo a proporção observada no corpus (predomínio de
periódicos, mistura de fontes nacionais e internacionais conforme a natureza do trabalho).

Regra da revista: *"Todas as referências listadas neste item devem aparecer no corpo do texto
e vice-versa."* — a conferência texto↔lista é obrigatória antes da submissão.

## Formato ABNT exigido (autor-data)

```
SOBRENOME, Nome. Título do artigo. Nome do Periódico, v. X, n. Y, p. 00-00, ano.
Disponível em: <URL>. Acesso em: DD mmm. AAAA.
```

- Autor na frase: `Breiman (2001)`
- Autor fora da frase: `(BREIMAN, 2001)`
- Até 3 autores: todos. Mais de 3: primeiro + `et al.`

## Arquivos desta pasta

| Arquivo | Conteúdo |
|---|---|
| `00-PROTOCOLO.md` | este documento |
| `01-TABELA-MESTRA.md` | todas as referências verificadas, por eixo |
| `02-NAO-CONFIRMADAS.md` | quarentena — não usar no artigo |
| `03-FICHA-DATASET-TEP.md` | ficha técnica do dataset público do TEP |
| `04-LACUNAS.md` | o que a literatura recente não cobre — insumo para a justificativa do artigo |
| `pdfs/` | PDFs baixados das referências, quando disponíveis em acesso aberto |

---

## Tabela de ancoragem de citações

Formato herdado de `Revisao_modelo_criar outro.xlsx` — o padrão de rigor já usado na
dissertação. Cada citação do artigo é ancorada em um **trecho literal da fonte**, com
localização precisa, e recebe um diagnóstico explícito.

Colunas:

| Coluna | Conteúdo |
|---|---|
| **ID** | sequencial; prefixo `W-` para ajustes de escrita, `E-` para ajustes editoriais |
| **Tópico** | seção do artigo onde a citação aparece |
| **Citação** | forma da chamada no texto, em ABNT autor-data |
| **Trecho do artigo (PT)** | a frase do nosso artigo que a citação sustenta |
| **Trecho da fonte** | o texto **literal** da fonte que ancora a afirmação |
| **Pág./Loc.** | página, seção ou localização exata dentro da fonte |
| **Tradução (PT)** | tradução do trecho, quando a fonte é em outro idioma |
| **Diagnóstico** | ✅ bem ancorada · ⚠️ ancoragem parcial · ❌ mal ancorada |
| **Decisão final** | manter · substituir · corrigir · remover |
| **Status** | ✅ aprovada · 🔄 aplicada · ⏳ pendente |

**Regra de ouro:** uma afirmação sem trecho literal correspondente na fonte é uma afirmação
sem ancoragem. Ou se encontra o trecho, ou se troca a fonte, ou se reescreve a afirmação.
Não se cita "de cabeça" nem por proximidade temática.

**Erros que este formato existe para pegar** — todos observados na revisão anterior:

- fonte tópico-adjacente mas que não sustenta a afirmação específica;
- afirmação factual atribuída à fonte errada;
- métrica atribuída a um trabalho que reporta outra (ex.: citar F1 de quem só reporta
  precisão e revocação);
- referência que ficou órfã na bibliografia após substituição no corpo;
- inconsistência na forma da chamada (`et al.` com 3 autores);
- número sem fonte inserido no texto.

Esta tabela só começa a ser preenchida nas colunas de "Trecho do artigo" **depois** que
houver texto redigido. Até lá, preenche-se a parte bibliográfica (ID, Tópico previsto,
Citação, Trecho da fonte, Pág./Loc., Tradução, Diagnóstico de ancoragem potencial).
