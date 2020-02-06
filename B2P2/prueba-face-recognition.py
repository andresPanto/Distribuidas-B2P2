import face_recognition
import numpy as np

imagenes = [ 'ce', 'ch', 'cp', 'rdjr', 'slj', 'bc']

datos = []


unknown = 'bc2'
unknown_image = face_recognition.load_image_file("bc2.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]


for imagen in imagenes:
    print(imagen)
    known_image = face_recognition.load_image_file('./imagenes/'+ imagen+ '.jpg')
    known_encoding = face_recognition.face_encodings(known_image)[0]
    print(known_encoding)
    print(type(known_encoding))
    datos.append(known_encoding)
    result = face_recognition.compare_faces([known_encoding], unknown_encoding)
    print(result)

    if result[0] == True:
        print("It's a picture of me!")
    else:
        print("It's not a picture of me!")
print("Works")
print(datos)

with open('out.txt', 'wb+') as archivo:
    np.savetxt(archivo, datos,  fmt='%4.1f')