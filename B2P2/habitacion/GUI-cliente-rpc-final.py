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


def interfaz():

    raiz = Tk()
    #raiz.iconbitmap("quiqsolution.ico")
    raiz.title("Paciente")
    raiz.geometry("650x350")

    frameInterno = Frame(raiz, width=500, height=500)
    frameInterno.pack(fill="both", expand="true")
    frameInterno.rowconfigure(0, weight=1)
    frameInterno.rowconfigure(1, weight=1)
    frameInterno.rowconfigure(2, weight=1)
    frameInterno.rowconfigure(3, weight=1)
    frameInterno.rowconfigure(4, weight=1)
    frameInterno.columnconfigure(0, weight=1)
    frameInterno.columnconfigure(1, weight=1)

    Label(frameInterno, text="Datos del paciente", padx=10, pady=10,
          relief="groove", bd=10).grid(row=0, columnspan=2, sticky=(N, S, W, E))

    labelNombre = Label(frameInterno, text="Nombre:", padx=10, pady=10, )
    labelNombre.grid(row=1, column=0, sticky=(N, S, W, E))

    entryNombre = Entry(frameInterno, font=(18))
    entryNombre.grid(row=1, column=1, sticky=(N, S, W, E))

    labelApellido = Label(frameInterno, text="Apellido:", padx=10, pady=10)
    labelApellido.grid(row=2, column=0, sticky=(N, S, W, E))

    entryApellido = Entry(frameInterno, font=(18))
    entryApellido.grid(row=2, column=1, sticky=(N, S, W, E))

    labelHabitacion = Label(frameInterno, text="Habitación:", padx=10, pady=10)
    labelHabitacion.grid(row=3, column=0, sticky=(N, S, W, E))

    entryHabitacion = Entry(frameInterno, font=(18))
    entryHabitacion.grid(row=3, column=1, sticky=(N, S, W, E))

    def enviar():
        global creado
        global paciente
        creado = 1
        paciente = Cliente(int(entryHabitacion.get()),
                           entryNombre.get(),
                           entryApellido.get())
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

    botonIniciar = Button(frameInterno, text="Enviar",
                          command=enviar, relief="groove", bd=5)
    botonIniciar.grid(row=4, column=0, sticky=(N, S, W, E))

    botonFinalizar = Button(frameInterno, text="Finalizar",
                            command=finalizar, relief="groove", bd=5)
    botonFinalizar.grid(row=4, column=1, sticky=(N, S, W, E))

    raiz.after(500, escanear)
    raiz.mainloop()


if __name__ == "__main__":
    interfaz()
    #paciente = Cliente(17,'JuanJo', 'Morales')
    # paciente.conectar()
    # print(cliente.system.listMethods())
