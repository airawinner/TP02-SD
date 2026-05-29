import pandas as pd
import matplotlib.pyplot as plt
import math
import os

# =====================================
# CARREGA CSV
# =====================================

df = pd.read_csv(
    "resultado_testes.csv",
    sep=";"
)

# =====================================
# CRIA PASTA DE SAÍDA
# =====================================

os.makedirs("tabelas", exist_ok=True)

# =====================================
# CONFIGURAÇÕES
# =====================================

LINHAS_POR_TABELA = 8

total_tabelas = math.ceil(
    len(df) / LINHAS_POR_TABELA
)

# =====================================
# GERA TABELAS
# =====================================

for i in range(total_tabelas):

    inicio = i * LINHAS_POR_TABELA
    fim = inicio + LINHAS_POR_TABELA

    parte = df.iloc[inicio:fim]

    fig, ax = plt.subplots(
        figsize=(22, 4.5)
    )

    ax.axis("off")

    tabela = ax.table(
        cellText=parte.values,
        colLabels=parte.columns,
        loc="center",
        cellLoc="center"
    )

    # =====================================
    # TAMANHO DA FONTE
    # =====================================

    tabela.auto_set_font_size(False)
    tabela.set_fontsize(8)

    tabela.scale(
        1.25,
        2
    )

    # =====================================
    # CABEÇALHO ROSA
    # =====================================

    for coluna in range(len(parte.columns)):

        celula = tabela[(0, coluna)]

        celula.set_facecolor("#D81B60")

        celula.set_text_props(
            color="white",
            weight="bold"
        )

    # =====================================
    # LINHAS ALTERNADAS
    # =====================================

    for linha in range(1, len(parte) + 1):

        cor = "#FCE4EC" if linha % 2 == 0 else "white"

        for coluna in range(len(parte.columns)):

            tabela[(linha, coluna)].set_facecolor(cor)

    # =====================================
    # BORDAS
    # =====================================

    for _, cell in tabela.get_celld().items():

        cell.set_edgecolor("#AD1457")
        cell.set_linewidth(0.7)

    # =====================================
    # TÍTULO
    # =====================================

    plt.title(
        f"Resultados dos Testes P2P (Parte {i + 1}/{total_tabelas})",
        fontsize=16,
        fontweight="bold",
        color="#AD1457",
        pad=20
    )

    plt.tight_layout()

    # =====================================
    # SALVAR
    # =====================================

    caminho_saida = (
        f"tabelas/tabela_resultados_parte_{i + 1}.png"
    )

    plt.savefig(
        caminho_saida,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print(
        f"Gerado: {caminho_saida}"
    )

print()
print("Todas as tabelas foram geradas com sucesso.")