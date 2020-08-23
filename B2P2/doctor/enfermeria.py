from xmlrpc.server import SimpleXMLRPCServer
import threading
from tkinter import *
from reconocimiento import ReconocimientoFacial
from tkinter import messagebox
from functools import partial
from reportesNFS import *
from subir_archivos import SubirArchivos
from PIL import ImageTk, Image

textSuero = None
textPulsaciones = None


class SalaDoctores():
    HOST = '192.168.43.64'
    PORT = 2530
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
        global textPulsaciones
        habitacion = "En la habitacion: " + str(datos_habitacion['id']) + "\n"
        paciente = "El cliente: " + datos_habitacion['nombre'] + " " + datos_habitacion['apellido'] + "\n"
        suero = "El nivel del suero esta al: " + str(datos_medicos['suero']) + "\n\n"
        textPulsaciones.config(state=NORMAL)
        textPulsaciones.insert(INSERT, habitacion)
        textPulsaciones.insert(INSERT, paciente)
        textPulsaciones.insert(INSERT, suero)
        textPulsaciones.config(state=DISABLED)
        
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




class Medico:
  path_imagen_quiq = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/B2P2/doctor/imagenes_interfaz/logoBase.png'
  path_imagen_hospital = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/B2P2/doctor/imagenes_interfaz/lorem.jpg'
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
    imagenLogoHospital= ImageTk.PhotoImage(Image.open(self.path_imagen_hospital).resize((120,120)))
    imagenLogo= ImageTk.PhotoImage(Image.open(self.path_imagen_quiq).resize((120,120)))
    labelLogo= Label(frameEncabezado, image=imagenLogo, background = "white").grid(pady=5, padx=50,row=0, column=0)
    
    titulo=Label(frameEncabezado, text="ENFERMERIA")
    titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
    titulo.grid(row=0, column=1, sticky=N+S+E+W)

    labelLogoHospital=Label(frameEncabezado, image=imagenLogoHospital, background = "white").grid(pady=5, padx=50, row=0, column=2)

    btnReportes=Button(frameBotones, text="Reportes",command= self.onClick )
    btnReportes.pack(fill="both", expand=1)
    Label(frameDatos, text="SUERO").grid(
    row=1, columnspan=3, sticky=(N+S+W+E))
    global textPulsaciones
    textPulsaciones = Text(frameDatos, width=30,height=10, state=DISABLED)
    textPulsaciones.grid(row=2, columnspan=2, sticky=(N, S, W, E))
    
    scrollPulsaciones = Scrollbar(
    frameDatos, command=textPulsaciones.yview)
    scrollPulsaciones.grid(row=2, column=2, sticky="nsew")
    textPulsaciones.config(yscrollcommand=scrollPulsaciones.set)

    serv = SalaDoctores()
    thread = threading.Thread(target=serv.iniciar_servidor)
    thread.start()
      
    raiz.mainloop()
        
    serv.cerrar_servidor()



  def onClick(self):
  
    respuesta = ReconocimientoFacial().reconocer()
    if respuesta != None:
      SubirArchivos(respuesta['imagen'], 'Imagenes').subir_archivo()
      if respuesta['nombre'] == "Desconocido":
        messagebox.showerror("Rostro desconocido", "Persona no autorizada")
      else:
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Bienvenido!", "Acceso concedido a {}!".format(respuesta['nombre']))
        generarInterfaz()
      
    else:
        messagebox.showerror("Rostro no encontrado", "No se ha encontrado un rostro")




if __name__ == "__main__":
    # interfaz()
    
    Medico()
