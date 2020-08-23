from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn
from xmlrpc.client import ServerProxy

class RPC(ThreadingMixIn, SimpleXMLRPCServer):
    HOST = '192.168.43.64' 
    PORT = 2527
    ADDRESS = (HOST, PORT)
    servidor = None
    
    def __init__(self):
        self.servidor = SimpleXMLRPCServer(self.ADDRESS, allow_none=True)
        self.guardar_funciones()
        
    def iniciar_servidor(self):
        self.servidor.serve_forever()
    
    def guardar_funciones(self):
        self.servidor.register_function(self.imprimir, 'imprime')
        self.servidor.register_function(self.aceptar_conexion, 'acepta_conexion')
        self.servidor.register_function(self.cerrar_conexion, 'cierra_conexion')
        self.servidor.register_function(self.manejar_datos, 'maneja_datos')

    def imprimir(self, data):
        print(data)

    def aceptar_conexion(self, datos_habitacion):
        print('La habitación ' + str(datos_habitacion["id"]) + ' se ha conectado y empieza a enviar datos')
        
    def cerrar_conexion(self, datos_habitacion):
        print('El envío de datos de la habitacion ' + str(datos_habitacion["id"]) +  ' ha terminado')
        nombre_archivo = '' + datos_habitacion["nombre"] + '_' + datos_habitacion["apellido"] + '_' + str(datos_habitacion["id"]) + datos_habitacion["fechaIngreso"] 
        with open(nombre_archivo, 'rb') as archivo:
            return archivo.read()

    def manejar_datos(self,datos_medicos, datos_habitacion):
        nombre_archivo = '' + datos_habitacion["nombre"] + '_' + datos_habitacion["apellido"] + '_' + str(datos_habitacion["id"]) + datos_habitacion["fechaIngreso"] 
        dato_a_escribir = '' +  datos_medicos["fecha"] + ' Pulsaciones: ' + str(datos_medicos["pulsaciones"]) + ' ppm. Suero: ' + str(datos_medicos["suero"] * 100) + '%\n' 
        with open(nombre_archivo, 'a+') as archivo:
            archivo.write(dato_a_escribir)
        pulsaciones_alarmantes = (50 > datos_medicos["pulsaciones"] ) and (datos_medicos["pulsaciones"] < 100) 
        suero_alarmante = (datos_medicos["suero"] < 0.05)
        if suero_alarmante:
            print("suero: " + str(datos_medicos["suero"] * 100) + '%')
            print('Envíar a enfermera')
            #with ServerProxy('http://192.168.43.199:2525') as server_suero:
            #   server_suero.alerta_suero(datos_medicos, datos_habitacion)
            
        if pulsaciones_alarmantes:
            print("Pulsaciones alarmantes: " + str(datos_medicos["pulsaciones"]) + ' ppm')
            print('Envíar a doctor')
            #with ServerProxy('http://192.168.43.25:2525') as server_suero:
            #    server_suero.alerta_pulsaciones(datos_medicos, datos_habitacion)
            
        # Lógica de la conexión al otro server    

if __name__ == "__main__":
    serv = RPC()
    print("Iniciando servidor...")
    serv.iniciar_servidor()