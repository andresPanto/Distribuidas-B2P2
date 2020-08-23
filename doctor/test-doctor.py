from reconocimiento import ReconocimientoFacial
from subir_archivos import SubirArchivos
respuesta = ReconocimientoFacial().reconocer()
if respuesta != None:
    SubirArchivos(respuesta['imagen'], 'Imagenes').subir_archivo()
else:
    print('No se reconoció ningun rostro')