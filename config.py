HOST = "127.0.0.1"

# Mapeamento de ID para Portas
PEERS = {
    1: 5001,
    2: 5002,
    3: 5003,
    4: 5004
}

# Topologia de vizinhança estática (Linear / Anel Aberto)
VIZINHOS = {
    1: [2],
    2: [1, 3],
    3: [2, 4],
    4: [3]
}

# Modifique este valor para 4096 no Teste de Fragmentação
TAMANHO_BLOCO = 1024