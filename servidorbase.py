import abc
import json
import socketserver
import threading
import signal
import sys
import re
import argparse

IP_PATTERN = r'(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])'  # noqa: E501


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


def direccion_ip(string):
    if string.lower() != 'localhost' and re.fullmatch(IP_PATTERN, string) is None:
        msg = "%s no es una direccion IP valida" % string
        raise argparse.ArgumentTypeError(msg)
    return string


class ServidorBase(metaclass=abc.ABCMeta):
    """ Clase base para todos los agentes en el sistema.

        Dispara un servidor para escuchar y un puerto, y un manejador para la linea de comandos
        en hilos separados. Espera por ctrl-c para finalizar el programa.

        Los metodos marcados con abstractmethod deben ser implementados por la clase derivada.
        Tambien debe definir un valor por defecto para los datos DEFAULT_DATA.
    """

    def __init__(self, ip, puerto, data_file):
        "Constructor de la clase, crea el objeto servidor y lee los datos guardados"
        class _Handler(socketserver.StreamRequestHandler):
            def handle(this):
                try:
                    msg = json.loads(this.rfile.readline().decode())
                except:
                    msg = {}
                self.msg_handler(msg, this)
        self.server = ThreadedTCPServer((ip, puerto), _Handler)
        self.data_file = data_file
        try:
            with open(data_file, mode='r') as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = self.DEFAULT_DATA

    def msg_send(self, msg, socket):
        socket.sendall((json.dumps(msg) + '\n').encode())

    @abc.abstractmethod
    def msg_handler(self, msg, handler):
        "Implementar este método para manejar los mensajes que recibe el servidor"
        pass

    @abc.abstractmethod
    def command_handler(self, command, arg):
        "Implementar este método para manejar los comandos"
        pass

    @abc.abstractmethod
    def setup(self):
        """ Metodo que se ejecuta luego de iniciar el servidor, pero antes de iniciar la interfaz
            de comando, para cualquier inicializacion automatica que requiera recibir mensajes
        """
        pass

    def command_line_interface(self):
        "Método que lee instrucciones desde la línea de comandos"
        while True:
            text = input("> ")
            splitted = text.split(' ')
            if len(splitted) == 1:
                self.command_handler(splitted[0], None)
            elif len(splitted) > 1:
                self.command_handler(splitted[0], splitted[1])

    def run(self, msg=None):
        """ Al ejecutar este método, se inician el servidor y la lectura de comandos.
            El hilo principal se detiene, esperando por ctrl-c
        """
        def signal_handler(signal, frame):
            self.server.shutdown()
            self.server.server_close()
            with open(self.data_file, mode='w') as f:
                json.dump(self.data, f)
            print()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        server_t = threading.Thread(target=self.server.serve_forever, daemon=True)
        cli_t = threading.Thread(target=self.command_line_interface, daemon=True)
        server_t.start()
        self.setup()
        print(msg)
        cli_t.start()
        signal.pause()
