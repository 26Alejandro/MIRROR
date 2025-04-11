import subprocess
import time
import re
import os
import sys

# Configuración
INTERVALO = 60
redes = ['10.0.2.0/24', '192.168.18.0/24']
# Define aquí las IPs conocidas directamente en el código
ips_conocidas = [
    '192.168.18.75',
    # Agrega más IPs conocidas aquí
]


def escanear_red(netrange):
    """Escanea una red usando nmap y devuelve los dispositivos detectados"""
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


def mostrar_dispositivos(dispositivos, detectar_desconocidos=True):
    """Muestra los dispositivos detectados y alerta de IPs desconocidas"""
    if not dispositivos:
        print("❌ No se encontraron dispositivos.")
        return []

    print("📋 Dispositivos encontrados:")
    ips_desconocidas = []

    for ip, mac, vendor in dispositivos:
        # Extraer solo la dirección IP si tiene un hostname
        ip_addr = ip
        if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
            ip_match = re.search(r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)', ip)
            if ip_match:
                ip_addr = ip_match.group(1)

        # Verificar si la IP es conocida
        es_conocida = ip_addr in ips_conocidas
        estado = "✅ Conocida" if es_conocida else "⚠️ DESCONOCIDA"

        if not es_conocida and detectar_desconocidos:
            ips_desconocidas.append((ip, mac, vendor))

        print(f"IP: {ip} | MAC: {mac} | Descripción: {vendor} | {estado}")

    # Lanzar alerta para IPs desconocidas
    if ips_desconocidas and detectar_desconocidos:
        print("\n🚨 ¡ALERTA! 🚨 Se detectaron dispositivos desconocidos:")
        for ip, mac, vendor in ips_desconocidas:
            print(f"  → IP: {ip} | MAC: {mac} | Descripción: {vendor}")

        # Opcional: Sonido de alerta
        print('\a')  # Beep de alerta

        # La opción de agregar automáticamente IPs desconocidas también se puede configurar aquí
        AGREGAR_DESCONOCIDAS_AUTOMATICAMENTE = False  # Cambia a True si quieres agregar automáticamente

        if AGREGAR_DESCONOCIDAS_AUTOMATICAMENTE:
            for ip, _, _ in ips_desconocidas:
                # Extraer solo la dirección IP si tiene un hostname
                ip_addr = ip
                if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip):
                    ip_match = re.search(r'\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)', ip)
                    if ip_match:
                        ip_addr = ip_match.group(1)

                if ip_addr not in ips_conocidas:
                    ips_conocidas.append(ip_addr)
            print(f"✅ IPs agregadas automáticamente a la lista de conocidas. Total: {len(ips_conocidas)}")

    return ips_desconocidas


def verificar_root():
    """Verifica si el script se ejecuta con privilegios de root"""
    if os.geteuid() != 0:
        print("⚠️ Este script debe ejecutarse como root. Usa: sudo python3 nombre_script.py")
        sys.exit(1)


def main():
    verificar_root()

    # Muestra la configuración actual
    print("\n=== CONFIGURACIÓN ===")
    print(f"Redes a escanear: {', '.join(redes)}")
    print(f"IPs conocidas configuradas: {len(ips_conocidas)}")
    print(f"Intervalo de escaneo: {INTERVALO} segundos")
    print("====================\n")

    # Bucle principal de monitorización
    while True:
        print("\n============================")
        print("🛰 Escaneo de red en curso")
        print("============================")

        alguna_desconocida = False
        for red in redes:
            dispositivos = escanear_red(red)
            desconocidas = mostrar_dispositivos(dispositivos)
            if desconocidas:
                alguna_desconocida = True

        if not alguna_desconocida:
            print("\n✅ No se detectaron dispositivos desconocidos en este escaneo.")

        print(f"\n⌛ Esperando {INTERVALO} segundos antes del próximo escaneo...\n")
        time.sleep(INTERVALO)


if __name__ == "__main__":
    main()