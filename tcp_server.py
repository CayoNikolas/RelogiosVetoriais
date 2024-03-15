import random
import sys
import threading
import socket
import time

host = '127.0.0.1'
port = 55555
portas = [5001, 5002, 5003, 5004]
minha_porta = 5001
meu_indice = 0
fila_mensagens = []
vetor_logico = [0, 0, 0, 0]

clients = []
names = []

def handle_client(client, ):
    while True:
        dados = client.recv(1024).decode("utf-8")
        if not dados:
            break
        global vetor_logico, meu_indice, fila_mensagens
        mensagem, relogio_recebido, indice_recebido = dados.split(';')
        indice_recebido = int(indice_recebido)
        relogio_recebido = [int(x) for x in relogio_recebido.split(',')]
        vetor_novo = vetor_logico.copy()
        vetor_novo[indice_recebido] += 1
        print("Vetor novo:", vetor_novo)
        print("Relogio recebido: ", relogio_recebido)
        if vetor_novo == relogio_recebido:
            print(f"Mensagem recebida: {mensagem}")
            print(f"Vetor antigo: {vetor_logico}")
            print(f"Vetor resultante: {vetor_novo}")
            vetor_logico = vetor_novo.copy()
            verificar_fila()
        else:
            print(f"Mensagem recebida: {mensagem}")
            print(f"Vetores lógicos diferem. A mensagem será guardada em uma fila")
            fila_mensagens.append((mensagem, relogio_recebido, indice_recebido))
    client.close()

def verificar_fila():
  global fila_mensagens, vetor_logico, meu_indice
  if (fila_mensagens):
    for i, m in enumerate(fila_mensagens):
      mensagem, relogio_recebido, indice_recebido = m
      vetor_novo = vetor_logico.copy()
      vetor_novo[indice_recebido] += 1
      if vetor_novo == relogio_recebido:
        print("Mensagem retirada da fila de espera:")
        print(f"Mensagem recebida: {mensagem}")
        print(f"Vetor antigo: {vetor_logico}")
        print(f"Vetor resultante: {vetor_novo}")
        vetor_logico = vetor_novo.copy()
        fila_mensagens.pop(i)

def tcp_chat():
    global vetor_logico, meu_indice
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcp_socket.bind((host, port))
    tcp_socket.listen(5) 
    print(f"TCP Server listening on port {port}")

    while True:
        print("tcp_chat")
        client, addr = tcp_socket.accept()
        print(f"TCP Connection from {addr}")
        print(vetor_logico)
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def send_message(m, port):
    global vetor_logico, meu_indice
    print(f"Enviando a mensagem: {m}, para o endereco: {port} [vetor lógico atual: {vetor_logico}]")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))
    tcp_client.send(str(f"{m};{','.join(map(str, vetor_logico))};{meu_indice}").encode('utf-8'))
    tcp_client.close()

def handle_send_message():
    global vetor_logico, meu_indice
    while True:
        vetor_logico[meu_indice] += 1
        for porta in portas:
            if porta == port:
                continue
            send_message('Tchau', porta)
        time.sleep(4)

if __name__ == '__main__':
    tcp_server_thread = threading.Thread(target=tcp_chat)
    tcp_server_thread.daemon = True
    tcp_server_thread.start()
    args = sys.argv[1:]
    port = int(args[0])
    meu_indice = portas.index(port)
    resp = input("Comecar a comunicar?")
    
    if(resp == 's'):
        handle_send_message()
    
