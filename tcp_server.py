import sys
import threading
import socket
import time

#Estabelecendo o Servidor no Localhost
host = '127.0.0.1'
port = 55555
'''server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
#Servidor agora esta ouvindo
server.listen()'''

#Lista para os clientes e seus nomes
#Relacionar com os Processos
clients = []
names = []

'''#Função para exibir para todos os clientes uma mensagem enviada
def broadcast(message):
    for client in clients:
        client.send(message)'''

#Tratamento das mensagens enviadas pelos clientes
def handle_client(client):
    # recebe dados do cliente e os imprime no console
    while True:
        data = client.recv(1024)
        if not data:
            break
        print(f"TCP Received: {data.decode('utf-8')}")
    
    # se não houver mais dados o loop é encerrado e o socket do cliente é fechado
    client.close()

'''def receive():
    while True:
        print('Servidor rodando e ouvindo...')
        #Estabelecendo conexão com o cliente
        client, address = server.accept()
        print(f'Conexão estabelecida com {str(address)}')
        #Recebendo o nome do processo pra guardar
        client.send('Qual processo?'.encode('utf-8'))
        name = client.recv(1024)
        #Regularizando conexão
        names.append(name)
        clients.append(client)
        print(f'Processo: {name}'.encode('utf-8'))
        broadcast(f'{name} esta conectado'.encode('utf-8'))
        client.send('Processo conectado com sucesso'.encode('utf-8'))
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()'''

def tcp_chat():
    tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria um socket TCP
    tcp_socket.bind((host, port)) # faz o bind para o endereço e porta desejados
    tcp_socket.listen(5) # começa a ouvir por conexões
    print(f"TCP Server listening on port {port}")

    # quando um cliente se conecta, inicia uma nova thread (client_handler) para lidar com esse cliente
    while True:
        client, addr = tcp_socket.accept()
        print(f"TCP Connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client,))
        client_handler.start()

'''def tcp_comm():
    while True:
        time.sleep(4)
        message = ('Exemplo'.encode('utf-8'))
        broadcast(message)'''

def send_message(message):
    tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_client.connect((host, port))
    tcp_client.send(message.encode('utf-8'))
    tcp_client.close()

def handle_send_message():
    while True:
        send_message('Tchau')
        time.sleep(4)

if __name__ == '__main__':
    tcp_server_thread = threading.Thread(target=tcp_chat)
    tcp_server_thread.start()
    args = sys.argv[1:]
    port = int(args[0])
    handle_send_message()