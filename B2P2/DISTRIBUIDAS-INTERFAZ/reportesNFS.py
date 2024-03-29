from tkinter import *
import os
import subprocess
from functools import partial

def boton(self):
    entrada = '/mnt/sharedfolder/'+self
    subprocess.call(['libreoffice6.3','--calc',entrada])


def generarInterfaz():
    raiz=Tk()
    interfazReporte = raiz
    interfazReporte.title("Reporte")
    interfazReporte.resizable(0,0)
    framePrincipal=Frame(interfazReporte, width=440,height=520)
    raiz.config(width=480, height=320)
    framePrincipal.pack(fill="both", expand=1)
    framePrincipal.config(bg="white")
    framePrincipal.config(relief="sunken")
    framePrincipal.config(bd=25)
    frameEncabezado=Frame(framePrincipal, width=480, height=10)
    frameEncabezado.pack(fill="x", expand=1)
    frameEncabezado.config(bg="white")
    frameDatos=Frame(framePrincipal, width=480, height=350)
    frameDatos.pack()
    frameDatos.config(bg="lightblue")
    framePrincipal.config(relief="groove")
    frameDatos.pack(fill="x", expand=1)
    frameDatos.columnconfigure(0,weight=1)
    frameDatos.rowconfigure(0,weight=1)
    frameBotones=Frame(framePrincipal, width=480, height=30)
    frameBotones.pack()
    frameBotones.config(bg="#3450be")
    frameBotones.pack(fill="x", expand=1)
    #imagenLogoHospital= PhotoImage(file="hospitalV.png")
    #imagenLogo= PhotoImage(file="logo2.png")
    #Label(frameEncabezado, image=imagenLogo).grid(padx=50,row=0, column=0, sticky=N+S+E+W)
    titulo=Label(frameEncabezado, text="REPORTES")
    titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
    titulo.grid(row=0, column=1, sticky=N+S+E+W)
    #Label(frameEncabezado, image=imagenLogoHospital).grid(padx=50, row=0, column=2)
    btnReportes=Button(frameBotones, text="SALIR", command=interfazReporte.destroy)
    btnReportes.pack(fill="both", expand=1)
    lista = os.listdir("/mnt/sharedfolder")
    for i in lista:
        Button(frameDatos, text=i, command=  partial(boton,i) ).pack(fill="both", expand=1)
    interfazReporte.mainloop()

if __name__=="__main__":
    generarInterfaz()