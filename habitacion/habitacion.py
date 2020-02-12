import xmlrpc.client
import time
from datetime import datetime
from random import *
from reportes import Reporte
from correo_electronico import Email
from subir_archivos import SubirArchivos

class Habitacion:
    datos_habitacion = None
    instancia_servidor = None
    nombre_archivo = None
    HOST = '192.168.43.64'
    PORT = '2527'
    LINK = None

    def __init__(self, id, nombre, apellido, correo):
        self.LINK = 'http://' + self.HOST + ':' + self.PORT
        self.instancia_servidor = xmlrpc.client.ServerProxy(
            self.LINK)
        self.datos_habitacion = {
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "correoElectronico": correo
            "fechaIngreso": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.iniciar_conexion()

    def iniciar_conexion(self):
        self.instancia_servidor.acepta_conexion(self.datos_habitacion)

    def enviar_datos(self):
        # self.iniciar_conexion()
        cont = 0
        datos_medicos = {
            "suero": random(),
            "pulsaciones": randint(1, 100),
            "fecha": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.instancia_servidor.maneja_datos(
            datos_medicos, self.datos_habitacion)
        time.sleep(1)
        cont = cont + 1
        #print("Datos enviados...")
        #print("Termina de enviar datos")

    def parar_conexion(self):
        #print("Termina de enviar datos")
        #informacion_binaria = self.instancia_servidor.cierra_conexion*(self.datos_habitacion)
        informacion = self.instancia_servidor.cierra_conexion(
            self.datos_habitacion)
        #print(informacion)
        #print(type(informacion))
        
        fecha_ingreso_para_nombre_archivo = self.datos_habitacion["fechaIngreso"].replace(':','_')
        self.nombre_archivo = 'Reporte_' + self.datos_habitacion["nombre"] + '_' + self.datos_habitacion["apellido"] + '_' + str(self.datos_habitacion["id"]) + fecha_ingreso_para_nombre_archivo + ".xlsx"
        respuesta_reporte = Reporte(self.nombre_archivo, self.datos_habitacion, informacion)
        mail = Email(self.datos_habitacion["correoElectronico"], self.nombre_archivo).enviar_email()
        subida_de_archivos = SubirArchivos(sel.nombre_archivo).subir_archivo()

        

