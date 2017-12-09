import sys
import argparse


def main(args):
    parser = argparse.ArgumentParser(
        prog=args[0],
        description=("Servidor central para descarga de videos por trozos." +
                     "Proyecto de Redes II, Septiembre-Diciembre 2017, USB.")
    )
    parser.add_argument(
        "--ip", "-i", action="store", help="Dirección IP donde se escuchará", default="0.0.0.0"
    )
    parser.add_argument(
        "--puerto", "-p", action="store", help="Puerto donde se escuchará", default=50000,
        type=int
    )
    parser.parse_args(args=args[1:])


if __name__ == '__main__':
    main(sys.argv)
