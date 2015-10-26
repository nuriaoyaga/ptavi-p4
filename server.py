#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    ips_dic = {}
    def handle(self):
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            instrucciones_list = line.decode('utf-8').split(' ')
            if instrucciones_list[0] == 'REGISTER':
                usuario = instrucciones_list[1].split(':')[1]
                expires = int(instrucciones_list[2].split(':')[1])
                self.ips_dic[usuario] = self.client_address[0]
                if expires == 0:
                    del self.ips_dic[usuario]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                print(self.ips_dic)
            else:
                self.wfile.write(b"Hemos recibido tu peticion")
                print("El cliente nos manda " + line.decode('utf-8'))
            if not line:
                break



if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        sys.exit("Invalid Port")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
