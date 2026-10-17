# BRIEF — scanner-portas-banner

## Entregas
- `pyproject.toml` — metadados do projeto, entry point de console e configuração do pytest (`pythonpath = ["src"]`, `testpaths = ["tests"]`)
- `src/scanner_portas_banner/__init__.py` — exporta `PortResult`, `resolve_service`, `scan_port`, `scan_ports`
- `src/scanner_portas_banner/scanner.py` — scanner TCP: `scan_port`, `scan_ports`, `resolve_service`, `_grab_banner`; dataclass `PortResult`; apenas stdlib (`socket`), sem dependências externas
- `src/scanner_portas_banner/__main__.py` — CLI (alvo, `--portas`, `--timeout`)
- `tests/test_scanner.py` — suíte pytest com servidor TCP falso local (socket, sem rede externa)
- `README.md` — documentação bilíngue PT-BR + EN (título, descrição, como usar, testes, licença MIT, autor Kelvin Oliveira)
- `BRIEF.md` — este arquivo

## Como verificar
1. Entre na pasta do projeto (`scanner-portas-banner/`).
2. Rode `python -m pytest -q`. O `pyproject.toml` já configura `src/` no caminho de busca do pytest.
   Resultado esperado: `5 passed`.
3. Rode manualmente: `python -m scanner_portas_banner --portas 22,80 127.0.0.1`.

## Critérios de aceitação (do PLANO_50_PROJETOS.md)
- Lista de portas/serviços com banner grabbing: implementada em `scanner.py` e exposta pelo CLI.
- Testes que passem: suíte pytest passa (5 testes).
- README PT-BR + EN completo: título, descrição, como usar, testes, licença MIT, autor Kelvin Oliveira.

Owner da validação: o gerente de fluxo de trabalho (workflow manager).
