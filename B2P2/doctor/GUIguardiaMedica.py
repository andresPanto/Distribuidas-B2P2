from tkinter import *
from servermedic import SalaDoctores
from functools import partial
from reconocimiento import ReconocimientoFacial
from subir_archivos import SubirArchivos
from reportesNFS import *
from tkinter import messagebox


class Medico:
  path_imagen_quiq = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/logo2.png'
  path_imagen_hospital = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/doctor/imagenes_interfaz/hospitalV.png'
  sala_doctores = None
  textPulsaciones = None
  def __init__(self):
    
    self.textPulsaciones = Text(frameDatos, width=30,height=10, state=DISABLED)
    self.sala_doctores = SalaDoctores(textPulsaciones).iniciar_servidor()
    self.guardiaMedica()

  def guardiaMedica(self):

    raiz=Tk()

    raiz.title('GUARDIA MÉDICA')
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
    imagenLogoHospital= PhotoImage(file=self.path_imagen_hospital)
    imagenLogo= PhotoImage(file=self.path_imagen_quiq)
    labelLogo= Label(frameEncabezado, image=imagenLogo).grid(pady=5, padx=50,row=0, column=0, sticky=N+S+E+W)
    titulo=Label(frameEncabezado, text="GUARDIA MÉDICA")
    titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
    titulo.grid(row=0, column=1, sticky=N+S+E+W)

    labelLogoHospital=Label(frameEncabezado, image=imagenLogoHospital).grid(pady=5, padx=50, row=0, column=2)

    btnReportes=Button(frameBotones, text="Reportes",command= self.onClick )
    btnReportes.pack(fill="both", expand=1)
    Label(frameDatos, text="PULSACIONES").grid(
    row=1, columnspan=3, sticky=(N+S+W+E))

    
    self.textPulsaciones.grid(row=2, columnspan=2, sticky=(N, S, W, E))
    
    scrollPulsaciones = Scrollbar(
    frameDatos, command=self.textPulsaciones.yview)
    scrollPulsaciones.grid(row=2, column=2, sticky="nsew")
    self.textPulsaciones.config(yscrollcommand=scrollPulsaciones.set)
      
    raiz.mainloop()

  def onClick(self):
  
    respuesta = ReconocimientoFacial().reconocer()
    if respuesta != None:
      #SubirArchivos(respuesta['imagen'], 'Imagenes').subir_archivo()
      if respuesta['imagen'] == "Desconocido":
        messagebox.showerror("Rostro desconocido", "Persona no autorizada")
      else:
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Bienvenido!", "Acceso concedido a {}!".format(respuesta['nombre']))
        generarInterfaz()
      
    else:
        messagebox.showerror("Rostro no encontrado", "No se ha encontrado un rostro")



if __name__=="__main__":
  Medico()
  