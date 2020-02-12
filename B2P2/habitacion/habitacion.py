import xmlrpc.client
import time
from datetime import datetime
from random import *
from reportes import Reporte
from correo_electronico import Email
from subir_archivos import SubirArchivos
from tkinter import messagebox

class Paciente:
    datos_habitacion = None
    instancia_servidor = None
    nombre_archivo = None
    HOST = '172.29.64.148'
    PORT = '2525'
    LINK = 'http://192.168.13.13:2525'
    enviando_datos = False

    def __init__(self, id, nombre, apellido, correo):
        #self.LINK = 'http://' + self.HOST + ':' + self.PORT
        print('Constructor')
        self.instancia_servidor = xmlrpc.client.ServerProxy(
            'http://192.168.43.13:2526')
        self.datos_habitacion = {
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "correoElectronico": correo,
            "fechaIngreso": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.iniciar_conexion()
        

    def iniciar_conexion(self):
        print('Inicia conexion')
        self.instancia_servidor.acepta_conexion(self.datos_habitacion)

    def enviar_datos(self):
        # self.iniciar_conexion()
        self.enviando_datos = True
        while self.enviando_datos:
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

    def parar_conexion(self):
        self.enviando_datos = False
        informacion = self.instancia_servidor.cierra_conexion(
            self.datos_habitacion)
        
        fecha_ingreso_para_nombre_archivo = self.datos_habitacion["fechaIngreso"].replace(':','_')
        self.nombre_archivo = 'Reporte_' + self.datos_habitacion["nombre"] + '_' + self.datos_habitacion["apellido"] + '_' + str(self.datos_habitacion["id"]) + '_' + fecha_ingreso_para_nombre_archivo + ".xlsx"
        
        
        respuesta_reporte = Reporte(self.nombre_archivo, self.datos_habitacion, informacion).generar_reporte()
        mail = Email(self.datos_habitacion["correoElectronico"], self.nombre_archivo).enviar_email()
        if mail == 0:
            messagebox.showerror("Correo Electrónico", "Error al envíar el correo electrónico")
        subida_de_archivos = SubirArchivos(self.nombre_archivo, 'Reportes').subir_archivo()
        if subida_de_archivos == 0:
            messagebox.showerror("Google Drive", "Error al subir archivo a Google Drive")
        

        

if __name__=="__main__":
    print('antes paciente')
    Paciente(1, "nombre", "apellido", "andres.pantoja@epn.edu.ec").enviar_datos()