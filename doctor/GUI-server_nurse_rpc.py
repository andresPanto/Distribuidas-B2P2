from xmlrpc.server import SimpleXMLRPCServer
import threading
from tkinter import *


textSuero = None
textPulsaciones = None


class SalaDoctores():
    HOST = '192.168.43.199'
    PORT = 2525
    ADDRESS = (HOST, PORT)
    BUFFSIZE = 1024

    def __init__(self):
        self.servidor = SimpleXMLRPCServer(self.ADDRESS, allow_none=True)
        self.guardar_funciones()

    def iniciar_servidor(self):
        print("Servidor Iniciado...")
        self.servidor.serve_forever()

    def guardar_funciones(self):
        self.servidor.register_function(self.alertar_suero, 'alerta_suero')
        self.servidor.register_function(
            self.alertar_pulsaciones, 'alerta_pulsaciones')

    def alertar_suero(self, datos_medicos, datos_habitacion):
        global textSuero
        habitacion = "En la habitacion: " + str(datos_habitacion['id']) + "\n"
        paciente = "El cliente: " + datos_habitacion['nombre'] + " " + datos_habitacion['apellido'] + "\n"
        suero = "El nivel del suero esta al: " + str(datos_medicos['suero']) + "\n\n"
        textSuero.config(state=NORMAL)
        textSuero.insert(INSERT, habitacion)
        textSuero.insert(INSERT, paciente)
        textSuero.insert(INSERT, suero)
        textSuero.config(state=DISABLED)
        
        print('\nEn la habitacion:', datos_habitacion['id'])
        print('El cliente:',datos_habitacion['nombre'], datos_habitacion['apellido'])
        print('El nivel del suero esta al:', datos_medicos['suero'])

    def alertar_pulsaciones(self, datos_medicos, datos_habitacion):
        global textPulsaciones
        habitacion = "En la habitacion: " + str(datos_habitacion['id']) + "\n"
        paciente = "El cliente: " + datos_habitacion['nombre'] + " " + datos_habitacion['apellido'] + "\n"
        pulsaciones = "Presenta pulsaciones de: " + str(datos_medicos['pulsaciones']) + "\n\n"
        textPulsaciones.config(state=NORMAL)
        textPulsaciones.insert(INSERT, habitacion)
        textPulsaciones.insert(INSERT, paciente)
        textPulsaciones.insert(INSERT, pulsaciones)
        textPulsaciones.config(state=DISABLED)
        
        print('\nEn la habitacion:', datos_habitacion['id'])
        print('El cliente:',datos_habitacion['nombre'], datos_habitacion['apellido'])
        print('Presenta pulsaciones de:', datos_medicos['pulsaciones'])

    def cerrar_servidor(self):
        self.servidor.shutdown()


class Interfaz:
    def __init__(self):
        self.ejecutar()

    def ejecutar(self):
        raiz = Tk()
        
        #print("Iniciando servidor...")
        # serv.iniciar_servidor()
        
        #raiz.iconbitmap("/home/juan/Universidad/Proyecto Distribuidas/quiqsolution.ico")
        raiz.title("Enfermería y Guardia")
        # raiz.resizable(0,1)
        raiz.geometry("650x350")

        frameInterno = Frame(raiz, width=500, height=500)
        frameInterno.pack(fill="both", expand="true")
        frameInterno.rowconfigure(0, weight=1)
        frameInterno.rowconfigure(1, weight=1)
        frameInterno.rowconfigure(2, weight=2)
        frameInterno.columnconfigure(0, weight=1)
        frameInterno.columnconfigure(1, weight=1)
        frameInterno.columnconfigure(2, weight=1)
        frameInterno.columnconfigure(3, weight=1)

        Label(frameInterno, text="ALERTAS", padx=10, pady=10,
              relief="groove", bd=10).grid(row=0, columnspan=4, sticky=(N, S, W, E))
        Label(frameInterno, text="ALERTA PULSACIONES").grid(
            row=1, column=2, sticky=(N, S, W, E))
        Label(frameInterno, text="ALERTA SUERO").grid(
            row=1, column=0, sticky=(N, S, W, E))

        global textSuero
        global textPulsaciones

        textSuero = Text(frameInterno, width=30, height=10,
                         state=DISABLED)
        textSuero.grid(row=2, column=0, sticky=(N, S, W, E))

        textPulsaciones = Text(frameInterno, width=30,
                               height=10, state=DISABLED)
        textPulsaciones.grid(row=2, column=2, sticky=(N, S, W, E))

        scrollSuero = Scrollbar(frameInterno, command=textSuero.yview)
        scrollSuero.grid(row=2, column=1, sticky="nsew")
        textSuero.config(yscrollcommand=scrollSuero.set)

        scrollPulsaciones = Scrollbar(
            frameInterno, command=textPulsaciones.yview)
        scrollPulsaciones.grid(row=2, column=3, sticky="nsew")
        textPulsaciones.config(yscrollcommand=scrollPulsaciones.set)
        serv = SalaDoctores()
        thread = threading.Thread(target=serv.iniciar_servidor)
        thread.start()
        raiz.mainloop()
        
        serv.cerrar_servidor()


if __name__ == "__main__":
    # interfaz()
    #serv = RPC()
    #print("Iniciando servidor...")
    # serv.iniciar_servidor()
    Interfaz()
