from tkinter import *
from reportesNFS import *
from functools import partial

class Medico:
  def __init__(self):
    self.guardiaMedica()

  def guardiaMedica(self):

    raiz=Tk()

    raiz.title('ENFERMERIA')
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

    frameDatos=Frame(framePrincipal, width=480, height=350)
    frameDatos.pack()
    frameDatos.config(bg="lightblue")
    framePrincipal.config(relief="groove")
    frameDatos.pack(fill="x", expand=1)
    frameDatos.rowconfigure(0,weight=1)
    frameDatos.rowconfigure(1,weight=1)
    frameDatos.rowconfigure(2,weight=1)
    frameDatos.columnconfigure(0,weight=1)
    frameDatos.columnconfigure(1,weight=1)

    frameBotones=Frame(framePrincipal, width=480, height=30)
    frameBotones.pack()
    frameBotones.config(bg="red")
    frameBotones.pack(fill="x", expand=1)
    imagenLogoHospital= PhotoImage(file="/home/d/Documentos/programacion/proyectoDistribuidas/vistas/DISTRIBUIDAS-INTERFAZ/hospitalV.png")
    imagenLogo= PhotoImage(file="/home/d/Documentos/programacion/proyectoDistribuidas/vistas/DISTRIBUIDAS-INTERFAZ//logo2.png")
    labelLogo= Label(frameEncabezado, image=imagenLogo).grid(pady=5, padx=50,row=0, column=0, sticky=N+S+E+W)
    titulo=Label(frameEncabezado, text="ENFERMERIA")
    titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
    titulo.grid(row=0, column=1, sticky=N+S+E+W)

    labelLogoHospital=Label(frameEncabezado, image=imagenLogoHospital).grid(pady=5, padx=50, row=0, column=2)

    btnReportes=Button(frameBotones, text="Reportes",command= partial(generarInterfaz) )
    btnReportes.pack(fill="both", expand=1)
    Label(frameDatos, text="SUERO").grid(
    row=1, columnspan=3, sticky=(N, S, W, E))

    textSuero = Text(frameDatos, width=30, height=15, state=DISABLED)
    textSuero.grid(row=2, columnspan=2, sticky=(N, S, W, E))

    scrollSuero = Scrollbar(frameDatos, command=textSuero.yview)
    scrollSuero.grid(row=2, column=2, sticky="nsew")
    textSuero.config(yscrollcommand=scrollSuero.set)
    raiz.mainloop()

if __name__=="__main__":
  Medico()
  