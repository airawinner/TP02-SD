import socket
import threading
import os
import sys
import time

from config import *
import protocolo
from metadata import gerar_metadata
from utils import calcular_sha256, salvar_log

if len(sys.argv) < 3:
    print("Uso correto: python peer.py <peer_id> <caminho_do_arquivo_ou_vazio>")
    sys.exit()

peer_id = int(sys.argv[1])
arquivo_alvo = sys.argv[2]

MINHA_PORTA = PEERS[peer_id]
MEUS_VIZINHOS = VIZINHOS[peer_id]

meus_blocos = {}
metadata = None
lock = threading.Lock()

def dividir_arquivo(caminho):
    blocos = []
    with open(caminho, "rb") as f:
        while True:
            bloco = f.read(TAMANHO_BLOCO)
            if not bloco:
                break
            blocos.append(bloco)
    return blocos

def montar_arquivo():
    pasta = f"files/p{peer_id}"
    os.makedirs(pasta, exist_ok=True)
    
    nome_saida = metadata["nome"]
    caminho_saida = f"{pasta}/{nome_saida}"
    
    with open(caminho_saida, "wb") as f:
        total = metadata["total_blocos"]
        for i in range(total):
            f.write(meus_blocos[i])
            
    print(f"\n[Peer {peer_id}] -> Arquivo remontado localmente!")
    hash_final = calcular_sha256(caminho_saida)
    print(f"[Peer {peer_id}] -> SHA256 Final: {hash_final}")
    
    if hash_final == metadata["sha256"]:
        print(f"[Peer {peer_id}] -> INTEGRIDADE VERIFICADA: SUCESSO ")
        salvar_log(peer_id, "Integridade OK")
    else:
        print(f"[Peer {peer_id}] -> INTEGRIDADE CORROMPIDA: ERRO ")
        salvar_log(peer_id, "ERRO DE INTEGRIDADE")

def tratar_cliente(conn, addr):
    global metadata
    try:
        conn.settimeout(5.0)
        dados = protocolo.ler_mensagem(conn)
        if not dados:
            return

        tipo = dados["tipo"]

        if tipo == "META":
            with lock:
                if metadata is not None:
                    resposta = protocolo.criar_meta_resposta(metadata)
                    protocolo.enviar_mensagem(conn, resposta)

        elif tipo == "GET":
            indice = dados["indice"]
            bloco_enviar = None
            
            with lock:
                if indice in meus_blocos:
                    bloco_enviar = meus_blocos[indice]
            
            if bloco_enviar:
                resposta = protocolo.criar_bloco(indice, bloco_enviar)
                protocolo.enviar_mensagem(conn, resposta)
                log = f"Enviou bloco {indice} para vizinho no endereço {addr}"
                salvar_log(peer_id, log)
                
    except Exception:
        pass
    finally:
        conn.close()

def servidor():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, MINHA_PORTA))
    s.listen()
    print(f"[Servidor] Peer {peer_id} online na porta {MINHA_PORTA}")
    
    while True:
        try:
            conn, addr = s.accept()
            threading.Thread(target=tratar_cliente, args=(conn, addr), daemon=True).start()
        except Exception:
            pass

def solicitar_metadata(porta):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((HOST, porta))
        protocolo.enviar_mensagem(s, protocolo.criar_meta())
        dados = protocolo.ler_mensagem(s)
        s.close()
        if dados and dados["tipo"] == "META_RESPOSTA":
            return dados["metadata"]
    except Exception:
        return None

def solicitar_bloco(porta, indice):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.5)
        s.connect((HOST, porta))
        protocolo.enviar_mensagem(s, protocolo.criar_get(indice))
        dados = protocolo.ler_mensagem(s)
        s.close()
        if dados and dados["tipo"] == "BLOCK":
            return bytes.fromhex(dados["dados"])
    except Exception:
        return None

def baixar_arquivo():
    global metadata
    
    # Busca de Metadados
    while metadata is None:
        for vizinho in MEUS_VIZINHOS:
            porta = PEERS[vizinho]
            meta = solicitar_metadata(porta)
            if meta is not None:
                with lock:
                    metadata = meta
                print(f"[Peer {peer_id}] Metadados do arquivo obtidos com sucesso.")
                salvar_log(peer_id, "Metadata recebida")
                break
        if metadata is None:
            time.sleep(1)

    total_blocos = metadata["total_blocos"]

    # Download Compartilhado P2P (Leecher vira Seeder bloco a bloco)
    while True:
        with lock:
            concluido = len(meus_blocos) >= total_blocos
        if concluido:
            break

        for indice in range(total_blocos):
            with lock:
                ja_tem = indice in meus_blocos
            if ja_tem:
                continue

            for vizinho in MEUS_VIZINHOS:
                porta = PEERS[vizinho]
                dados = solicitar_bloco(porta, indice)
                if dados is not None:
                    with lock:
                        meus_blocos[indice] = dados
                    print(f"[Peer {peer_id}] Baixou bloco {indice}/{total_blocos-1} do Peer {vizinho}")
                    salvar_log(peer_id, f"Recebeu bloco {indice} do peer {vizinho}")
                    break 

        time.sleep(0.05)

    montar_arquivo()

def main():
    global metadata
    
    # Inicia Servidor em background (Garante a Simetria do Nó)
    threading.Thread(target=servidor, daemon=True).start()
    time.sleep(0.5)

    # Verifica se este nó inicia possuindo o arquivo original (Seeder)
    if os.path.exists(arquivo_alvo) and os.path.getsize(arquivo_alvo) > 0:
        metadata = gerar_metadata(arquivo_alvo)
        blocos = dividir_arquivo(arquivo_alvo)
        with lock:
            for i, b in enumerate(blocos):
                meus_blocos[i] = b
                
        print(f"[Peer {peer_id}] Modo SEEDER Inicial. Carregados {len(blocos)} blocos.")
        print(f"[Peer {peer_id}] SHA256 Original: {metadata['sha256']}")
        salvar_log(peer_id, f"Seeder iniciado com {len(blocos)} blocos")
    else:
        print(f"[Peer {peer_id}] Modo LEECHER Inicial. Aguardando rede...")
        baixar_arquivo()

    # Mantém o processo principal vivo permitindo uploads contínuos
    while True:
        time.sleep(1)

if __name__ == "__main__":
    main()