"""Scanner de portas TCP com banner grabbing."""

from .scanner import PortResult, resolve_service, scan_port, scan_ports

__all__ = ["PortResult", "resolve_service", "scan_port", "scan_ports"]
__version__ = "0.1.0"
