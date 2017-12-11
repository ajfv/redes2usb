import sys
import argparse
import signal
import socket
import json
import threading
from servidorbase import ServidorBase


class Cliente():
    def __init__(self, ip, puerto, ip_central, puerto_central):
        self.ip = ip
        self.puerto = puerto
        self.ip_central = ip_central
        self.puerto_central = puerto_central
        self._nombre = None
        self.nombre_lock = threading.Lock()

    @property
    def nombre(self):
        with self.nombre_lock:
            return self._nombre

    @nombre.setter
    def nombre(self, val):
        with self.nombre_lock:
            self._nombre = val

    def run(self):
        def signal_handler(signal, frame):
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        while True:
            try:
                text = input("> ")
            except EOFError:
                return
            splitted = text.split(' ')
            if len(splitted) == 1:
                self.command_handler(splitted[0], None)
            elif len(splitted) > 1:
                self.command_handler(splitted[0], splitted[1])

    def command_handler(self, command, arg):
        if command.upper() == "INSCRIBIR":
            if arg is None:
                print("Falta parametro: INSCRIBIR <nombre>")
            else:
                self.nombre = arg
        elif command.upper() == "LISTA_VIDEOS":
            self.listar_videos()
        else:
            print("Comando no reconocido: {}".format(command))

    def listar_videos(self):
        try:
            socket_central = socket.socket()
            socket_central.connect((self.ip_central, self.puerto_central))
            ServidorBase.msg_send({"accion": "listado"}, socket_central)
            lista_videos = bytearray()
            data = socket_central.recv(1024)
            while len(data) > 0:
                lista_videos.extend(data)
                data = socket_central.recv(1024)
            socket_central.close()
            print("Los videos disponibles para descargar son: \n {}".format(lista_videos.decode("utf-8")))
        except:
            print("No se pudo establecer conexión con el servidor central")

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
    cliente = Cliente(pargs.ip, pargs.puerto, pargs.ip_central, pargs.puerto_central)
    cliente.run()


if __name__ == '__main__':
    main(sys.argv)
