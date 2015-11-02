#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Programa cliente que abre un socket a un servidor
"""

import socket
import sys

# Cliente UDP simple.
if len(sys.argv) != 6:
    sys.exit("Usage: client.py ip puerto register sip_address expires_value")
# Dirección IP del servidor.
SERVER = sys.argv[1]
try:
    PORT = int(sys.argv[2])
except ValueError:
    sys.exit("Invalid Port")

# Contenido que vamos a enviar
METODO = sys.argv[3].upper()
USUARIO = sys.argv[4]
try:
    EXPIRES = sys.argv[5]
    if int(EXPIRES) < 0:
        sys.exit("Expires must be >0")
except ValueError:
    sys.exit("Expires must be an integer")

# Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    my_socket.connect((SERVER, PORT))
except socket.gaierror:
    sys.exit("Invalid IP")

print("Enviando: " + METODO + ' sip:' + USUARIO + ' SIP/2.0' + ' Expires:'
      + EXPIRES)
my_socket.send(bytes(METODO, 'utf-8') + b' sip:' + bytes(USUARIO, 'utf-8') +
               b' SIP/2.0\r\n' + b'Expires:' +
               bytes(EXPIRES, 'utf-8') + b'\r\n\r\n')
try:
    data = my_socket.recv(1024)
except ConnectionRefusedError:
    sys.exit("Conection refused")

print('Recibido -- ', data.decode('utf-8'))
print("Terminando socket...")

# Cerramos todo
my_socket.close()
print("Fin.")
