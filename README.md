# RelogiosVetoriais
Trabalho para a AB2 da disciplina de Sistemas Distribuídos.

# Passo-a-Passo de execução

## 1. Criando instâncias para os múltiplos processos
Execute o programa "tcp_server.py" em 4 intâncias de terminais diferentes, mas passando sempre uma das portas listadas dentro do programa.

Terminal 1:
```bash
python3 tcp_server.py 5001
```
Terminal 2:
```bash
python3 tcp_server.py 5002
```
Terminal 3:
```bash
python3 tcp_server.py 5003
```
Terminal 4:
```bash
python3 tcp_server.py 5004
```

## 2. Rodando as múltiplas instâncias
Cada instância sendo executada em cada terminal vai pedir uma confirmação de início do processo.

Basta digitar "s" e apertar Enter em cada um dos terminais para que todos comecem a enviar mensagens e, consequentemente, seus relógios vetoriais.
