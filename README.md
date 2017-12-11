# redes2usb

Proyecto para Redes de Computadoras II, Universidad Simón Bolívar, trimestre septiembre-diciembre 2017.
Implementación de un sistema de descarga de archivos por partes.

## Autores:

* Alfredo Fanghella
* Fernando Pérez

## Arquitectura

El proyecto es un sistema distribuido con 3 clases de agentes clientes, servidor central y servidores secundarios. Cada
agente esta implementado con un script distinto. El sistema sirve para que los clientes descarguen archivos desde 3
servidores secundarios, aunque el cliente solo necesita conocer el IP y el puerto donde se ejecuta el servidor central. En
caso de caída de servidores secundarios, el resto de ellos asume su trabajo sin causar errores fátales. Originalmente el
proyecto estaba pensado para descargar videos, pero en realidad soporta cualquier tipo de archivo.

## Ejecución

Primero debe iniciar el servidor central (videocentral.py), luego tres secundarios (videosecundario.py) y finalmente cuantos
clientes se quiera usar (videocliente.py). Todos los entes son interactivos, para ver que comandos soportan ejecute el
comando `h` o `help`. Se pueden detener usando Ctrl-D, Ctrl-C o enviandoles SIGTERM, y antes de finalizar guardan los datos
con las estadísticas de descarga en archivos en formato JSON.

### videocliente.py

Script que ejecuta al cliente, con la siguiente interfaz de línea de comandos (Nota: esta ayuda esta parcialmente
autogenerada y por ello tiene partes en inglés):

```
usage: videocliente.py [-h] [--ip-central IP_CENTRAL]
                       [--puerto-central PUERTO_CENTRAL]

Cliente para descarga de videos por trozos.Proyecto de Redes II, Septiembre-
Diciembre 2017, USB.

optional arguments:
  -h, --help            show this help message and exit
  --ip-central IP_CENTRAL
                        Dirección IP del servidor central
  --puerto-central PUERTO_CENTRAL
                        Puerto donde escucha el servidor central
```
Maneja comandos para cambiar el nombre del cliente, ver los archivos disponibles y descargar un archivo.

### videocentral.py

Script para el servidor central, que debe ser el primero en ejecutarse y del cual solo se necesita una instancia.

```
usage: videocentral.py [-h] [--ip IP] [--puerto PUERTO]

Servidor central para descarga de videos por trozos.Proyecto de Redes II,
Septiembre-Diciembre 2017, USB.

optional arguments:
  -h, --help            show this help message and exit
  --ip IP, -i IP        Dirección IP donde se escuchará
  --puerto PUERTO, -p PUERTO
                        Puerto donde se escuchará
```

### videosecundario.py

Script para los servidores secundarios. Se necesitan 3 para que el sistema inicie su funcionamiento, aunque luego se adapta
si se caen uno o dos. 

```
usage: videosecundario.py [-h] [--ip IP] [--puerto PUERTO]
                          [--ip-central IP_CENTRAL]
                          [--puerto-central PUERTO_CENTRAL] --numero NUMERO

Servidor secundario para descarga de videos por trozos.Proyecto de Redes II,
Septiembre-Diciembre 2017, USB.

optional arguments:
  -h, --help            show this help message and exit
  --ip IP, -i IP        Dirección IP donde se escuchará
  --puerto PUERTO, -p PUERTO
                        Puerto donde se escuchará
  --ip-central IP_CENTRAL
                        Dirección IP del servidor central
  --puerto-central PUERTO_CENTRAL
                        Puerto donde escucha el servidor central
  --numero NUMERO, -n NUMERO
                        Numero del servidor (1-3)
```

## Instalación

Solo se utiliza la librería estandar de Python 3, así que no se requiere ninguna instalación más alla de la del intérprete
del lenguaje. En particular, debería funcionar con Python 3.4 o mayor. Los distintos scripts dependen únicamente de la
presencia en el mismo directorio del módulo servidorbase.py.

## Problemas conocidos

* Cuando el servidor central se cae y se vuelve a levantar, se deben reiniciar los servidores secundarios.
* Cuando todos los servidores secundarios se caen, un intento de descarga ocasiona que se disparen excepciones sin atrapar
en el servidor central, aunque esto no ocasiona que se caiga.
