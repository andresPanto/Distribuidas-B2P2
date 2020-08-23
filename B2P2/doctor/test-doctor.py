from reconocimiento import ReconocimientoFacial
from subir_archivos import SubirArchivos
from tkinter import Tk
from tkinter import messagebox
from functools import partial
from reportesNFS import *


respuesta = ReconocimientoFacial().reconocer()
if respuesta != None:
    
    if respuesta['nombre'] == "Desconocido":
        messagebox.showerror("Rostro desconocido", "Persona no autorizada")
    else:
        
        print(respuesta['nombre'])
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Bienvenido!", "Acceso concedido a {}!".format(respuesta['nombre']))
        generarInterfaz()
        
    #SubirArchivos(respuesta['imagen'], 'Imagenes').subir_archivo()
    
else:
    messagebox.showerror("Rostro no encontrado", "No se ha encontrado un rostro")