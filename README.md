# MIRROR

## Descripción

MIRROR es una herramienta de seguridad de red ligera diseñada para monitorizar dispositivos conectados a redes especificadas. El sistema escanea periódicamente las redes configuradas y alerta cuando detecta dispositivos no autorizados, proporcionando una capa adicional de seguridad para entornos domésticos y pequeñas empresas.

## 🔑 Características principales

- **Monitorización automatizada**: Escaneo periódico de rangos de red configurables
- **Detección de intrusos**: Alerta sobre dispositivos desconocidos conectados a la red
- **Identificación de dispositivos**: Muestra dirección IP, MAC y fabricante de cada dispositivo
- **Operación continua**: Funcionamiento en segundo plano con intervalos configurables

## 🛠️ Requisitos

- Python 3.6+
- Nmap
- Privilegios de administrador/root
- Sistema operativo compatible (Linux/macOS/Windows con WSL)
- Se recomienda usar KALI Linux

## 🚀 Instalación

1. Clona el repositorio:
```bash
git clone https://github.com/26Alejandro/MIRROR.git
cd MIRRoR
```

2. Instala las dependencias de sistema:
```bash
# En Debian/Ubuntu
sudo apt-get install nmap

# En Fedora/CentOS
sudo dnf install nmap

# En macOS
brew install nmap
```

## ⚙️ Configuración

Edita el archivo principal para personalizar:

- `INTERVALO`: Tiempo entre escaneos (en segundos)
- `redes`: Lista de rangos de red a monitorizar
- `ips_conocidas`: Lista de IPs de dispositivos autorizados

```python
# Ejemplo de configuración
INTERVALO = 300  # 5 minutos
redes = ['192.168.1.0/24', '10.0.0.0/24']
ips_conocidas = [
    '192.168.1.1',  # Router
    '192.168.1.10', # PC principal
    '192.168.1.20'  # Servidor NAS
]
```

## 📊 Uso

Ejecuta el script con privilegios de administrador:

```bash
sudo python3 MIRROR.py
```

El sistema comenzará a escanear las redes configuradas y mostrará:
- Listado de dispositivos detectados
- Estado de cada dispositivo (conocido/desconocido)
- Alertas cuando se detecten dispositivos no autorizados

## 🔒 Consideraciones de privacidad y seguridad

- Esta herramienta debe utilizarse únicamente en redes donde tengas autorización para realizar escaneos
- Los escaneos de red pueden ser detectados por sistemas de seguridad más avanzados
- No utilices esta herramienta en redes públicas o en entornos de producción sin las autorizaciones adecuadas

## 📝 Notas adicionales

- Los resultados pueden variar según la configuración de la red y los firewalls
- Algunos dispositivos pueden no responder a los escaneos por políticas de seguridad
- La precisión en la identificación de fabricantes depende de la base de datos de Nmap

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría implementar.

## 📜 Licencia

Este proyecto está licenciado bajo [MIT License](LICENSE).
