import xlsxwriter


class Reporte:
    nombre_de_archivo = None
    data = None
    datos_habitacion = None
    path_logo_quiq = './imagenes_interfaz/logoBase.png' 
    def __init__(self, nombre_de_archivo, datos_habitacion, informacion):
        self.nombre_de_archivo = nombre_de_archivo
        self.datos_habitacion = datos_habitacion
        self.data = informacion.data.decode('utf-8')

    def generar_reporte(self):
        fechas = []
        pulsaciones = []
        porcentajes_suero = []
        lineas = self.data.split('\n')
        for i in range(len(lineas) - 1):
            tokens = lineas[i].split(' ')
            fechas.append(tokens[0] + '/ ' + tokens[1])
            pulsaciones.append(int(tokens[3]))
            porcentajes_suero.append(float(tokens[6][:-1]))

        workbook = xlsxwriter.Workbook(self.nombre_de_archivo)
        worksheet = workbook.add_worksheet()
        #Insertar imagen
        worksheet.insert_image('A1', self.path_logo_quiq, {'x_scale': 0.75, 'y_scale': 0.75})
        #worksheet.insert_image('A1', 'logo.png', {'x_offset': 15, 'y_offset': 10})
        #worksheet.insert_image('A1', 'logo.png')


        worksheet.write('A11', 'Habitacion')
        worksheet.write('A12', 'Paciente')
        worksheet.write('A13', 'Fecha / hora de ingreso')
        worksheet.write('B11', self.datos_habitacion['id'])
        worksheet.write(
            'B12', self.datos_habitacion['nombre'] + ' ' + self.datos_habitacion['apellido'])
        worksheet.write('B14', self.datos_habitacion['fechaIngreso'])
        worksheet.write('A15', 'Datos Medicos')
        worksheet.write('A16', 'Fecha y Hora')
        worksheet.write('B16', 'Pulsaciones (ppm)')
        worksheet.write('C16', 'Porcentaje de suero (%)')
        worksheet.write_column('A17', fechas)
        worksheet.write_column('B17', pulsaciones)
        worksheet.write_column('C17', porcentajes_suero)

        chart = workbook.add_chart({'type': 'line'})
        chart.add_series({
            'values': '=Sheet1!$B$17:$B${}'.format(len(pulsaciones) + 6),
            'categories': '=Sheet1!$A$17:$A${}'.format(len(pulsaciones) + 6),
            'name': 'Pulsaciones',
            'marker': {
                'type': 'square',
                        'size': 8,
                        'border': {'color': 'black'},
                        'fill':   {'color': 'red'},
            }
        })

        worksheet.insert_chart('F8', chart)

        # grafico del % de suero
        chart_suero = workbook.add_chart({'type': 'line'})
        chart_suero.add_series({
            'values': '=Sheet1!$C$17:$C${}'.format(len(porcentajes_suero) + 6),
            'categories': '=Sheet1!$A$17:$A${}'.format(len(porcentajes_suero) + 6),
            'name': 'Porcentajes de Sueros',
            'marker': {
                'type': 'square',
                        'size': 8,
                        'border': {'color': 'red'},
                        'fill':   {'color': 'black'},
            }
        })
        worksheet.insert_chart('F29', chart_suero)
        workbook.close()