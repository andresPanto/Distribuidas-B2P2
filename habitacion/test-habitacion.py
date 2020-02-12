from correo_electronico import Email
from subir_archivos import SubirArchivos

class Test:
    def __init__(self):
        '''
        mail = Email("andrespantojaxv@gmail.com", "client_secrets.json").enviar_email()
        if mail == 1:
            print('Correo enviado correctamente')
        else:
            print('No se ha enviado el correo')
        '''
        subida_de_archivos = SubirArchivos('CredencialesQuiq.txt', 'Reportes').subir_archivo()
        

test = Test()