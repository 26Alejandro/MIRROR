import subprocess
import re
import os
import sys

redes = ['10.0.2.0/24', '192.168.18.0/24']

def escanear_red(netrange):
    print(f"\n🔍 Escaneando red: {netrange}...")
    try:
        resultado = subprocess.check_output(['nmap', '-sn', netrange], stderr=subprocess.DEVNULL).decode()

        dispositivos = []
        lineas = resultado.split('\n')
        ip, mac, vendor = None, None, None

        for linea in lineas:
            if "Nmap scan report for" in linea:
                if ip:
                    dispositivos.append((ip, mac or "No detectada", vendor or "Desconocido"))
                ip = re.search(r'Nmap scan report for (.+)', linea).group(1)
                mac, vendor = None, None
            elif "MAC Address:" in linea:
                mac_vendor_match = re.search(r'MAC Address: ([\w:]+)( \((.*?)\))?', linea)
                if mac_vendor_match:
                    mac = mac_vendor_match.group(1)
                    vendor = mac_vendor_match.group(3)

        if ip:
            dispositivos.append((ip, mac or "No detectada", vendor or "Desconocido"))

        return dispositivos
    except Exception as e:
        print(f"❌ Error al escanear la red {netrange}: {e}")
        return []

def mostrar_dispositivos(dispositivos):
    if dispositivos:
        print("📋 Dispositivos encontrados:")
        for ip, mac, vendor in dispositivos:
            print(f"IP: {ip} | MAC: {mac} | Descripción: {vendor}")
    else:
        print("❌ No se encontraron dispositivos.")

def verificar_root():
    if os.geteuid() != 0:
        print("⚠️ Este script debe ejecutarse como root. Usa: sudo python3 nombre_script.py")
        sys.exit(1)

def main():
    verificar_root()

    print("\n============================")
    print("🛰 Escaneo de red en curso")
    print("============================")
    for red in redes:
        dispositivos = escanear_red(red)
        mostrar_dispositivos(dispositivos)

if __name__ == "__main__":
    main()
