import abc
import json
import socketserver
import threading
import signal
import sys


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class ServidorBase(metaclass=abc.ABCMeta):
    """ Clase base para todos los agentes en el sistema.

        Dispara un servidor para escuchar y un puerto, y un manejador para la linea de comandos
        en hilos separados. Espera por ctrl-c para finalizar el programa.
    """

    def __init__(self, ip, puerto):
        class _Handler(socketserver.StreamRequestHandler):
            def handle(this):
                msg = json.loads(this.rfile.readline().decode())
                self.msg_handler(msg, this.request, this.rfile, this.wfile)
        self.server = ThreadedTCPServer((ip, puerto), _Handler)

    @abc.abstractmethod
    def msg_handler(self, msg, socket, rfile, wfile):
        "Implementar este método para manejar los mensajes que recibe el servidor"
        pass

    @abc.abstractmethod
    def command_handler(self, command, arg):
        "Implementar este método para manejar los comandos"
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
            self.server.server_close()
            print()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)
        server_t = threading.Thread(target=self.server.serve_forever, daemon=True)
        cli_t = threading.Thread(target=self.command_line_interface, daemon=True)
        server_t.start()
        cli_t.start()
        print(msg)
        signal.pause()
