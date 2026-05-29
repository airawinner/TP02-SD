# Transferência de Arquivos Peer-to-Peer

Trabalho Prático 2 - Sistemas Distribuídos (CEFET-MG)

## Pré-requisitos

- Python 3.10 ou superior

Verifique a instalação:

```bash
python --version
```

## Estrutura do Projeto

```text
.
├── peer.py
├── config.py
├── metadata.py
├── protocolo.py
├── utils.py
├── files/
└── logs/
```

## Executando o Seeder

O Seeder é o peer que possui o arquivo original.

Exemplo:

```bash
python peer.py 1 files/arquivo.bin
```

## Executando os Leechers

Em outros terminais:

```bash
python peer.py 2 files/vazio.txt
```

```bash
python peer.py 3 files/vazio.txt
```

```bash
python peer.py 4 files/vazio.txt
```

## Exemplo de Teste com 2 Peers

Terminal 1:

```bash
python peer.py 1 files/arquivo.bin
```

Terminal 2:

```bash
python peer.py 2 files/vazio.txt
```

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

## Arquivos Gerados

Os arquivos recebidos são remontados em:

```text
files/p2/
files/p3/
files/p4/
```

Os logs de execução são armazenados em:

```text
logs/
```

## Verificação de Integridade

Ao final da transferência, cada peer calcula o hash SHA-256 do arquivo recebido e compara com o hash do arquivo original, garantindo a integridade dos dados transferidos.
