import xmlrpc.client
import time
import xlsxwriter
from datetime import datetime
from random import *
from tkinter import *
import os
import sys
from habitacion import Paciente
from queue import *
import threading



class GUICliente:
    datos_habitacion = None
    instancia_servidor = None
    nombre_archivo = None
    habitacion_rpc = None
    paciente = None
    nombre_paciente = None
    apellido_paciente = None
    correo_paciente = None
    id_habitacion = None
    txtHabitacion = None
    txtApellido = None
    txtCorreo = None
    txtNombre = None
    raiz = None
    creado = 0
    botonIniciar = None
    botonFinalizar = None
    queue =  Queue()
    path_imagen_quiq = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/logo2.png'
    path_imagen_hospital = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/hospitalV.png'

#LINK = 'http://' + HOST + ':' + str(PORT)


    def paciente(self):
        self.raiz=Tk()
        self.raiz.title('PACIENTE')
        self.raiz.resizable(0,0)
        self.raiz.geometry('650x350')

        framePrincipal=Frame(self.raiz, width=480,height=520)
        self.raiz.config(width=480, height=320)
        framePrincipal.pack(fill="both", expand=1)
        framePrincipal.config(bg="white")
        framePrincipal.config(relief="sunken")
        framePrincipal.config(bd=25)


        frameEncabezado=Frame(framePrincipal, width=480, height=100)
        frameEncabezado.pack(fill="x", expand=1)

        frameEncabezado.config(bg="white")
        frameEncabezado.rowconfigure(0,weight=1)
        frameEncabezado.columnconfigure(0,weight=1)
        frameEncabezado.columnconfigure(1,weight=1)
        frameEncabezado.columnconfigure(2,weight=1)

        frameDatos=Frame(framePrincipal, width=480, height=350)
        frameDatos.pack()
        frameDatos.config(bg="lightblue")
        framePrincipal.config(relief="groove")
        frameDatos.pack(fill="x", expand=1)
        frameDatos.rowconfigure(0,weight=1)
        frameDatos.columnconfigure(0,weight=1)

        frameBotones=Frame(framePrincipal, width=480, height=100)
        frameBotones.pack()
        frameBotones.config(bg="lightgrey")
        frameBotones.pack(fill="both", expand=1)
        frameBotones.rowconfigure(0,weight=1)
        frameBotones.columnconfigure(0,weight=1)
        frameBotones.columnconfigure(1,weight=1)
        imagenLogoHospital= PhotoImage(file=self.path_imagen_hospital)
        imagenLogo= PhotoImage(file=self.path_imagen_quiq)
        labelLogo= Label(frameEncabezado, image=imagenLogo).grid(pady=10, padx=10,row=0, column=0, sticky=N+S+E+W)
        titulo=Label(frameEncabezado, text="PACIENTE")
        titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
        titulo.grid(row=0, column=1, sticky=N+S+E+W)

        labelLogoHospital=Label(frameEncabezado, image=imagenLogoHospital).grid(pady=5, padx=50, row=0, column=2)

        self.botonIniciar=Button(frameBotones, text="Inicializar",command=self.enviar)
        self.botonIniciar.grid(row=0,column=0,sticky=(N, S, W, E))

        self.botonFinalizar=Button(frameBotones, text="Finalizar",command=self.finalizar)
        self.botonFinalizar.grid(row=0,column=1,sticky=(N, S, W, E))
        

        Label(frameDatos, text="NOMBRE").grid(row=0, column=0, sticky=(N+S+W+E))

        Label(frameDatos, text="APELLIDO",width=35).grid(
        row=1, column=0, sticky=(N, S, W, E))

        Label(frameDatos, text="HABITACION").grid(
        row=2, column=0, sticky=(N, S, W, E))

        Label(frameDatos, text="CORREO").grid(
        row=3, column=0, sticky=(N, S, W, E))

        self.txtNombre = Entry(frameDatos, font=(28))
        self.txtNombre.grid(row=0, column=1, sticky=(N,W,S,E))

        self.txtApellido = Entry(frameDatos, font=(28))
        self.txtApellido.grid(row=1, column=1, sticky=(N, W, S, E))

        self.txtHabitacion = Entry(frameDatos, font=(28))
        self.txtHabitacion.grid(row=2, column=1, sticky=(N,  W, S, E))

        self.txtCorreo = Entry(frameDatos, font=(28))
        self.txtCorreo.grid(row=3, column=1, sticky=(N,  W, S, E))
        self.raiz.after(500, self.process_queue)
        self.raiz.mainloop()
        

    def enviar(self):
        
        
        self.id_habitacion = int(self.txtHabitacion.get())
        self.nombre_paciente = self.txtNombre.get()
        self.apellido_paciente = self.txtApellido.get()
        self.correo_paciente = self.txtCorreo.get()
        self.paciente = Paciente(self.id_habitacion, self.nombre_paciente, self.apellido_paciente, self.correo_paciente)
        self.botonIniciar.config(state=DISABLED)
        self.txtNombre.config(state=DISABLED)
        self.txtApellido.config(state=DISABLED)
        self.txtHabitacion.config(state=DISABLED)
        self.txtCorreo.config(state=DISABLED)
        self.botonFinalizar.config(state = NORMAL)
        self.creado = 1
        
        
        ThreadedTask(self.queue, self.paciente).start()
        self.raiz.after(500, self.process_queue)
        
        



    def finalizar(self):
        
        if self.creado == 1:
            self.creado = 0
            
            self.paciente.parar_conexion()
            self.botonIniciar.config(state=NORMAL)
            self.txtNombre.config(state=NORMAL)
            self.txtApellido.config(state=NORMAL)
            self.txtHabitacion.config(state=NORMAL)
            self.txtCorreo.config(state=NORMAL)
            sys.exit()
            

    
    def escanear(self):
        
        if self.creado == 0:
            pass    #print("nada")
        else:
            self.paciente.enviar_datos()
        self.raiz.after(500, self.escanear)

    
    def process_queue(self):
        try:
            msg = self.queue.get(0)
            # Show result of the task if needed
            #self.prog_bar.stop()
        except Empty:
            self.raiz.after(100, self.process_queue)



    
class ThreadedTask(threading.Thread):
    def __init__(self, queue, paciente):
        threading.Thread.__init__(self)
        self.queue = queue
        self.paciente = paciente
    def run(self):
        self.paciente.enviar_datos()
        self.queue.put("Task finished")

if __name__=="__main__":
   GUICliente().paciente()
            