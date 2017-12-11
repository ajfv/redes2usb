import sys
import argparse
import servidorbase
import os
import threading
import socket


class ServidorSecundario(servidorbase.ServidorBase):
    "Clase para los servidor secundarios"

    def __init__(self, ip, puerto, ip_central, puerto_central, data_file):
        "Inicializacion del servidor secundario"
        for i in ['1', '2', '3']:
            if i in data_file:
                self.video_folder = "./videos" + i
                break
        self.DEFAULT_DATA = {v: 0 for v in os.listdir(self.video_folder)}
        super().__init__(ip, puerto, data_file)
        self.ip_c = ip_central
        self.puerto_c = puerto_central
        self.lock = threading.Lock()
        self.MENSAJES = {  # mensajes y sus respectivos manejadores
            'sincronizacion': self.sincronizacion,
            'descarga': self.descarga
        }

    def setup(self):
        "Se envia el mensaje de inscripcion al servidor. Si el envio falla, se acaba el programa"
        try:
            socket_dest = socket.socket()
            ip, puerto = self.server.server_address
            socket_dest.connect((self.ip_c, self.puerto_c))
            inscripcion = {
                "accion": "inscripcion", "ip": ip, "puerto": puerto,
                "videos": list(self.data.keys())
                }
            self.msg_send(inscripcion, socket_dest)
            socket_dest.close()
        except:
            print("No se hallo el servidor central")
            sys.exit(1)

    def msg_handler(self, msg, handler):
        "Manejador general, que escoge el especifico dependiendo del tipo de mensaje"
        try:
            operacion = self.MENSAJES[msg['accion']]
        except:
            print('Se recibio mensaje mal formado desde ' + str(handler.client_address), end='\n> ')
        else:
            operacion(msg, handler)

    def sincronizacion(self, msg, handler):
        pass

    def descarga(self, msg, handler):
        pass

    def command_handler(self, command, arg):
        if command.upper() == "VIDEOS_DESCARGANDO":
            print("por implementar")
        elif command.upper() == "VIDEOS_DESCARGADOS":
            with self.lock:
                print('video|descargas')
                for nombre, veces in self.data.items():
                    print("%s|%d" % (nombre, veces))
        else:
            print("Comando no reconocido")


def main(args):
    parser = argparse.ArgumentParser(
        prog=args[0],
        description=("Servidor secundario para descarga de videos por trozos." +
                     "Proyecto de Redes II, Septiembre-Diciembre 2017, USB.")
    )
    parser.add_argument(
        "--ip", "-i", action="store", help="Dirección IP donde se escuchará", default='0.0.0.0'
    )
    parser.add_argument(
        "--puerto", "-p", action="store", help="Puerto donde se escuchará", default=50000,
        type=int
    )
    parser.add_argument(
        "--ip-central", action='store', help='Dirección IP del servidor central',
        default="localhost"
    )
    parser.add_argument(
        "--puerto-central", action='store', help='Puerto donde escucha el servidor central',
        default=50000, type=int
    )
    parser.add_argument(
        "--numero", "-n", action='store', help='Numero del servidor (1-3)', required=True,
        type=int
    )
    pargs = parser.parse_args(args=args[1:])
    if pargs.numero not in (1, 2, 3):
        print("El numero del servidor es invalido.")
        sys.exit()
    pargs.puerto += pargs.numero
    servidor = ServidorSecundario(
        pargs.ip, pargs.puerto, pargs.ip_central, pargs.puerto_central,
        'secundario%d.json' % pargs.numero
    )
    servidor.run("Servidor escuchando en %s:%d" % (pargs.ip, pargs.puerto))


if __name__ == '__main__':
    main(sys.argv)
