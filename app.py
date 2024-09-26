import cv2
import shutil
from time import sleep
import numpy as np
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import threading
import os

# Variáveis úteis
pasta_temp = "execucao/temp"
pasta_correta = "execucao/corretas"
pasta_errada = "execucao/erradas"
url_ala_1 = "http://192.168.1.101:8080/shot.jpg"
url_ala_2 = "http://192.168.1.101:8080/shot.jpg"
url_ala_3 = "http://192.168.1.101:8080/shot.jpg"

modelo = load_model(f"modelo_seguranca_epi.keras")

arquivos = os.listdir(pasta_temp)
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_temp, arquivo)
    os.remove(caminho_arquivo)

arquivos = os.listdir(pasta_correta)
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_correta, arquivo)
    os.remove(caminho_arquivo)

arquivos = os.listdir(pasta_errada)
for arquivo in arquivos:
    caminho_arquivo = os.path.join(pasta_errada, arquivo)
    os.remove(caminho_arquivo)
A
def obter_imagem(caminho):
    # Carregar e redimensionar a imagem
    img = image.load_img(caminho, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)

    # Processar a imagem para melhorar a qualidade
    x = preprocess_input(x)

    # Converte a imagem para o formato de OpenCV para aplicar os tratamentos
    img_cv = cv2.cvtColor(x[0], cv2.COLOR_RGB2BGR)  # converter de RGB para BGR

    # Aplicar tratamentos
    imagem_tratada = cv2.resize(img_cv, (224, 224), interpolation=cv2.INTER_CUBIC)
    imagem_tratada = cv2.GaussianBlur(imagem_tratada, (5, 5), 0)
    imagem_tratada = cv2.convertScaleAbs(imagem_tratada, alpha=1.5, beta=50)
    imagem_cinza = cv2.cvtColor(imagem_tratada, cv2.COLOR_BGR2GRAY)
    imagem_equalizada = cv2.equalizeHist(imagem_cinza)
    imagem_tratada = cv2.cvtColor(imagem_equalizada, cv2.COLOR_GRAY2BGR)
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    imagem_tratada = cv2.filter2D(imagem_tratada, -1, kernel)

    # Converter a imagem tratada de volta para o formato esperado pelo modelo
    x_tratada = np.expand_dims(imagem_tratada, axis=0)
    x_tratada = preprocess_input(x_tratada)

    return img, x

def ala_1():
    cont = 0
    while True:
        try:
            ala = "ala_1"

            cap = cv2.VideoCapture(url_ala_1)  # Captura de vídeo
            ret, frame = cap.read()
            if not ret:
                break
            
            #cv2.imshow('Video', frame) # Exibir o frame capturado
            cont += 1
            cv2.imwrite(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", frame)

            img, x = obter_imagem(f"{pasta_temp}/imagem_{ala}_{cont}.jpg")
            probabilidade = modelo.predict([x])
            probabilidade = probabilidade[0]
   
            probabilidade_correto = probabilidade[0] * 100
            probabilidade_errado = probabilidade[1] * 100

            print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
            print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

            if probabilidade_errado > probabilidade_correto:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_errada}/imagem_{ala}_{cont}.jpg")
            else:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_correta}/imagem_{ala}_{cont}.jpg")
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as erro:
            print(f"Erro na camera: {erro}")

def ala_2():
    cont = 0
    while True:
        try:
            ala = "ala_2"

            cap = cv2.VideoCapture(url_ala_2)  # Captura de vídeo
            ret, frame = cap.read()
            if not ret:
                break
            
            #cv2.imshow('Video', frame) # Exibir o frame capturado
            cont += 1
            cv2.imwrite(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", frame)

            img, x = obter_imagem(f"{pasta_temp}/imagem_{ala}_{cont}.jpg")
            probabilidade = modelo.predict([x])
            probabilidade = probabilidade[0]
   
            probabilidade_correto = probabilidade[0] * 100
            probabilidade_errado = probabilidade[1] * 100

            print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
            print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

            if probabilidade_errado > probabilidade_correto:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_errada}/imagem_{ala}_{cont}.jpg")
            else:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_correta}/imagem_{ala}_{cont}.jpg")
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as erro:
            print(f"Erro na camera: {erro}")



def ala_3():
    cont = 0
    while True:
        try:
            ala = "ala_3"

            cap = cv2.VideoCapture(url_ala_3)  # Captura de vídeo
            ret, frame = cap.read()
            if not ret:
                break
            
            #cv2.imshow('Video', frame) # Exibir o frame capturado
            cont += 1
            cv2.imwrite(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", frame)

            img, x = obter_imagem(f"{pasta_temp}/imagem_{ala}_{cont}.jpg")
            probabilidade = modelo.predict([x])
            probabilidade = probabilidade[0]
   
            probabilidade_correto = probabilidade[0] * 100
            probabilidade_errado = probabilidade[1] * 100

            print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
            print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

            if probabilidade_errado > probabilidade_correto:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_errada}/imagem_{ala}_{cont}.jpg")
            else:
                shutil.move(f"{pasta_temp}/imagem_{ala}_{cont}.jpg", f"{pasta_correta}/imagem_{ala}_{cont}.jpg")
            
            cap.release()
            cv2.destroyAllWindows()
        except Exception as erro:
            print(f"Erro na camera: {erro}")


thread_ala_1 = threading.Thread(target=ala_1)
thread_ala_2 = threading.Thread(target=ala_2)
thread_ala_3 = threading.Thread(target=ala_3)

thread_ala_1.start()
thread_ala_2.start()
thread_ala_3.start()

thread_ala_1.join()
thread_ala_2.join()
thread_ala_3.join()

print("Todas as Thread foram finalizadas!")