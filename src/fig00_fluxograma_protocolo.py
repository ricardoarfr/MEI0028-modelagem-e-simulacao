"""fig00_fluxograma_protocolo.py — Figura 1 do artigo: fluxograma do protocolo experimental.
Padrão da Revista Sodebras: caixas brancas, traço preto fino, texto centrado, setas simples.
Gera results/figures/fig00_fluxograma_protocolo.png em 300 dpi."""
import os, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrow

ROOT = os.environ.get("WP1A_ROOT") or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
FIG = os.path.join(ROOT, "results", "figures"); os.makedirs(FIG, exist_ok=True)

# (linhas de texto, altura da caixa) — uma ação por caixa, na ordem de execução do pipeline
ETAPAS = [
    (["Base pública de Rieth et al. (2017):", "52 variáveis, 21 classes, 500 execuções cada"], 46),
    (["Auditoria dos arquivos e conversão para Parquet"], 34),
    (["Divisão por execução completa, com manifesto:", "100 treino e 50 validação por classe"], 46),
    (["Rótulo físico: amostras anteriores à falha", "recebem a classe normal"], 46),
    (["Padronização ajustada apenas no treinamento"], 34),
    (["Seleção de hiperparâmetros na validação e", "congelamento da configuração"], 46),
    (["Treino final: seis famílias × cinco sementes,", "com registro de tempo e memória"], 46),
    (["Leitura única do teste: 500 execuções por", "classe, 10,08 milhões de amostras"], 46),
    (["F1 macro, MCC, acurácia balanceada e custo,", "com intervalos por bootstrap de execuções"], 46),
]
W, GAP, MARG = 400.0, 12.0, 8.0                      # unidades de desenho
H = sum(h for _, h in ETAPAS) + GAP * (len(ETAPAS) - 1) + 2 * MARG
WC = W + 2 * MARG                                    # tela com margem lateral
LARGURA_CM = 11.5
fig = plt.figure(figsize=(LARGURA_CM / 2.54, LARGURA_CM / 2.54 * H / WC))
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, WC); ax.set_ylim(H, 0); ax.axis("off")
ax.add_patch(Rectangle((0, 0), WC, H, facecolor="white", edgecolor="none", zorder=0))

y = MARG
for i, (linhas, h) in enumerate(ETAPAS):
    ax.add_patch(Rectangle((MARG, y), W, h, facecolor="white", edgecolor="#111111", linewidth=0.8, zorder=1))
    for j, texto in enumerate(linhas):                # 18 unidades entre linhas, bloco centrado na caixa
        yy = y + h / 2 + (j - (len(linhas) - 1) / 2) * 18
        ax.text(WC / 2, yy, texto, ha="center", va="center", fontsize=8.2, color="#111111", zorder=2)
    y += h
    if i < len(ETAPAS) - 1:                            # seta até a borda da caixa seguinte
        ax.add_patch(FancyArrow(WC / 2, y, 0, GAP - 4.5, width=0.6, head_width=5, head_length=4.5,
                                length_includes_head=True, facecolor="#111111", edgecolor="#111111", zorder=2))
        y += GAP

out = os.path.join(FIG, "fig00_fluxograma_protocolo.png")
fig.savefig(out, dpi=300, facecolor="white"); plt.close(fig)
print(f"gravado {out} | {LARGURA_CM} cm × {LARGURA_CM * H / WC:.1f} cm")
