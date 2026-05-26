import json
import struct

def enviar_mensagem(sock, dados_dict):
    """Prefixa a mensagem com 4 bytes contendo o tamanho para evitar fragmentação no TCP."""
    payload = json.dumps(dados_dict).encode('utf-8')
    header = struct.pack('!I', len(payload))
    sock.sendall(header + payload)

def ler_mensagem(sock):
    """Lê estritamente o cabeçalho e consome o tamanho exato do payload do buffer."""
    try:
        header = sock.recv(4)
        if not header or len(header) < 4:
            return None
        
        tamanho_payload = struct.unpack('!I', header)[0]
        dados = bytearray()
        
        while len(dados) < tamanho_payload:
            pacote = sock.recv(tamanho_payload - len(dados))
            if not pacote:
                return None
            dados.extend(pacote)
            
        return json.loads(dados.decode('utf-8'))
    except Exception:
        return None

def criar_get(indice):
    return {"tipo": "GET", "indice": indice}

def criar_bloco(indice, dados):
    return {"tipo": "BLOCK", "indice": indice, "dados": dados.hex()}

def criar_meta():
    return {"tipo": "META"}

def criar_meta_resposta(metadata):
    return {"tipo": "META_RESPOSTA", "metadata": metadata}