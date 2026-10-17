"""Testes do scanner de portas TCP com banner grabbing.

Usa um servidor TCP falso local (somente socket, sem rede externa) para
validar porta aberta com banner e porta fechada.
"""

from __future__ import annotations

import socket
import threading

import pytest

from scanner_portas_banner import PortResult, resolve_service, scan_port, scan_ports


def _run_banner_server(banner: bytes, stop: threading.Event, ready: threading.Event, holder: list[int]) -> None:
    """Servidor TCP falso: aceita uma conexao, envia o banner e fecha."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 0))
    server.listen(1)
    server.settimeout(0.5)
    holder.append(server.getsockname()[1])
    ready.set()
    while not stop.is_set():
        try:
            conn, _ = server.accept()
        except socket.timeout:
            continue
        with conn:
            try:
                conn.sendall(banner)
            except OSError:
                pass
    server.close()


@pytest.fixture
def banner_port() -> int:
    """Porta localhost com um servidor falso que envia um banner fixo."""
    stop = threading.Event()
    ready = threading.Event()
    holder: list[int] = []
    thread = threading.Thread(
        target=_run_banner_server,
        args=(b"SSH-2.0-fake.local\r\n", stop, ready, holder),
        daemon=True,
    )
    thread.start()
    ready.wait(timeout=5)
    try:
        yield holder[0]
    finally:
        stop.set()
        thread.join(timeout=2)


def test_scan_port_open_with_banner(banner_port: int) -> None:
    resultado = scan_port("127.0.0.1", banner_port, timeout=2.0)

    assert isinstance(resultado, PortResult)
    assert resultado.port == banner_port
    assert resultado.is_open is True
    assert resultado.banner == "SSH-2.0-fake.local"
    assert isinstance(resultado.service, str)


def test_scan_port_closed() -> None:
    resultado = scan_port("127.0.0.1", 59999, timeout=1.0)

    assert resultado.is_open is False
    assert resultado.banner is None
    assert isinstance(resultado.service, str)


def test_scan_ports_returns_list(banner_port: int) -> None:
    resultados = scan_ports("127.0.0.1", [banner_port, 59999], timeout=2.0)

    assert isinstance(resultados, list)
    assert len(resultados) == 2
    assert resultados[0].is_open is True
    assert resultados[0].banner == "SSH-2.0-fake.local"
    assert resultados[1].is_open is False
    assert resultados[1].banner is None


def test_resolve_service_known_port() -> None:
    assert resolve_service(22) == "ssh"


def test_resolve_service_unknown_port() -> None:
    assert resolve_service(59999) == "desconhecido"
