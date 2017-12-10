import sys
import argparse
import socket
import json


class Cliente():
    def __init__(self, ip, puerto, ip_central, puerto_central):
        self.ip = ip
        self.puerto = puerto
        self.ip_central = ip_central
        self.puerto_central = puerto_central


def main(args):
    parser = argparse.ArgumentParser(
        prog=args[0],
        description=("Cliente para descarga de videos por trozos." +
                     "Proyecto de Redes II, Septiembre-Diciembre 2017, USB.")
    )
    parser.add_argument(
        "--ip", "-i", action="store", help="Dirección IP donde se escuchará", default='0.0.0.0'
    )
    parser.add_argument(
        "--puerto", "-p", action="store", help="Puerto donde se escuchará", default=50004,
        type=int
    )
    parser.add_argument(
        "--ip-central", action='store', help='Dirección IP del servidor central',
        default="localhost"
    )
    parser.add_argument(
        "--puerto-central", action='store', help='Puerto donde escucha el servidor central',
        default=5000, type=int
    )
    pargs = parser.parse_args(args=args[1:])
    cliente = Cliente(pargs.ip, pargs.puerto)
    cliente.msg_send({"Hola": "Mundo!"})


if __name__ == '__main__':
    main(sys.argv)
