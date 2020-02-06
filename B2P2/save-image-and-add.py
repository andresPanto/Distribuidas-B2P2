import cv2
import face_recognition
import numpy as np

cam = cv2.VideoCapture(0)

cv2.namedWindow("test")

img_counter = 0

while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        img_name = "photo_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        imgaen_cargada = face_recognition.load_image_file(img_name)
        data_nueva_imagen = face_recognition.face_encodings(imgaen_cargada)[0]
        data = np.loadtxt('out.txt')
        lista =  data.tolist()
        lista.append(data_nueva_imagen)
        data = np.array(lista)
        with open('out.txt', 'wb+') as archivo:
            np.savetxt(archivo, data,  fmt='%4.1f')

        print('Registrado')
        img_counter += 1


cam.release()

cv2.destroyAllWindows()