"""Varredura de portas TCP com captura de banner.

Determinístico e sem dependências externas: usa apenas a biblioteca
padrão ``socket``. Um alvo e uma lista de portas produzem uma lista de
resultados contendo porta aberta/fechada, serviço e banner.
"""

from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Optional

# Mapeamento porta -> servico para portas comuns quando o SO nao as
# conhece via getservbyport.
COMMON_SERVICES: dict[int, str] = {
    21: "ftp",
    22: "ssh",
    23: "telnet",
    25: "smtp",
    53: "dns",
    80: "http",
    110: "pop3",
    139: "netbios-ssn",
    143: "imap",
    443: "https",
    445: "microsoft-ds",
    3306: "mysql",
    3389: "rdp",
    5432: "postgresql",
    5900: "vnc",
    6379: "redis",
    8080: "http-proxy",
    8443: "https-alt",
    27017: "mongodb",
}

DEFAULT_TIMEOUT = 1.0
DEFAULT_HOST = "127.0.0.1"


@dataclass(frozen=True)
class PortResult:
    """Resultado da varredura de uma única porta TCP.

    Attributes:
        port: Numero da porta varrida.
        is_open: True se a conexao TCP foi estabelecida.
        service: Nome do servico associado a porta.
        banner: Conteudo lido do socket apos conectar, ou None.
    """

    port: int
    is_open: bool
    service: str
    banner: Optional[str] = None


def resolve_service(port: int) -> str:
    """Retorna o nome do servico TCP da porta.

    Tenta primeiro o servico do sistema (tipo /etc/services) e, em
    seguida, o mapeamento interno de portas comuns. Retorna
    "desconhecido" quando nao ha mapeamento.
    """
    try:
        return socket.getservbyport(port, "tcp")
    except OSError:
        return COMMON_SERVICES.get(port, "desconhecido")


def _grab_banner(sock: socket.socket, timeout: float) -> Optional[str]:
    """Lê o banner do socket ja conectado, sem bloquear para sempre."""
    try:
        data = sock.recv(4096)
    except (OSError, socket.timeout):
        return None
    if not data:
        return None
    return data.decode("utf-8", errors="replace").strip()


def scan_port(host: str, port: int, timeout: float = DEFAULT_TIMEOUT) -> PortResult:
    """Varre uma única porta TCP e tenta capturar o banner.

    Args:
        host: Alvo (endereco IPv4 ou nome de host).
        port: Porta TCP a varrer.
        timeout: Tempo limite da conexao e do recv, em segundos.

    Returns:
        PortResult com o estado da porta, servico e banner.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        sock.connect((host, port))
        banner = _grab_banner(sock, timeout)
        return PortResult(
            port=port,
            is_open=True,
            service=resolve_service(port),
            banner=banner,
        )
    except (OSError, socket.timeout):
        return PortResult(
            port=port,
            is_open=False,
            service=resolve_service(port),
            banner=None,
        )
    finally:
        sock.close()


def scan_ports(
    host: str,
    ports: list[int],
    timeout: float = DEFAULT_TIMEOUT,
) -> list[PortResult]:
    """Varre varias portas TCP no host e retorna os resultados.

    Args:
        host: Alvo da varredura.
        ports: Lista de portas TCP.
        timeout: Tempo limite de cada conexao, em segundos.

    Returns:
        Lista de PortResult, uma por porta informada.
    """
    return [scan_port(host, port, timeout) for port in ports]
