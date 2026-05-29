# Transferência de Arquivos Peer-to-Peer

Trabalho Prático 2 — Sistemas Distribuídos (CEFET-MG)
Nomes: Aira Winner e Arthur Secundino

## Pré-requisitos

* Python 3.10 ou superior

Verifique a instalação:

```bash
python --version
```

---

## Estrutura do Projeto

```text
.
├── peer.py
├── config.py
├── metadata.py
├── protocolo.py
├── utils.py
├── files/
├── logs/
├── tabelas/
├── graficos/
└── scripts/
```

---

## Execução Automática dos Testes

O projeto possui scripts para executar automaticamente toda a bateria de testes definida no enunciado, gerar tabelas e produzir gráficos para análise dos resultados.

### 1. Executar todos os testes

```bash
python scripts/executar_testes.py
```

Esse script:

* Executa todos os cenários de teste definidos no trabalho;
* Varia a quantidade de peers (2 e 4);
* Varia o tamanho dos blocos (1024 e 4096 bytes);
* Testa diferentes tamanhos de arquivos;
* Mede tempo de transferência;
* Conta a quantidade de mensagens trocadas;
* Calcula o throughput;
* Gera o arquivo `resultado_testes.csv`.

---

### 2. Gerar os gráficos

```bash
python scripts/gerar_graficos.py
```

Os gráficos serão salvos na pasta:

```text
graficos/
```

Incluindo:

```text
teste1_peers.png
teste2_fragmentacao.png
teste3_pequenos.png
teste4_medios.png
teste5_grandes.png
teste6_protocolo_p2p.png
```

---

### 3. Gerar as tabelas formatadas

```bash
python scripts/tabelacores.py
```

As tabelas serão geradas em formato PNG e salvas na pasta:

```text
tabelas/
```

Exemplo:

```text
tabela_resultados_parte_1.png
tabela_resultados_parte_2.png
tabela_resultados_parte_3.png
```

---

## Execução Manual dos Peers

### Executando o Seeder

O Seeder é o peer que possui inicialmente o arquivo completo.

Exemplo:

```bash
python peer.py 1 files/arquivo.bin
```

---

### Executando os Leechers

Em terminais separados:

Peer 2:

```bash
python peer.py 2 files/vazio.txt
```

Peer 3:

```bash
python peer.py 3 files/vazio.txt
```

Peer 4:

```bash
python peer.py 4 files/vazio.txt
```

---

## Exemplo de Teste com 2 Peers

Terminal 1:

```bash
python peer.py 1 files/arquivo.bin
```

Terminal 2:

```bash
python peer.py 2 files/vazio.txt
```

---

## Exemplo de Teste com 4 Peers

Terminal 1:

```bash
python peer.py 1 files/arquivo.bin
```

Terminal 2:

```bash
python peer.py 2 files/vazio.txt
```

Terminal 3:

```bash
python peer.py 3 files/vazio.txt
```

Terminal 4:

```bash
python peer.py 4 files/vazio.txt
```

---

## Arquivos Gerados

Após a conclusão da transferência, os arquivos recebidos e remontados são armazenados em:

```text
files/p2/
files/p3/
files/p4/
```

---

## Logs de Execução

Todos os eventos relevantes da execução são registrados na pasta:

```text
logs/
```

Os logs incluem informações como:

* Inicialização dos peers;
* Recebimento de metadados;
* Download de blocos;
* Compartilhamento de blocos;
* Verificação de integridade.

---

## Verificação de Integridade

Ao final da transferência, cada peer:

1. Remonta o arquivo utilizando todos os blocos recebidos;
2. Calcula o hash SHA-256 do arquivo reconstruído;
3. Compara o resultado com o hash SHA-256 do arquivo original informado nos metadados.

Caso os hashes sejam iguais, a transferência é considerada íntegra e bem-sucedida.

---

## Métricas Avaliadas

Os testes realizados coletam as seguintes métricas:

* Tempo total de transferência;
* Quantidade de mensagens trocadas entre os peers;
* Throughput (Bytes por segundo);
* Integridade do arquivo transferido.

Essas métricas são utilizadas para avaliar o impacto:

* Da quantidade de peers;
* Do tamanho dos blocos;
* Do tamanho dos arquivos;
* Da comunicação P2P baseada em vizinhança estática.
