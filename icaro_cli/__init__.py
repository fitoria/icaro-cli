#!/usr/bin/python

import os
import sys
import time
import platform

from pystache.common import TemplateNotFoundError
from pystache.renderer import Renderer


try:
    from icaro.hardware.icaro.modulos import docker
except ImportError:
    #YOLO
    sys.path.append('/Users/fitoria/code/tallericaro/')
    from icaro.hardware.icaro.modulos import docker


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = '/dev/ttyACM0'
PORT_USB = '/dev/ttyUSB0'

PIC16_DIR = 'micro/firmware/non-free/include/pic16/'
LIBS_DIR = [
        'micro/firmware/source/',
        'micro/firmware/tmp',
        PIC16_DIR,
        'micro/firmware/icaro_lib/',
        'micro/firmware/include/pic16/',
]
LIBS_DIR = [os.path.join(BASE_DIR, d) for d in LIBS_DIR]

TEMPORAL_DIR = '/tmp/icarotemporal'
ARCHIVO_LKR = os.path.join(BASE_DIR, 'micro/firmware/pic16/lkr/18f2550.lkr')
LIBPUF = os.path.join(BASE_DIR, 'micro/firmware/pic16/lib/libpuf.lib')

os_name = platform.system()
if os_name == 'Darwin':
    LIBC18F = os.path.join(BASE_DIR, '/usr/local/Cellar/sdcc/3.5.0/share/sdcc/lib/pic16/libc18f.lib')
    LIBM18F = os.path.join(BASE_DIR, '/usr/local/Cellar/sdcc/3.5.0/share/sdcc/lib/pic16/libm18f.lib')
else:
    LIBC18F = os.path.join(BASE_DIR, '/usr/share/sdcc/lib/pic16/libc18f.lib')
    LIBM18F = os.path.join(BASE_DIR, '/usr/share/sdcc/lib/pic16/libm18f.lib')

USB_DESCRIPTORS = os.path.join(BASE_DIR, 'micro/firmware/pic16/obj/usb_descriptors.o')
CRT0IPINGUINO = os.path.join(BASE_DIR, 'micro/firmware/pic16/obj/crt0ipinguino.o')
APPLICATION_IFACE = os.path.join(BASE_DIR, 'micro/firmware/pic16/obj/application_iface.o')
APPLICATION_IFACE = os.path.join(BASE_DIR, 'micro/firmware/pic16/obj/application_iface.o')
OUTPUT_FILE = os.path.join(TEMPORAL_DIR, 'main.o')
HEX_FILE = os.path.join(TEMPORAL_DIR, 'main.hex')

PARAMETROS_COMPILADOR = [
    '--verbose',
    '-mpic16',
    '--denable-peeps',
    '--use-non-free',
    '--obanksel=9',
    '--opt-code-size',
    '--optimize-cmp',
    '--optimize-df',
    '-p18f4550',
]

PARAMETROS_BINARIO = [
    '-o %s' % HEX_FILE,
    '--denable-peeps',
    '--use-non-free',
    '--obanksel=9',
    '--optimize-df',
    '--no-crt',
    '-Wl-s%s,-m' % ARCHIVO_LKR,
    '-mpic16',
    '-p18f4550',
    '-l %s' % LIBPUF,
    '-l %s' % LIBC18F,
    '--lib-path %s' % PIC16_DIR,
    '-l %s' % LIBM18F,
    USB_DESCRIPTORS,
    CRT0IPINGUINO,
    APPLICATION_IFACE,
    OUTPUT_FILE
]


SOURCE_FILE = os.path.join(BASE_DIR, 'micro/firmware/source/main.c')
SOURCE_TEMPLATE = os.path.join(BASE_DIR, 'micro/firmware/source/main.c')

def crear_plantilla(archivo_fuente='user.c'):
    print "creando plantilla para archivo %s" % archivo_fuente
    renderer = Renderer()
    template = renderer.load_template(SOURCE_TEMPLATE)
    dato_plantilla = renderer.render(template, {'include_path': archivo_fuente})
    archivo = open(SOURCE_FILE, 'w')
    archivo.write(dato_plantilla)
    archivo.close()
    print "plantilla creada"

def compilar_archivo(archivo_fuente=SOURCE_FILE, archivo_salida=OUTPUT_FILE):
    '''
    Compila archivo fuente determinado, por defecto compila el main.c dentro de source
    '''

    try:
        os.stat(TEMPORAL_DIR)
    except:
        os.mkdir(TEMPORAL_DIR)

    compiler = 'sdcc' if os_name == 'Darwin' else 'sdcc-sdcc'
    #primer: compilador
    #segundo: parametros
    #tercero: include_dirs
    #cuarto: output
    #quinto: source
    comando = "%s %s %s -c -c -o %s %s" % (compiler,
                                               ' '.join(PARAMETROS_COMPILADOR),
                                               ' -I '.join(LIBS_DIR),
                                               archivo_salida,
                                               archivo_fuente
                                               )
    return comando

def enlazar_archivo():
    '''Enlaza el archivo y produce el binario'''
    compiler = 'sdcc' if os_name == 'Darwin' else 'sdcc-sdcc'
    comando = "%s %s" % (compiler, ' '.join(PARAMETROS_BINARIO))
    return comando

def cargar(nombre_archivo=HEX_FILE):
    '''Sube el archivo a la placa usando el modulo docker de icaro'''
    vivo = True
    a = 1
    docker.buscar_bus_docker = True
    while vivo:
        i = docker.docker(HEX_FILE)
        time.sleep(1)
        a = a + 1
        if a >= 10:
            vivo = False
            print 'No se pudo cargar el programa'

        if i == 0:
            print 'El programa fue cargado exitosamente'
            vivo = False
    docker.buscar_bus_docker = False

def main():
    if len(sys.argv)==2:
        crear_plantilla(os.path.abspath(sys.argv[1]))
    else:
        crear_plantilla()
    print "COMPILANDO"
    salida = compilar_archivo()
    os.system(salida)
    print "ENLAZANDO"
    salida = enlazar_archivo()
    os.system(salida)
    print "CARGANDO"
    cargar()

if __name__ == "__main__":
    main()
