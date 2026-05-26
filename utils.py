import hashlib
import os

def calcular_sha256(caminho):
    """Calcula o hash SHA256 de um arquivo para validação de integridade."""
    sha256 = hashlib.sha256()
    try:
        with open(caminho, "rb") as f:
            while True:
                dados = f.read(4096)
                if not dados:
                    break
                sha256.update(dados)
        return sha256.hexdigest()
    except FileNotFoundError:
        return ""

def salvar_log(peer_id, mensagem):
    """Registra eventos em arquivos de log na pasta /logs."""
    os.makedirs("logs", exist_ok=True)
    caminho = f"logs/peer{peer_id}.log"
    with open(caminho, "a", encoding="utf-8") as f:
        f.write(mensagem + "\n")