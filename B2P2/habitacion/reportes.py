import xlsxwriter

class Reporte:
    nombre_de_archivo = None
    data = None
    datos_habitacion = None
    def __init__(self, nombre_de_archivo, datos_habitacion, informacion)
        self.nombre_de_archivo = nombre_de_archivo
        self.datos_habitacion = datos_habitacion
        self.data = informacion

    def generar_reporte:
        fechas = []
        pulsaciones = []
        porcentajes_suero = []
        lineas = self.data.split('\n')
        for i in range(len(lineas) - 1):
            tokens = lineas[i].split(' ')
            fechas.append(tokens[0] + '/ ' + tokens[1])
            pulsaciones.append(int(tokens[3]))
            porcentajes_suero.append(float(tokens[6][:-1]))

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
        worksheet.write('B6', 'Pulsaciones (ppm)')
        worksheet.write('C6', 'Porcentaje de suero (%)')
        worksheet.write_column('A7', fechas)
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
