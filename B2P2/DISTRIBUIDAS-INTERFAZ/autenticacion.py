from tkinter import *

raiz=Tk()

raiz.title('AUTENTICACIÓN')
raiz.resizable(0,0)

framePrincipal=Frame(raiz, width=440,height=520)
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

frameBotones=Frame(framePrincipal, width=480, height=30)
frameBotones.pack()
frameBotones.config(bg="white")
frameBotones.pack(fill="x", expand=1)

imagenLogoHospital= PhotoImage(file="hospitalV.png")
imagenLogo= PhotoImage(file="logo2.png")
labelLogo= Label(frameEncabezado, image=imagenLogo).grid(padx=50,row=0, column=0, sticky=N+S+E+W)
titulo=Label(frameEncabezado, text="AUTENTICACIÓN")
titulo.config(fg="blue",bg="white",font=("Verdana",22)) 
titulo.grid(row=0, column=1, sticky=N+S+E+W)

labelLogoHospital=Label(frameEncabezado, image=imagenLogoHospital).grid(padx=50, row=0, column=2)

btnAtras=Button(frameBotones, text="Atras", font=("Helvetica",14), background='#6883ec')
btnAtras.grid(row=0, column=0, columnspan=3, sticky='NEWS', padx=100)
btnAcceder=Button(frameBotones, text="Acceder",font=("Helvetica",14),background='#6883ec')
btnAcceder.grid(row=0, column=4, columnspan=3, sticky='NEWS', padx=140)

raiz.mainloop()