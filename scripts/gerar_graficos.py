import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("resultado_testes.csv", sep=";")

os.makedirs("graficos", exist_ok=True)

# ==================================================
# TESTE 1
# ==================================================

dados = df[
    df["teste"] == "Teste 1 - Testar o impacto dos peers"
]

if not dados.empty:

    plt.figure(figsize=(8, 5))

    plt.bar(
        dados["peers"].astype(str),
        dados["tempo_s"]
    )

    plt.title("Teste 1 - Impacto da Quantidade de Peers")
    plt.xlabel("Quantidade de Peers")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste1_peers.png")
    plt.close()

# ==================================================
# TESTE 2
# ==================================================

dados = df[
    df["teste"] == "Teste 2 - Testar o impacto da fragmentação"
]

if not dados.empty:

    plt.figure(figsize=(8, 5))

    plt.bar(
        dados["bloco"].astype(str),
        dados["throughput_Bps"]
    )

    plt.title("Teste 2 - Impacto da Fragmentação")
    plt.xlabel("Tamanho do Bloco (bytes)")
    plt.ylabel("Throughput (B/s)")
    plt.grid(True)

    plt.savefig("graficos/teste2_fragmentacao.png")
    plt.close()

# ==================================================
# TESTE 3
# ==================================================

dados = df[
    (df["teste"] == "Teste 3 - Validar transferência rápida de poucos blocos")
    & (df["bloco"] == 1024)
    & (df["peers"] == 2)
]

if not dados.empty:

    plt.figure(figsize=(8, 5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 3 - Arquivos Pequenos")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste3_pequenos.png")
    plt.close()

# ==================================================
# TESTE 4
# ==================================================

dados = df[
    (df["teste"] == "Teste 4 - Validar fragmentação em número razoável de blocos")
    & (df["bloco"] == 1024)
    & (df["peers"] == 2)
]

if not dados.empty:

    plt.figure(figsize=(8, 5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 4 - Arquivos Médios")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste4_medios.png")
    plt.close()

# ==================================================
# TESTE 5
# ==================================================

dados = df[
    (df["teste"] == "Teste 5 - Testar estabilidade para grandes transferências")
    & (df["bloco"] == 1024)
    & (df["peers"] == 2)
]

if not dados.empty:

    plt.figure(figsize=(8, 5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 5 - Arquivos Grandes")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste5_grandes.png")
    plt.close()

# ==================================================
# TESTE 6
# ==================================================

dados = (
    df.groupby("arquivo", as_index=False)["mensagens"]
      .mean()
)

plt.figure(figsize=(10, 5))

plt.bar(
    dados["arquivo"],
    dados["mensagens"]
)

plt.title("Teste 6 - Quantidade Média de Mensagens por Arquivo")
plt.xlabel("Arquivo")
plt.ylabel("Mensagens")
plt.grid(True)

plt.savefig("graficos/teste6_protocolo_p2p.png")
plt.close()

print("Todos os gráficos foram gerados.")