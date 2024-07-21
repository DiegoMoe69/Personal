import socket
import threading
import json
import sys

from codificacion import codificar, decodificacion

class Servidor:

    def __init__(self, port, host):
        self.host = host
        self.port = port
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockets = {}
        self.server_sock.bind((self.host, self.port))
        self.server_sock.listen()
        self.accept_connections()

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()
    
    def accept_connections_thread(self):
        while True:
            client_socket, address = self.server_sock.accept()
            self.sockets[client_socket] = address
            listening_client_thread = threading.Thread(
                target = self.listen_client_thread,
                args = (client_socket, ),
                daemon = True)
            listening_client_thread.start()

    def listen_client_thread(self, client_socket: socket.socket):
        conectado = True
        while conectado:
            try:
                mensaje = client_socket.recv(5000)
                if not mensaje:
                    break
                dificultad, puzzle = decodificacion(mensaje).split(';')
                with open('assets/solucion_puzzles/' + dificultad) as archivo:
                    archivo = archivo.readlines()
                    archivo = ''.join(archivo)
                if archivo == puzzle:
                    client_socket.sendall(codificar('valido'))
                else:
                    client_socket.sendall(codificar('invalido'))
            except (ConnectionResetError, ConnectionAbortedError):
                print('Se desconecto un cliente')
                conectado = False
        client_socket.close()
        del self.sockets[client_socket]

if __name__ == '__main__':
    port = int(sys.argv[1])
    with open('config.json') as configuracion:
        config = json.load(configuracion)
    host = config['host']
    server = Servidor(port, host)