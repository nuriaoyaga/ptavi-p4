#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class EchoHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """

    def handle(self):
        # Escribe dirección y puerto del cliente (de tupla client_address)
        print(self.client_address)
        self.wfile.write(b"Hemos recibido tu peticion")
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            print("El cliente nos manda " + line.decode('utf-8'))

            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except ValueError:
        sys.exit("Invalid Port")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', port), EchoHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
