"""Interface de linha de comando do scanner de portas."""

from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .scanner import DEFAULT_HOST, DEFAULT_TIMEOUT, scan_ports


def _parse_ports(spec: str) -> list[int]:
    """Converte '22,80,443' ou '1-1024' (ou misto) em lista de portas."""
    ports: list[int] = []
    for part in spec.replace(" ", "").split(","):
        if not part:
            continue
        if "-" in part:
            start_s, end_s = part.split("-", 1)
            start, end = int(start_s), int(end_s)
            if not (0 < start <= end < 65536):
                raise ValueError(f"intervalo de portas invalido: {part}")
            ports.extend(range(start, end + 1))
        else:
            port = int(part)
            if not (0 < port < 65536):
                raise ValueError(f"porta invalida: {port}")
            ports.append(port)
    return ports


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scanner de portas TCP com banner grabbing.",
    )
    parser.add_argument(
        "host",
        nargs="?",
        default=DEFAULT_HOST,
        help="Alvo (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--ports",
        default="1-1024",
        help="Portas, ex: '22,80,443' ou '1-1024' (default: 1-1024)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=DEFAULT_TIMEOUT,
        help="Tempo limite de conexao em segundos (default: 1.0)",
    )
    args = parser.parse_args(argv)

    try:
        ports = _parse_ports(args.ports)
    except ValueError as exc:
        print(f"erro: {exc}", file=sys.stderr)
        return 2

    resultados = scan_ports(args.host, ports, args.timeout)
    abertos = [r for r in resultados if r.is_open]
    for r in resultados:
        banner = f" | banner: {r.banner}" if r.banner else ""
        print(
            f"porta {r.port}: {'aberta' if r.is_open else 'fechada'} "
            f"| servico: {r.service}{banner}"
        )
    print(f"\n{len(abertos)} porta(s) aberta(s) de {len(resultados)} varrida(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
