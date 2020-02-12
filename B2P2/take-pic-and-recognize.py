import cv2
import numpy as np
import face_recognition

class Reconocimiento:
    

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("Reconocimiento Facial")

    nombre_imagen = None

    def mostar_pantalla

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
        img_name = "pic_{}.png".format(img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        data = np.loadtxt('out.txt')
        unknown_image = face_recognition.load_image_file(img_name)
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        result = face_recognition.compare_faces(data, unknown_encoding)
        if True in result:
            print('Encontrado')
        else:
            print('No Encontrado')

        img_counter += 1

    cam.release()

    cv2.destroyAllWindows()