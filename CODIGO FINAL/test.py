import pytest
from unittest.mock import patch
from MIRROR import escanear_red, mostrar_dispositivos

# Simulación de salida de nmap
nmap_output = """Starting Nmap 7.80 ( https://nmap.org ) at 2025-04-12 10:00
Nmap scan report for 192.168.18.75
Host is up (0.0010s latency).
MAC Address: AA:BB:CC:DD:EE:FF (VendorX)
Nmap scan report for 192.168.18.250
Host is up (0.0012s latency).
MAC Address: 11:22:33:44:55:66 (VendorY)
"""

@patch("MIRROR.subprocess.check_output")
def test_escanear_red(mock_subproc):
    mock_subproc.return_value = nmap_output.encode()
    dispositivos = escanear_red("192.168.18.0/24")

    assert len(dispositivos) == 2
    assert dispositivos[0] == ("192.168.18.75", "AA:BB:CC:DD:EE:FF", "VendorX")
    assert dispositivos[1] == ("192.168.18.250", "11:22:33:44:55:66", "VendorY")


def test_mostrar_dispositivos(capsys):
    dispositivos = [
        ("192.168.18.75", "AA:BB:CC:DD:EE:FF", "VendorX"),     # conocida
        ("192.168.18.99", "DE:AD:BE:EF:00:01", "VendorZ")      # desconocida
    ]

    desconocidas = mostrar_dispositivos(dispositivos)
    captured = capsys.readouterr()

    assert "✅ Conocida" in captured.out
    assert "⚠️ DESCONOCIDA" in captured.out
    assert "🚨 ¡ALERTA!" in captured.out
    assert len(desconocidas) == 1
    assert desconocidas[0][0] == "192.168.18.99"
