import os
import math
from config import TAMANHO_BLOCO
from utils import calcular_sha256

def gerar_metadata(caminho):
    """Gera o dicionário de metadados obrigatório do arquivo."""
    tamanho = os.path.getsize(caminho)
    total_blocos = math.ceil(tamanho / TAMANHO_BLOCO)
    
    return {
        "nome": os.path.basename(caminho),
        "tamanho": tamanho,
        "total_blocos": total_blocos,
        "sha256": calcular_sha256(caminho)
    }