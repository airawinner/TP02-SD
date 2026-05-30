import subprocess
import time
import os
import pandas as pd
import re

RESULTADOS = []

# =====================================
# ARQUIVOS DO ENUNCIADO
# =====================================

ARQUIVOS = [
    ("10KB", 10 * 1024),
    ("20KB", 20 * 1024),
    ("1MB", 1 * 1024 * 1024),
    ("5MB", 5 * 1024 * 1024),
    ("10MB", 10 * 1024 * 1024),
    ("20MB", 20 * 1024 * 1024)
]

BLOCOS = [1024, 4096]

PEERS = [2, 4]

# =====================================
# FUNÇÕES
# =====================================

def criar_arquivo(nome, tamanho):

    os.makedirs("files", exist_ok=True)

    with open(nome, "wb") as f:
        f.write(os.urandom(tamanho))


def alterar_bloco(valor):

    with open("config.py", "r", encoding="utf8") as f:
        txt = f.read()

    txt = re.sub(
        r"TAMANHO_BLOCO\s*=\s*\d+",
        f"TAMANHO_BLOCO = {valor}",
        txt
    )

    with open("config.py", "w", encoding="utf8") as f:
        f.write(txt)


def limpar_logs():

    os.makedirs("logs", exist_ok=True)

    for arq in os.listdir("logs"):
        os.remove(os.path.join("logs", arq))


def limpar_downloads():

    for i in range(1, 5):

        pasta = f"files/p{i}"

        if os.path.exists(pasta):

            for arq in os.listdir(pasta):
                os.remove(os.path.join(pasta, arq))


def contar_mensagens():

    total = 0

    if not os.path.exists("logs"):
        return 0

    for arq in os.listdir("logs"):

        caminho = os.path.join("logs", arq)

        with open(caminho, encoding="utf8") as f:
            total += len(f.readlines())

    return total


# =====================================
# CRIA ARQUIVOS
# =====================================

for nome, tamanho in ARQUIVOS:

    caminho = f"files/{nome}.bin"

    if not os.path.exists(caminho):

        print(f"Criando {caminho}")

        criar_arquivo(caminho, tamanho)


# =====================================
# EXECUÇÃO DOS TESTES
# =====================================

for bloco in BLOCOS:

    alterar_bloco(bloco)

    print(f"\n========== BLOCO {bloco} ==========")

    for nome_arq, tamanho in ARQUIVOS:

        caminho = f"files/{nome_arq}.bin"

        for qtd_peers in PEERS:

            print(
                f"\nArquivo={nome_arq}"
                f" | Bloco={bloco}"
                f" | Peers={qtd_peers}"
            )

            limpar_logs()
            limpar_downloads()

            processos = []

            inicio = time.time()

            # Seeder

            processos.append(
                subprocess.Popen(
                    ["python3", "peer.py", "1", caminho]
                )
            )

            time.sleep(2)

            # Leechers

            for peer in range(2, qtd_peers + 1):

                vazio = f"files/vazio{peer}.txt"

                open(vazio, "w").close()

                processos.append(
                    subprocess.Popen(
                        ["python3", "peer.py", str(peer), vazio]
                    )
                )

            terminado = False

            while not terminado:

                terminado = True

                for peer in range(2, qtd_peers + 1):

                    esperado = (
                        f"files/p{peer}/{nome_arq}.bin"
                    )

                    if not os.path.exists(esperado):

                        terminado = False
                        break

                time.sleep(1)

            fim = time.time()

            tempo = fim - inicio

            throughput = tamanho / tempo

            mensagens = contar_mensagens()

            # ===========================
            # IDENTIFICAÇÃO DOS TESTES
            # ===========================

            testes = []

            # Teste 1
            if nome_arq == "20MB" and bloco == 1024:

                testes.append(
                    "Teste 1 - Testar o impacto dos peers"
                )

            # Teste 2
            if nome_arq == "20MB" and qtd_peers == 4:

                testes.append(
                    "Teste 2 - Testar o impacto da fragmentação"
                )

            # Teste 3
            if nome_arq in ["10KB", "20KB"]:

                testes.append(
                    "Teste 3 - Validar transferência rápida de poucos blocos"
                )

            # Teste 4
            if nome_arq in ["1MB", "5MB"]:

                testes.append(
                    "Teste 4 - Validar fragmentação em número razoável de blocos"
                )

            # Teste 5
            if nome_arq in ["10MB", "20MB"]:

                testes.append(
                    "Teste 5 - Testar estabilidade para grandes transferências"
                )

            if not testes:

                testes.append(
                    "Teste Complementar"
                )

            # ===========================
            # ADICIONA UMA LINHA POR TESTE
            # ===========================

            for teste in testes:

                RESULTADOS.append({

                    "teste":
                        teste,

                    "configuracao_vizinhos":
                        "Estática",

                    "arquivo":
                        nome_arq,

                    "tamanho_bytes":
                        tamanho,

                    "bloco":
                        bloco,

                    "peers":
                        qtd_peers,

                    "tempo_s":
                        round(tempo, 3),

                    "mensagens":
                        mensagens,

                    "throughput_Bps":
                        round(throughput, 2)
                })

            for proc in processos:

                try:
                    proc.kill()
                except:
                    pass


# =====================================
# SALVA CSV
# =====================================

df = pd.DataFrame(RESULTADOS)

df.to_csv(
    "resultado_testes.csv",
    index=False,
    sep=";"
)

print("\n===============================")
print("RESULTADOS")
print("===============================")

print(df)

print("\nArquivo gerado:")
print("resultado_testes.csv")