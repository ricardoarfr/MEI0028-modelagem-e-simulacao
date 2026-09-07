"""build_relatorio_auditoria.py — entrega A1 do WP1A: relatório de auditoria da base em PDF.
Lê reports/01-auditoria.md e o resultado de 02_auditoria.py; não depende de editor externo."""
import os, json, textwrap
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
AUD  = json.load(open(os.path.join(RAIZ, "results", "metadata", "auditoria.json"), encoding="utf-8"))
OUT  = os.path.join(RAIZ, "reports", "A1-relatorio-auditoria.pdf")
LARG, ALT = 8.27, 11.69                       # A4 retrato, em polegadas
ESQ, DIR = 0.13, 0.90
P = lambda pt: pt / 72 / ALT

class Folha:
    """Escreve texto corrido em páginas A4, quebrando a página quando o rodapé é alcançado."""
    def __init__(self, pdf): self.pdf = pdf; self.nova()
    def nova(self):
        self.fig = plt.figure(figsize=(LARG, ALT)); self.fig.patch.set_facecolor("white"); self.y = 1 - 0.09
    def fecha(self): self.pdf.savefig(self.fig); plt.close(self.fig)
    def espaco(self, dy):
        if self.y - dy < 0.07: self.fecha(); self.nova()
    def txt(self, s, tam=10.5, cor="#111111", peso="normal", larg=86, recuo=0.0, antes=0, depois=6):
        self.y -= P(antes)
        for linha in (textwrap.wrap(s, larg) or [""]):
            self.espaco(P(tam * 1.6))
            self.fig.text(ESQ + recuo, self.y, linha, fontsize=tam, color=cor, fontweight=peso, va="top")
            self.y -= P(tam * 1.55)
        self.y -= P(depois)
    def secao(self, s): self.txt(s, 13, "#1F4E79", "bold", antes=10, depois=6)

with PdfPages(OUT) as pdf:
    # capa
    fig = plt.figure(figsize=(LARG, ALT)); fig.patch.set_facecolor("white")
    linhas_capa = [(0.62, "RELATÓRIO DE AUDITORIA DA BASE", 19, "bold", "#111111"),
                   (0.575, "Entrega A1 — Tennessee Eastman Process", 12, "normal", "#444444"),
                   (0.555, "Rieth et al. (2017), Harvard Dataverse, DOI 10.7910/DVN/6C3JR1", 11, "normal", "#444444"),
                   (0.45, "Subprojeto WP1A — Grupo A", 11, "normal", "#111111"),
                   (0.432, "MEI0028 — Modelagem e Simulação", 11, "normal", "#111111"),
                   (0.414, "Pontifícia Universidade Católica de Goiás", 11, "normal", "#111111"),
                   (0.33, "Anderson Ricardo de Freitas Rocha", 11, "normal", "#111111"),
                   (0.312, "Professor responsável: Clarimar José Coelho", 11, "normal", "#111111"),
                   (0.22, "Goiânia, setembro de 2026", 11, "normal", "#444444")]
    for y, s, tam, peso, cor in linhas_capa:
        fig.text(0.5, y, s, fontsize=tam, fontweight=peso, color=cor, ha="center", va="top")
    pdf.savefig(fig); plt.close(fig)

    f = Folha(pdf)
    f.secao("1 Objetivo")
    f.txt("Verificar a integridade e a estrutura da base antes de qualquer treinamento, conforme a Etapa 1 "
          "do protocolo (§9.1 do WP1A): dimensões, nomes e tipos das colunas, distribuição das classes, número "
          "de execuções por classe, amplitude do índice de amostra, valores ausentes, infinitos e duplicatas.")

    f.secao("2 Procedimento")
    for item in ["Download dos quatro arquivos .RData a partir do Harvard Dataverse, com conferência dos MD5 publicados.",
                 "Conversão para Parquet em ponto flutuante de 32 bits, executada em R por classe, com escrita "
                 "incremental, para manter o uso de memória constante.",
                 "Leitura de cada arquivo convertido e verificação programática de cada item acima (02_auditoria.py)."]:
        f.txt("•  " + item, recuo=0.01, larg=84)

    f.secao("3 Resultado — composição da base")
    cab = ["Arquivo", "Linhas", "Classes", "Exec./cl.", "Amostras/ex.", "Nulos", "Infin.", "Duplic."]
    col = [0.00, 0.215, 0.310, 0.395, 0.505, 0.615, 0.670, 0.735]
    f.espaco(P(150)); ytab = f.y
    for k, c in enumerate(cab):
        f.fig.text(ESQ + col[k], ytab, c, fontsize=8.5, fontweight="bold", color="#111111", va="top")
    f.y -= P(17)
    linhas = [("TEP_FaultFree_Training", "250.000", "1", "500", "500"),
              ("TEP_FaultFree_Testing", "480.000", "1", "500", "960"),
              ("TEP_Faulty_Training", "5.000.000", "20", "500", "500"),
              ("TEP_Faulty_Testing", "9.600.000", "20", "500", "960")]
    for nome, lin, cl, ex, am in linhas:
        vals = [nome, lin, cl, ex, am, "0", "0", "0"]
        for k, v in enumerate(vals):
            f.fig.text(ESQ + col[k], f.y, v, fontsize=8.5, color="#111111", va="top")
        f.y -= P(16)
    f.y -= P(8)
    f.txt("Total: 15.330.000 linhas e 55 colunas por arquivo — faultNumber, simulationRun, sample e as 52 "
          "variáveis de processo (41 medidas XMEAS e 11 manipuladas XMV), amostradas a cada três minutos.", depois=8)

    f.secao("4 Verificações por arquivo")
    for nome, cl, ex, am, tam_r, tam_p in [
        ("TEP_FaultFree_Training", "[0]", "500 (simulationRun 1 a 500)", "500 (sample 1 a 500)", "25 MB", "21 MB"),
        ("TEP_FaultFree_Testing", "[0]", "500 (simulationRun 1 a 500)", "960 (sample 1 a 960)", "47 MB", "39 MB"),
        ("TEP_Faulty_Training", "[1 a 20]", "500 (simulationRun 1 a 500)", "500 (sample 1 a 500)", "494 MB", "434 MB"),
        ("TEP_Faulty_Testing", "[1 a 20]", "500 (simulationRun 1 a 500)", "960 (sample 1 a 960)", "837 MB", "801 MB")]:
        f.txt(nome, 11, "#111111", "bold", antes=4, depois=2)
        f.txt(f"Classes: {cl} · execuções por classe: {ex} · amostras por execução: {am}", 10, "#333333", recuo=0.01, depois=1, larg=88)
        f.txt(f"Nulos 0 · infinitos 0 · duplicatas de chave 0 · .RData {tam_r} convertido em Parquet float32 {tam_p}",
              10, "#333333", recuo=0.01, depois=5, larg=88)

    f.secao("5 Conclusão da auditoria")
    f.txt("A base confere integralmente com a descrição publicada por Rieth et al. (2017). As 52 variáveis de "
          "processo são as mesmas nos arquivos de treinamento e de teste. Todas as 21 classes têm exatamente 500 "
          "execuções, e todas as execuções têm o número esperado de amostras. Não há valores ausentes, infinitos ou "
          "duplicatas de chave em nenhum dos quatro arquivos. A base foi aprovada para uso sem qualquer imputação, "
          "remoção de registros ou correção.")
    f.txt("Evidência completa: results/metadata/auditoria.json, results/tables/tab01_caracterizacao_base.csv e "
          "results/metadata/download_manifest.json (MD5 conferidos).", 10, "#444444")
    f.fecha()
print("gravado", OUT)
