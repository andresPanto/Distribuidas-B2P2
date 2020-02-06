import numpy as np 
import face_recognition

data = np.loadtxt('out.txt')
print(data)
print(type(data))
unknown = 'bc2'
unknown_image = face_recognition.load_image_file("bc2.jpg")
unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

result = face_recognition.compare_faces(data, unknown_encoding)
if True in result:
    print('Encontrado')
