"""09_registro.py — copia figuras/tabelas/dados relevantes para ../apresentacao/ e gera o Excel de referenciamento
(ID, tipo, arquivo, título/legenda, descrição, explicação breve, fonte, seção do artigo, insumo §12 do WP1A)."""
import os, shutil, glob, json, pandas as pd
ROOT=os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)),".."); AP=os.path.join(ROOT,"..","apresentacao")
TAB=os.path.join(ROOT,"results","tables"); FIG=os.path.join(ROOT,"results","figures"); META=os.path.join(ROOT,"results","metadata")
for d in ("figuras","tabelas","dados"): os.makedirs(os.path.join(AP,d),exist_ok=True)
REG=[ # (arquivo, tipo, título/legenda, descrição, explicação breve p/ leigo, seção do artigo, insumo §12)
 ("tab01_caracterizacao_base.csv","tabela","Tabela 1 – Caracterização da base de dados","Linhas, colunas, classes, runs por classe, amostras por run, nulos, infinitos e duplicatas de cada um dos 4 arquivos do dataset Rieth et al. (2017).","É o inventário: diz exatamente o que há na base antes de qualquer modelo. Sem isso, um erro nos dados vira erro no resultado sem ninguém perceber.","II. Metodologia (2.1)","1"),
 ("manifesto_divisao.csv","dado","Manifesto de divisão por execução (run)","Uma linha por (classe, run) com o conjunto ao qual pertence: treino (100/classe), validação (50/classe), teste (500/classe), não usado.","É a prova de que nenhuma simulação foi usada para ensinar e testar ao mesmo tempo — qualquer pessoa pode conferir.","II. Metodologia (2.2)","A3"),
 ("tab_piloto_vazamento.csv","tabela","Tabela – Efeito da unidade de divisão (piloto)","Mesmo modelo (árvore), mesmo volume de dados: divisão por run vs. divisão aleatória por amostra. Acurácia, acurácia balanceada, F1 macro e MCC.","Mede o vazamento nos nossos próprios dados. Se a versão embaralhada acerta muito mais, a diferença não é desempenho — é o modelo reconhecendo vizinhos que já viu.","III. Resultados (3.1)","8"),
 ("fig07_vazamento.png","figura","Figura – Efeito do vazamento de dados","Barras comparando as quatro métricas nas duas formas de divisão.","Visualização do experimento acima.","III. Resultados (3.1)","8"),
 ("fig_eda_pca.png","figura","Figura – Projeção PCA das 21 classes","Duas primeiras componentes principais, 2.000 amostras por classe (treino), normal em preto.","Comprime 52 medições em duas dimensões desenháveis. Classes que se sobrepõem na figura são as que os modelos vão confundir.","III. Resultados (3.1)","A2"),
 ("fig_eda_correlacao.png","figura","Figura – Correlação entre as 52 variáveis","Matriz de correlação de Pearson (treino, padronizado).","Mostra quais sensores 'andam juntos'. Muita correlação significa redundância — informação repetida.","II. Metodologia / apêndice","A2"),
 ("fig_eda_separacao.png","figura","Figura – Afastamento de cada falha em relação ao normal","Por variável e por falha: |média_falha − média_normal| / desvio_normal.","Quanto mais escura a linha de uma falha, mais parecida com a operação normal — e mais difícil de detectar.","III. Resultados (3.1)","A2"),
 ("tab02_hiperparametros.csv","tabela","Tabela 2 – Hiperparâmetros selecionados","Configuração final de cada modelo, escolhida pelo F1 macro na validação (nunca no teste).","Cada modelo tem 'botões' de ajuste. Estes são os valores escolhidos — usando só a validação, para não contaminar o teste.","II. Metodologia (2.4)","2"),
 ("tab09_busca_hp_resumo.csv","tabela","Tabela – Resumo da busca de hiperparâmetros","Número de configurações testadas por modelo e faixa de F1 macro na validação.","Mostra quanto cada modelo variou conforme o ajuste — modelos sensíveis ao ajuste exigem mais cuidado.","II. Metodologia (2.4)","2"),
 ("tab09b_nystroem_tradeoff.csv","tabela","Tabela – SVM via Nyström: qualidade × custo","F1 macro, MCC e tempo em função do número de componentes D e de C.","O SVM exato é inviável nesta escala; a aproximação tem um 'botão' (D) que troca tempo por qualidade. A tabela mostra o preço de cada escolha.","III. Resultados (3.4)","7"),
 ("fig06_svm_nystroem_tradeoff.png","figura","Figura – SVM via Nyström em função de D","Curvas de F1 macro e tempo de treino vs. D.","Visualização do compromisso acima.","III. Resultados (3.4)","7"),
 ("tab03_metricas_globais.csv","tabela","Tabela 3 – Métricas globais no teste","Média, desvio-padrão e IC 95% (5 sementes) de acurácia, acurácia balanceada, F1 macro, F1 ponderada e MCC; também com rótulo do run.","O resultado central. Cinco repetições e intervalo de confiança: é a diferença entre 'deu 87%' e 'dá entre 86,5% e 87,5%'.","III. Resultados (3.2)","3"),
 ("fig01_f1_mcc_comparativo.png","figura","Figura 1 – F1 macro e MCC por modelo","Barras com IC 95%.","F1 macro dá o mesmo peso a cada classe; MCC só é alto quando toda a matriz de acertos está boa. Juntos, evitam que uma acurácia alta esconda classes ignoradas.","III. Resultados (3.2)","6"),
 ("tab04_metricas_por_classe.csv","tabela","Tabela 4 – Precisão, revocação e F1 por classe","Por modelo e por classe (média de 5 sementes).","Mostra onde cada modelo acerta e onde falha, falha por falha.","III. Resultados (3.3)","4"),
 ("fig04_f1_por_classe_heatmap.png","figura","Figura – F1 por classe (mapa de calor)","Modelos × 21 classes.","Colunas escuras em todos os modelos = falhas intrinsecamente difíceis, não fraqueza de um algoritmo.","III. Resultados (3.3)","4"),
 ("tab06_falhas_confundidas.csv","tabela","Tabela – Pares de classes mais confundidos","Para cada modelo, os 10 pares (verdadeira → predita) com maior fração fora da diagonal.","Diz *com o que* o modelo confunde cada falha — informação de engenharia, não só estatística.","III. Resultados (3.3)","8"),
 ("tab06b_dificuldade_por_classe.csv","tabela","Tabela – Dificuldade por classe","F1 médio entre modelos, por classe, ordenado.","Ranking das falhas mais difíceis, independente do algoritmo.","III. Resultados (3.3)","8"),
 ("tab05_custo_computacional.csv","tabela","Tabela 5 – Custo computacional","Tempo de treino, tempo de inferência (total e por amostra), tamanho do modelo e pico de memória — mesmo hardware, 5 sementes.","Um modelo 1% melhor mas 50× mais lento não é 'melhor', é diferente. Em planta industrial a resposta precisa vir em segundos.","III. Resultados (3.4)","5"),
 ("fig02_custo_computacional.png","figura","Figura 2 – Custo computacional","Três painéis em escala log: treino, inferência por amostra, tamanho.","Visualização da tabela acima.","III. Resultados (3.4)","7"),
 ("fig05_tradeoff_f1_vs_inferencia.png","figura","Figura – Desempenho × custo de inferência","Dispersão F1 macro vs. tempo por amostra (log).","O 'melhor compromisso' (QP5 do WP1A) está no canto superior esquerdo: alto F1, baixo tempo.","III. Resultados (3.4)","7"),
 ("tab07_estatistica.csv","tabela","Tabela – Comparação estatística","Friedman (global) e Wilcoxon pareado com correção de Holm, sobre F1 macro e MCC nas 5 sementes.","Responde se as diferenças entre modelos são maiores que a variação por acaso entre repetições.","III. Resultados (3.2)","3"),
 ("tab08_run_level.csv","tabela","Tabela – Métricas em nível de execução (voto majoritário)","F1 macro, acurácia e MCC agregando as predições de cada run por voto majoritário.","Em vez de julgar cada leitura de 3 min, julga a simulação inteira. É como Koçak et al. (2026) reportam — permite comparação direta.","III. Resultados (3.5)","3"),
 ("ambiente.json","dado","Metadados do ambiente computacional","Versões de Python e bibliotecas, hardware, sementes.","Permite a outra pessoa reproduzir exatamente o que foi feito.","II. Metodologia (2.5)","10"),
 ("busca_hp_resultados.json","dado","Resultados brutos da busca de hiperparâmetros","Todas as configurações testadas com F1 macro, MCC e tempo (validação).","Registro completo do ajuste — nada foi escolhido 'de cabeça'.","apêndice / repositório","9"),
 ("auditoria.json","dado","Auditoria completa (JSON)","Todos os itens do §9.1 do WP1A por arquivo.","Versão detalhada da Tabela 1.","repositório","1"),
]
for m in ["regressao_logistica","arvore_decisao","random_forest","gradient_boosting","xgboost","svm_nystroem"]:
    REG.append((f"fig03_matriz_confusao_{m}.png","figura",f"Figura – Matriz de confusão: {m}","Normalizada por linha, 5 sementes agregadas, rótulo físico.","Cada linha é a classe verdadeira; cada coluna, o que o modelo disse. A diagonal são os acertos; o resto, as confusões.","III. Resultados (3.3) / apêndice","5"))
    REG.append((f"tab_matriz_confusao_{m}.csv","tabela",f"Tabela – Matriz de confusão (CSV): {m}","Valores normalizados da figura correspondente.","Versão numérica da matriz.","repositório","5"))
