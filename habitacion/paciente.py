import xmlrpc.client
import time
import xlsxwriter
from datetime import datetime
from random import *
from tkinter import *
import os
import sys
from habitacion import Habitacion


paciente = None
creado = 0

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
    path_imagen_quiq = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/logo2.png'
    path_imagen_hospital = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/hospitalV.png'

#LINK = 'http://' + HOST + ':' + str(PORT)
    def __init__(self, id, nombre, apellido):


    def paciente():
        raiz=Tk()
        raiz.title('PACIENTE')
        raiz.resizable(0,0)

        framePrincipal=Frame(raiz, width=480,height=520)
        raiz.config(width=480, height=320)
        framePrincipal.pack(fill="both", expand=1)
        framePrincipal.config(bg="white")
        framePrincipal.config(relief="sunken")
        framePrincipal.config(bd=25)


        frameEncabezado=Frame(framePrincipal, width=480, height=10)
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

        frameBotones=Frame(framePrincipal, width=480, height=30)
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

        btnInicializar=Button(frameBotones, text="Inicializar",command=enviar)
        btnInicializar.grid(row=0,column=0,sticky=(N, S, W, E))

        btnFinalizar=Button(frameBotones, text="Finalizar",command=finalizar)
        btnFinalizar.grid(row=0,column=1,sticky=(N, S, W, E))

        Label(frameDatos, text="NOMBRE").grid(row=0, column=0, sticky=(N+S+W+E))

        Label(frameDatos, text="APELLIDO",width=35).grid(
        row=1, column=0, sticky=(N, S, W, E))

        Label(frameDatos, text="HABITACION").grid(
        row=2, column=0, sticky=(N, S, W, E))

        Label(frameDatos, text="CORREO").grid(
        row=3, column=0, sticky=(N, S, W, E))

        txtNombre = Text(frameDatos, width=30, height=3)
        txtNombre.grid(row=0, column=1, sticky=(N,W,S,E))

        txtApellido = Text(frameDatos, width=30, height=3)
        txtApellido.grid(row=1, column=1, sticky=(N, W, S, E))

        txtHabitacion = Text(frameDatos, width=30, height=3)
        txtHabitacion.grid(row=2, column=1, sticky=(N,  W, S, E))

        txtCorreo = Text(frameDatos, width=30, height=3)
        txtCorreo.grid(row=3, column=1, sticky=(N,  W, S, E))

        #raiz.after(500,escanear)
        raiz.mainloop()

    def enviar():
        global creado
        global paciente
        creado = 1
        self.id_habitacion = int(txtHabitacion.get())
        self.nombre_paciente = txtNombre.get()
        self.apellido_paciente = txtApellido.get()
        self.correo_paciente = txtCorreo.get()
        self.paciente = Paciente(self.id_habitacion, self.nombre_paciente, self.apellido_paciente, self.correo_paciente)
        self.paciente.enviar_datos()
        botonIniciar.config(state=DISABLED)
        entryNombre.config(state=DISABLED)
        entryApellido.config(state=DISABLED)
        entryHabitacion.config(state=DISABLED)
        raiz.after(500, escanear)

    def finalizar():
        global creado
        creado = 0
        self.paciente.parar_conexion()
        botonIniciar.config(state=NORMAL)
        entryNombre.config(state=NORMAL)
        entryApellido.config(state=NORMAL)
        entryHabitacion.config(state=NORMAL)
        sys.exit()
            

    def escanear():
        global creado
        if creado == 0:
            pass    #print("nada")
        else:
            self.paciente.enviar_datos()
        raiz.after(500, escanear)

    if __name__=="__main__":
        paciente()
            