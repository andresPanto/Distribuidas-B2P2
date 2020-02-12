import xmlrpc.client
import time
import xlsxwriter
from datetime import datetime
from random import *
from tkinter import *
import os
import sys

paciente = None
creado = 0

class Cliente:
    datos_habitacion = None
    instancia_servidor = None
    nombre_archivo = None

#LINK = 'http://' + HOST + ':' + str(PORT)
    def __init__(self, id, nombre, apellido):
        self.instancia_servidor = xmlrpc.client.ServerProxy(
            'http://192.168.43.64:2527')
        self.datos_habitacion = {
            "id": id,
            "nombre": nombre,
            "apellido": apellido,
            "fechaIngreso": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.iniciar_conexion()

    def iniciar_conexion(self):
        self.instancia_servidor.acepta_conexion(self.datos_habitacion)

    def enviar_datos(self):
        # self.iniciar_conexion()
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
        #print("Datos enviados...")
        #print("Termina de enviar datos")

    def parar_conexion(self):
        #print("Termina de enviar datos")
        #informacion_binaria = self.instancia_servidor.cierra_conexion*(self.datos_habitacion)
        informacion = self.instancia_servidor.cierra_conexion(
            self.datos_habitacion)
        #print(informacion)
        #print(type(informacion))
        if os.name == 'nt':
            self.datos_habitacion["fechaIngreso"] = self.datos_habitacion["fechaIngreso"].replace(':','_')
        self.nombre_archivo = 'Reporte_' + self.datos_habitacion["nombre"] + '_' + self.datos_habitacion["apellido"] + '_' + str(self.datos_habitacion["id"]) + self.datos_habitacion["fechaIngreso"] + ".xlsx"
        self.crear_reporte(informacion.data.decode("utf-8"))

    def crear_reporte(self, data):
        fechas = []
        #horas = []
        pulsaciones = []
        porcentajes_suero = []
        lineas = data.split('\n')
        for i in range(len(lineas) - 1):
            tokens = lineas[i].split(' ')
            fechas.append(tokens[0] + '/ ' + tokens[1])
            #horas.append(tokens[1])
            pulsaciones.append(int(tokens[3]))
            porcentajes_suero.append(float(tokens[6][:-1]))
            # print(tokens)
        #print(porcentajes_suero)
        #print(horas)
        #print(fechas)
        #print(pulsaciones)
        workbook = xlsxwriter.Workbook(self.nombre_archivo)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'Habitacion')
        worksheet.write('A2', 'Paciente')
        worksheet.write('A3', 'Fecha / hora de ingreso')
        worksheet.write('B1', self.datos_habitacion['id'])
        worksheet.write(
            'B2', self.datos_habitacion['nombre'] + ' ' + self.datos_habitacion['apellido'])
        worksheet.write('B3', self.datos_habitacion['fechaIngreso'])
        worksheet.write('A5', 'Datos Medicos')
        worksheet.write('A6', 'Fecha y Hora')
        #worksheet.write('B6', 'Hora')
        worksheet.write('B6', 'Pulsaciones (ppm)')
        worksheet.write('C6', 'Porcentaje de suero (%)')
        worksheet.write_column('A7', fechas)
        #worksheet.write_column('B7', horas)
        worksheet.write_column('B7', pulsaciones)
        worksheet.write_column('C7', porcentajes_suero)

        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'values': '=Sheet1!$B$7:$B${}'.format(len(pulsaciones) + 6),
            'categories': '=Sheet1!$A$7:$A${}'.format(len(pulsaciones) + 6),
            'name': 'Pulsaciones',
            'marker': {
                'type': 'square',
                        'size': 8,
                        'border': {'color': 'black'},
                        'fill':   {'color': 'red'},
            }
        })

        worksheet.insert_chart('F3', chart)

        # grafico del % de suero
        chart_suero = workbook.add_chart({'type': 'line'})
        chart_suero.add_series({
            'values': '=Sheet1!$C$7:$C${}'.format(len(porcentajes_suero) + 6),
            'categories': '=Sheet1!$A$7:$A${}'.format(len(porcentajes_suero) + 6),
            'name': 'Porcentajes de Sueros',
            'marker': {
                'type': 'square',
                        'size': 8,
                        'border': {'color': 'red'},
                        'fill':   {'color': 'black'},
            }
        })
        worksheet.insert_chart('F19', chart_suero)
        workbook.close()


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
        imagenLogoHospital= PhotoImage(file="/home/d/Documentos/programacion/proyectoDistribuidas/vistas/DISTRIBUIDAS-INTERFAZ/hospitalV.png")
        imagenLogo= PhotoImage(file="/home/d/Documentos/programacion/proyectoDistribuidas/vistas/DISTRIBUIDAS-INTERFAZ/logo2.png")
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
        paciente = Cliente(int(entryHabitacion.get()),entryNombre.get(),entryApellido.get())
        botonIniciar.config(state=DISABLED)
        entryNombre.config(state=DISABLED)
        entryApellido.config(state=DISABLED)
        entryHabitacion.config(state=DISABLED)
        raiz.after(500, escanear)

def finalizar():
        global paciente
        global creado
        creado = 0
        paciente.parar_conexion()
        botonIniciar.config(state=NORMAL)
        entryNombre.config(state=NORMAL)
        entryApellido.config(state=NORMAL)
        entryHabitacion.config(state=NORMAL)
        sys.exit()
        

def escanear():
        global paciente
        global creado
        if creado == 0:
            pass    #print("nada")
        else:
            paciente.enviar_datos()
        raiz.after(500, escanear)

if __name__=="__main__":
    paciente()
        