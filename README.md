# stp-root-att-lab
Lab ataque STP Root Bridge


Eunice Y. Francisca Fleming 2024-1185

Enlace de video: https://youtu.be/ZF6JSYBob3U?si=uXY-Sjp3Drg_-LP7

Enlace de Playlist: https://www.youtube.com/playlist?list=PLedgCpC2B7oUOUOG7D6VLYsRR7i7bySIM

---

## Descripción

Script Python que realiza un ataque **STP Root Bridge (Claim Root Attack)**, enviando BPDUs falsos con prioridad 0 para engañar al switch y convertir al atacante en el Root Bridge de la topología STP, redirigiendo todo el tráfico de Capa 2 a través de él.

---

## Requisitos

| Requisito | Detalle |
|-----------|---------|
| Sistema Operativo | Linux (probado en Linux2024 / Debian) |
| Python | 3.x |
| Librería | Scapy (`pip3 install scapy`) |
| Privilegios | root (sudo) |
| Simulador | GNS3 con IOU Cisco + STP habilitado |

---

## Instalación

```bash
pip3 install scapy
```

---

## Uso

```bash
sudo python3 stp_root.py [opciones]
```

### Parámetros

| Parámetro | Descripción | Ejemplo |
|-----------|-------------|---------|
| `-i` / `--iface` | Interfaz de red | `-i eth0` |
| `-p` / `--priority` | Prioridad BPDU (default: 0) | `-p 0` |
| `-t` / `--interval` | Intervalo entre BPDUs (seg) | `-t 2.0` |
| `-c` / `--count` | Número de BPDUs (0=infinito) | `-c 20` |
| `-v` / `--verbose` | Mostrar cada BPDU | `--verbose` |

### Ejemplo

```bash
sudo python3 stp_root.py -i eth0 -p 0 -t 2 -v
```

---

## Topología

<img width="496" height="563" alt="image" src="https://github.com/user-attachments/assets/0b5fef46-0511-4e1a-a841-52abaaf6ccb1" />

### Tabla de Direccionamiento

| Dispositivo | IP | Máscara | Rol |
|-------------|-----|---------|-----|
| IOU1 | — | — | Switch / Root Bridge original |
| PC1 (VPCS) | 10.11.85.10 | /24 | Víctima |
| Linux2024 | 10.11.85.30 | /24 | Atacante |

---

## Verificación

```bash
# En IOU1 — antes del ataque
show spanning-tree vlan 1
# Root ID Priority: 32769, This bridge is the root

# Durante el ataque
show spanning-tree vlan 1
# Root ID Priority: 0, Address: 000c.2902.5d70 (MAC atacante)
```
Antes del ataque

<img width="975" height="731" alt="image" src="https://github.com/user-attachments/assets/086800a6-aefe-4699-b074-d00592846c5b" />

Ejecución del ataque y verificación del spanning-tree


<img width="636" height="366" alt="image" src="https://github.com/user-attachments/assets/af7822c2-1710-46ff-be8a-4c4069c3adac" />


<img width="940" height="474" alt="image" src="https://github.com/user-attachments/assets/05cb6e0d-74fd-4137-bf1b-75835c31d689" />

---

## Contramedida

```bash
# En IOU1 — BPDU Guard
conf t
spanning-tree portfast bpduguard default
interface Ethernet0/0
 spanning-tree portfast
interface Ethernet0/1
 spanning-tree portfast
end
wr

# Verificar
show spanning-tree summary
```

<img width="870" height="571" alt="image" src="https://github.com/user-attachments/assets/d0d5ec2f-3bda-4d68-9985-3a3063b636a6" />

Resultado esperado:
```
%SPANTREE-2-BLOCK_BPDUGUARD: Received BPDU on port Et0/0
with BPDU Guard enabled. Disabling port.
```

<img width="975" height="157" alt="image" src="https://github.com/user-attachments/assets/2ac4fd5c-781e-4203-8a2b-3c23d38e2160" />

<img width="871" height="302" alt="image" src="https://github.com/user-attachments/assets/0fccaea5-f67c-4c33-ba58-23e6572ead98" />

---

## Video

> Enlace al video de demostración: https://youtu.be/ZF6JSYBob3U?si=uXY-Sjp3Drg_-LP7

---

## Documentación

