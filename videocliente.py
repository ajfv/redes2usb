import sys
import argparse
import socket
import json


class Cliente():
    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto

    def msg_send(self, msg):
        server = socket.socket()
        server.connect((self.ip, self.puerto))
        server.sendall((json.dumps(msg) + '\n').encode())
        server.close()


def main(args):
    parser = argparse.ArgumentParser(
        prog=args[0],
        description=("Cliente para descarga de videos por trozos." +
                     "Proyecto de Redes II, Septiembre-Diciembre 2017, USB.")
    )
    parser.add_argument(
        "--ip", "-i", action="store", help="Dirección IP donde se escuchará", default='localhost'
    )
    parser.add_argument(
        "--puerto", "-p", action="store", help="Puerto donde se escuchará", default=50000,
        type=int
    )
    parser.add_argument(
        "--ip-maestro", action='store', help='Dirección IP del servidor central', required=True
    )
    parser.add_argument(
        "--puerto-maestro", action='store', help='Puerto donde escucha el servidor central',
        required=True, type=int
    )
    pargs = parser.parse_args(args=args[1:])
    cliente = Cliente(pargs.ip, pargs.puerto)
    cliente.msg_send({"Hola": "Mundo!"})


if __name__ == '__main__':
    main(sys.argv)
