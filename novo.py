import random
import sys
import threading
import socket
import time

host = '127.0.0.1'
portas = [5001, 5002, 5003, 5004]
# portas = [5001, 5002, 5003]
global minha_porta, meu_indice, vetor_logico
minha_porta = 5001
meu_indice = 0
vetor_logico = [0, 0, 0, 0]

def handle_client(client, ):
    while True:
        global vetor_logico, meu_indice, portas
        dados = client.recv(1024).decode("utf-8")
        if not dados:
            break
        mensagem, relogio_recebido, porta = dados.split(';')
        print(porta)
        indice_recebido = portas.index(int(porta))
        relogio_recebido = [int(x) for x in relogio_recebido.split(',')]
        vetor_novo = vetor_logico.copy()
        vetor_novo[indice_recebido] += 1
        vetor_novo_max = [
            max(a, b)
            for a, b in zip(
                vetor_logico, 
                relogio_recebido    
            )
        ]
        
        print(f"Mensagem recebida: {mensagem}. Da porta: {porta}")
        print(f"Vetor antigo: {vetor_logico}")
        print(f"Vetor resultante: {vetor_novo_max}")
        vetor_logico = vetor_novo_max.copy()
        
    client.close()

def tcp_chat():
    global vetor_logico, meu_indice, minha_porta
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    tcp_socket.bind((host, minha_porta))
    tcp_socket.listen(5) 
    print(f"\nTCP Server listening on port {minha_porta}")

    while True:
        client, addr = tcp_socket.accept()
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

def send_message(m, port):
    global vetor_logico, meu_indice, minha_porta
    print(f"Enviando a mensagem: {m}, para o endereco: {port} [vetor lógico atual: {vetor_logico}]")
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))
    tcp_client.send(str(f"{m};{','.join(map(str, vetor_logico))};{minha_porta}").encode('utf-8'))
    tcp_client.close()

def handle_send_message():
    global vetor_logico, meu_indice, minha_porta
    while True:
        porta = random.choice(portas)
        if porta != minha_porta:   
            vetor_logico[meu_indice] += 1
            send_message('Tchau', porta)
        time.sleep(4)

if __name__ == '__main__':
    args = sys.argv[1:]
    minha_porta = int(args[0])
    meu_indice = portas.index(minha_porta)
    tcp_server_thread = threading.Thread(target=tcp_chat)
    tcp_server_thread.daemon = True
    tcp_server_thread.start()
    resp = input("Comecar a comunicar?")
    
    if(resp == 's'):
        handle_send_message()
    