rows=[]
for i,(arq,tipo,tit,desc,expl,sec,ins) in enumerate(REG,1):
    src=None
    for base in (TAB,FIG,META):
        if os.path.exists(os.path.join(base,arq)): src=os.path.join(base,arq); break
    dst_dir={"figura":"figuras","tabela":"tabelas","dado":"dados"}[tipo]; status="ok" if src else "AUSENTE"
    if src: shutil.copy2(src,os.path.join(AP,dst_dir,arq))
    rows.append(dict(ID=f"{tipo[0].upper()}{i:02d}",Tipo=tipo,Arquivo=f"{dst_dir}/{arq}",Titulo_Legenda=tit,Descricao=desc,Explicacao_breve=expl,Secao_do_artigo=sec,Insumo_WP1A_s12=ins,Fonte="Autores (2026), a partir de Rieth et al. (2017)",Status=status))
df=pd.DataFrame(rows); xl=os.path.join(AP,"REGISTRO-FIGURAS-TABELAS.xlsx")
with pd.ExcelWriter(xl,engine="openpyxl") as w:
    df.to_excel(w,sheet_name="Registro",index=False); ws=w.sheets["Registro"]
    for col,wd in zip("ABCDEFGHIJ",(6,8,42,48,70,80,26,10,34,9)): ws.column_dimensions[col].width=wd
df.to_csv(os.path.join(AP,"REGISTRO-FIGURAS-TABELAS.csv"),index=False)
print(df[["ID","Arquivo","Status"]].to_string(index=False)); print(f"\n{(df.Status=='ok').sum()}/{len(df)} presentes → {xl}")
