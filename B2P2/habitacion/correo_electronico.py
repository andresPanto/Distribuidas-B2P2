import smtplib
from os.path import basename
from getpass import getpass
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


class Email():

    correo_fuente = "quiqsolutionsg1@gmail.com"
    correo_destino = None
    nombre_archivo_enviar = None
    mensaje = None
    nombre_servidor_smtp ='smtp.gmail.com'
    servidor = None
    #port = '465' # for secure messages
    #port = '587' # for normal messages
    puerto_smtp = '465'
    password = "DellG715"

    def __init__(self, destino, nombre_archivo):
        self.correo_destino = destino
        self.nombre_archivo_enviar = nombre_archivo


    def enviar_email(self):
        ## Editar el contenido para que se vea mejor
        contenido = """Un mensaje cualquiera"""

        self.mensaje = MIMEMultipart()
        self.mensaje['From'] = self.correo_fuente
        self.mensaje['To'] = self.correo_destino
        ## Editar el Subject del email
        self.mensaje['Subject'] = 'Envío email'
        self.mensaje.attach(MIMEText(contenido))

        try:

            with open(self.nombre_archivo_enviar, "rb") as file:
                        parte_archivo = MIMEApplication(
                            file.read(),
                            Name=basename(self.nombre_archivo_enviar)
                        )
            
            parte_archivo['Content-Disposition'] = 'attachment; filename="%s"' % basename(self.nombre_archivo_enviar)
            self.mensaje.attach(parte_archivo)
        except:
            return 0



        try:    

            if self.puerto_smtp == '465':
                self.servidor = smtplib.SMTP_SSL('{}:{}'.format(self.nombre_servidor_smtp, self.puerto_smtp))
            else :
                self.servidor = smtplib.SMTP('{}:{}'.format(self.nombre_servidor_smtp, self.puerto_smtp))
                self.servidor.starttls() # Para seguridad
            self.servidor.login(self.correo_fuente, self.password)
            self.servidor.send_message(self.mensaje)
            self.servidor.quit()
            return 1
        except:
            return 0