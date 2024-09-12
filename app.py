import cv2
from time import sleep
import os
import random
import numpy as np
import keras
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input

model = keras.models.load_model(f"C:/Desenvolvimento/Projetos/seguranca_epi/meu_modelo.keras")

def obter_imagem(caminho):
    img = image.load_img(caminho, target_size=(224, 224))

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x


# URL do stream de vídeo (IP Webcam)
url = "http://192.168.1.100:8080/shot.jpg"

cont = 0

while True:
    # Captura de vídeo
    cap = cv2.VideoCapture(url)
    ret, frame = cap.read()
    if not ret:
        break
    
    # Exibir o frame capturado
    #cv2.imshow('Video', frame)
    cont += 1
    cv2.imwrite(f"C:/Desenvolvimento/Projetos/seguranca_epi/monitoramento/imagens/execucao/imagem_{cont}.jpg", frame)
    sleep(10)

    img, x = obter_imagem(f"C:/Desenvolvimento/Projetos/seguranca_epi/monitoramento/imagens/execucao/imagem_{cont}.jpg")
    probabilidade = model.predict([x])
    probabilidade = model.predict([x])
    probabilidade = probabilidade[0]
    print(f"Probabilidade de ser a classe 0 (correto): {probabilidade[0] * 100}")
    print(f"Probabilidade de ser a classe 1 (errado): {probabilidade[1] * 100}")

cap.release()
cv2.destroyAllWindows()
