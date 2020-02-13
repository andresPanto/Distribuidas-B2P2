import face_recognition
import cv2
import numpy as np
import time
import datetime

class ReconocimientoFacial:

    pantalla_captura = None
    caras_conocidas = None
    nombres_conocidos = None
    nombre_encontrado = 'Desconocido'
    fichero = './imagenes/'
    path_out = './datos_reconocimiento/out.txt'
    path_nombres = './datos_reconocimiento/nombres.txt'
    def __init__(self):
        self.pantalla_captura = cv2.VideoCapture(0)
        self.caras_conocidas = np.loadtxt(self.path_out)
        with open(self.path_nombres, 'r') as archivo:
            self.nombres_conocidos = archivo.read().splitlines()
        
        



# Create arrays of known face encodings and their names



# Initialize some variables
    def reconocer(self):
        
        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

     
    # Grab a single frame of video
        ret, frame = self.pantalla_captura.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(self.caras_conocidas, face_encoding)
                name = None

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(self.caras_conocidas, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    self.nombre_encontrado = self.nombres_conocidos[best_match_index]
                tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                img_name = "{}Acceso_de_{}_el_{}.png".format(
                    self.fichero, self.nombre_encontrado, tiempo)
                    
                cv2.imwrite(img_name, frame)
                respuesta = {
                    "nombre": self.nombre_encontrado,
                    "imagen": img_name,
                }
                return respuesta
        

        # Release handle to the webcam
        self.pantalla_captura.release()
        cv2.destroyAllWindows()