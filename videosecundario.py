import sys
import argparse


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
        "--ip-maestro", action='store', help='Dirección IP del servidor central',
        default="localhost"
    )
    parser.add_argument(
        "--puerto-maestro", action='store', help='Puerto donde escucha el servidor central',
        default=5000, type=int
    )
    parser.add_argument(
        "--numero", "-n", action='store', help='Numero del servidor (1-3)', required=True,
        type=int
    )
    pargs = parser.parse_args(args=args[1:])
    if pargs.numero not in (1, 2, 3):
        print("El numero del servidor es invalido.")
        sys.exit()


if __name__ == '__main__':
    main(sys.argv)
