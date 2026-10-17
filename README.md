# scanner-portas-banner

Scanner de portas TCP com banner grabbing / TCP port scanner with banner grabbing

## Português

### O que faz
Varre portas TCP de um alvo (default: 127.0.0.1) e, para cada porta aberta, informa o serviço e captura o banner que o servidor envia logo após a conexão. Útil para reconhecimento de rede local e testes de serviços próprios. Escrito em Python, depende apenas da biblioteca padrão (`socket`). Sem pacotes externos.

### Como usar
Do diretório do projeto:

python -m pytest -q   # roda os testes (o pyproject.toml coloca src/ no caminho do pytest)

python -m scanner_portas_banner --portas 22,80,443 127.0.0.1

Saída de exemplo:
porta 22: aberta | serviço: ssh | banner: SSH-2.0-OpenSSH_8.9
porta 80: fechada | serviço: http
porta 443: fechada | serviço: https

1 porta(s) aberta(s) de 3 varrida(s).

Opções:
  host     Alvo (default: 127.0.0.1)
  --portas Portas, ex: '22,80,443' ou '1-1024' (default: 1-1024)
  --timeout Tempo limite da conexão em segundos (default: 1.0)

Depois de instalar o pacote (`pip install -e .`), use o comando direto:

scanner-portas-banner --portas 1-1024 --timeout 0.5 127.0.0.1

### Testes
O projeto usa pytest. Na raiz do repositório:

python -m pytest -q

O pyproject.toml já adiciona src/ ao caminho de busca do pytest. Os testes sobem um servidor TCP falso local (somente socket, sem rede externa) e cobrem porta aberta com banner, porta fechada e resolução de serviço.

### Licença
MIT.

### Autor
Kelvin Oliveira

## English

### What it does
Scans TCP ports on a target (default: 127.0.0.1) and, for each open port, reports the service and grabs the banner the server sends right after connecting. Useful for local network reconnaissance and testing your own services. Written in Python, standard library only (`socket`). No external packages.

### How to use
From the project directory:

python -m pytest -q   # runs the test suite (pyproject sets pythonpath=src)

python -m scanner_portas_banner --ports 22,80,443 127.0.0.1

Example output:
port 22: open | service: ssh | banner: SSH-2.0-OpenSSH_8.9
port 80: closed | service: http
port 443: closed | service: https

1 open port(s) out of 3 scanned.

Options:
  host      Target (default: 127.0.0.1)
  --ports   Ports, e.g. '22,80,443' or '1-1024' (default: 1-1024)
  --timeout Connection timeout in seconds (default: 1.0)

After installing the package (`pip install -e .`), run the console command:

scanner-portas-banner --ports 1-1024 --timeout 0.5 127.0.0.1

### Tests
The project uses pytest. At the repository root:

python -m pytest -q

pyproject.toml already adds src/ to pytest's module path. Tests start a local fake TCP server (socket only, no external network) and cover open port with banner, closed port, and service resolution.

### License
MIT.

### Author
Kelvin Oliveira
