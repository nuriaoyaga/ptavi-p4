#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Clase (y programa principal) para un servidor de eco en UDP simple
"""

import socketserver
import sys
import json
import time
import calendar

class SIPRegisterHandler(socketserver.DatagramRequestHandler):
    """
    Echo server class
    """
    users_dic = {}
    def handle(self):
        caract_dic = {}
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            instrucciones_list = line.decode('utf-8').split(' ')
            if instrucciones_list[0] == 'REGISTER':
                usuario = instrucciones_list[1].split(':')[1]
                expires = int(instrucciones_list[2].split(':')[1])
                caract_dic["address"] = self.client_address[0]
                timeexp = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(time.time()+expires))
                caract_dic["expires"] = timeexp
                self.users_dic[usuario] = caract_dic
                if expires == 0:
                    del self.users_dic[usuario]
                self.wfile.write(b'SIP/2.0 200 OK\r\n\r\n')
                timenow = time.gmtime(time.time())
                for user in self.users_dic:
                    carac = self.users_dic[user]
                    
                    if timenow >= calendar.timegm(expires):
                        del self.users_dic[user]
                self.register2json()
            else:
                self.wfile.write(b"Hemos recibido tu peticion")
                print("El cliente nos manda " + line.decode('utf-8'))
            if not line:
                break


    def register2json(self):
        with open('registered.json', 'w') as fichero_json:
         json.dump(self.users_dic, fichero_json, sort_keys=True, indent=4, separators=(',', ':'))




if __name__ == "__main__":
    try:
        PORT = int(sys.argv[1])
    except ValueError:
        sys.exit("Invalid Port")
    # Creamos servidor de eco y escuchamos
    serv = socketserver.UDPServer(('', PORT), SIPRegisterHandler)
    print("Lanzando servidor UDP de eco...")
    serv.serve_forever()
