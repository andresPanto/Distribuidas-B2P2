from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os


class SubirArchivos:
    nombre_archivo_credenciales = '/home/andres/Desktop/EPN/DISTRIBUIDAS/Distribuidas-B2P2/B2P2/CredencialesQuiq.txt'
    nombre_archivo_a_subir = None
    google_auth = GoogleAuth()
    nombre_carpeta_g_drive = None

    def __init__(self, nombre_archivo_a_subir, nombre_de_carpeta):
        self.nombre_archivo_a_subir = nombre_archivo_a_subir
        self.nombre_carpeta_g_drive = nombre_de_carpeta

    def subir_archivo(self):
        # Cargar credenciales cargadas previamente
        self.google_auth.LoadCredentialsFile(self.nombre_archivo_credenciales)
        print(self.google_auth.credentials)
        if self.google_auth.credentials is None:
            self.google_auth.GetFlow()
            self.google_auth.flow.params.update({'access_type': 'offline'})
            self.google_auth.flow.params.update({'approval_Prompt': 'force'})

            # Autenticarse si no hay credenciales
            self.google_auth.LocalWebserverAuth()
        elif self.google_auth.access_token_expired: 
            # Refrescar la sesion si ha expirado
            self.google_auth.Refresh()
        else:
            # Inicializar credenciales guardadas
            self.google_auth.Authorize()
        # Guardar las credenciales en un archivo
        self.google_auth.SaveCredentialsFile(self.nombre_archivo_credenciales)

    
            
        sesion_google_drive = GoogleDrive(self.google_auth)


        carpetas = sesion_google_drive.ListFile(
            {'q': "title='" + self.nombre_carpeta_g_drive + "' and mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
        for carpeta in carpetas:
            if carpeta['title'] == self.nombre_carpeta_g_drive:
                archivo_de_drive = sesion_google_drive.CreateFile(
                    {'parents': [{'id': carpeta['id']}],
                    'title': self.nombre_archivo_a_subir.split('/')[2]
                    })
                archivo_de_drive.SetContentFile(self.nombre_archivo_a_subir)
                archivo_de_drive.Upload()
                sesion_google_drive.CreateFile({'id':archivo_de_drive['id']}).GetContentFile('eng-dl.txt')
        
        