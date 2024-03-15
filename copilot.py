import socket
import threading
import time
import queue

# Define uma classe para representar um relógio vetorial
class RelogioVetorial:
    def __init__(self, num_processos, id_processo):
        self.relogio = [0] * num_processos
        self.id_processo = id_processo

    def incrementa(self):
        self.relogio[self.id_processo] += 1

    def atualiza(self, outro):
        for i in range(len(self.relogio)):
            self.relogio[i] = max(self.relogio[i], outro[i])

    def __str__(self):
        return str(self.relogio)

# Define uma classe para representar um processo com um relógio vetorial
class Processo:
    def __init__(self, id_processo, num_processos, porta):
        self.id_processo = id_processo
        self.relogio_vetorial = RelogioVetorial(num_processos, id_processo)
        self.porta = porta
        self.fila_mensagens = queue.PriorityQueue()
        self.soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soquete.bind(('localhost', porta))
        self.soquete.listen(5)
        self.conexoes = []

    def envia_mensagem(self, mensagem, atraso, porta_destino):
        time.sleep(atraso)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', porta_destino))
            self.relogio_vetorial.incrementa()
            s.sendall(f"{','.join(map(str, self.relogio_vetorial.relogio))} {mensagem}".encode())

    def recebe_mensagem(self, conn, addr):
        while True:
            data = conn.recv(1024)
            if not data:
                break
            mensagem = data.decode()
            relogio_vetorial, mensagem = mensagem.split(' ', 1)
            relogio_vetorial = [int(x) for x in relogio_vetorial.split(',')]
            if relogio_vetorial > self.relogio_vetorial.relogio:
                self.fila_mensagens.put((relogio_vetorial, mensagem))
            else:
                self.relogio_vetorial.atualiza(relogio_vetorial)
                print(f"Processo {self.id_processo} recebeu a mensagem: {mensagem} com relógio: {self.relogio_vetorial}")

    def inicia_escuta(self):
        while True:
            conn, addr = self.soquete.accept()
            self.conexoes.append(conn)
            threading.Thread(target=self.recebe_mensagem, args=(conn, addr)).start()

    def verifica_fila_mensagens(self):
        while not self.fila_mensagens.empty():
            relogio_vetorial, mensagem = self.fila_mensagens.get()
            if relogio_vetorial > self.relogio_vetorial.relogio:
                self.fila_mensagens.put((relogio_vetorial, mensagem))
            else:
                self.relogio_vetorial.atualiza(relogio_vetorial)
                print(f"Processo {self.id_processo} recebeu a mensagem atrasada: {mensagem} com relógio: {self.relogio_vetorial}")

# Exemplo de uso
if __name__ == "__main__":
    num_processos = 3
    portas_processos = [5000, 5001, 5002]

    processos = [Processo(i, num_processos, portas_processos[i]) for i in range(num_processos)]

    for processo in processos:
        tcp_server_thread = threading.Thread(target=processo.inicia_escuta)
        tcp_server_thread.daemon = True
        tcp_server_thread.start()

    # Simula o envio de mensagens com atrasos
    processos[0].envia_mensagem("Olá do processo 0", 2, portas_processos[1])
    processos[1].envia_mensagem("Olá do processo 1", 1, portas_processos[2])
    processos[2].envia_mensagem("Olá do processo 2", 3, portas_processos[0])

    # Verifica a fila de mensagens após algum tempo
    time.sleep(5)
    for processo in processos:
        processo.verifica_fila_mensagens()
