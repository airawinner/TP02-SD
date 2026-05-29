import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("resultado_testes.csv", sep=";")

os.makedirs("graficos", exist_ok=True)

# ==================================================
# TESTE 1
# ==================================================

dados = df[df["teste"] == "Teste 1 - Testar o impacto dos peers"]

if not dados.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        dados["peers"].astype(str),
        dados["tempo_s"]
    )

    plt.title("Teste 1 - Testar o impacto dos peers")
    plt.xlabel("Quantidade de Peers")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste1_peers.png")
    plt.close()

# ==================================================
# TESTE 2
# ==================================================

dados = df[df["teste"] == "Teste 2 - Testar o impacto da fragmentação"]

if not dados.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        dados["bloco"].astype(str),
        dados["tempo_s"]
    )

    plt.title("Teste 2 - Testar o impacto da fragmentação")
    plt.xlabel("Tamanho do Bloco")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste2_fragmentacao.png")
    plt.close()

# ==================================================
# TESTE 3
# ==================================================

dados = df[df["teste"] == "Teste 3 - Validar transferência rápida de poucos blocos"]

if not dados.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 3 - Validar transferência rápida de poucos blocos")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste3_pequenos.png")
    plt.close()

# ==================================================
# TESTE 4
# ==================================================

dados = df[df["teste"] == "Teste 4 - Validar fragmentação em número razoável de blocos"]

if not dados.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 4 - Validar fragmentação em número razoável de blocos")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste4_medios.png")
    plt.close()

# ==================================================
# TESTE 5
# ==================================================

dados = df[df["teste"] == "Teste 5 - Testar estabilidade para grandes transferências"]

if not dados.empty:

    plt.figure(figsize=(8,5))

    plt.bar(
        dados["arquivo"],
        dados["tempo_s"]
    )

    plt.title("Teste 5 - Testar estabilidade para grandes transferências")
    plt.xlabel("Arquivo")
    plt.ylabel("Tempo (s)")
    plt.grid(True)

    plt.savefig("graficos/teste5_grandes.png")
    plt.close()

# ==================================================
# TESTE 6
# ==================================================

plt.figure(figsize=(10,5))

plt.bar(
    df["arquivo"],
    df["mensagens"]
)

plt.title("Teste 6 - Configuração de Vizinhos Estática (Protocolo P2P)")
plt.xlabel("Arquivo")
plt.ylabel("Quantidade de Mensagens")
plt.grid(True)

plt.savefig("graficos/teste6_protocolo_p2p.png")
plt.close()

print("Todos os gráficos foram gerados.")