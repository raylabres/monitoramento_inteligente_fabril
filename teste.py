import cv2
import numpy as np
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import matplotlib.pyplot as plt

# Variáveis úteis
pasta_temp = "execucao/temp"

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

    return imagem_tratada, x_tratada

modelo = load_model(f"modelo_seguranca_epi.keras")

img, x = obter_imagem(r"C:\Users\thera\Downloads\teste2.jpeg")
probabilidade = modelo.predict([x])
probabilidade = probabilidade[0]

probabilidade_correto = probabilidade[0] * 100
probabilidade_errado = probabilidade[1] * 100

plt.figure(figsize=(16, 4))
plt.imshow(img)
plt.axis("off")
plt.show()

print(probabilidade_correto)
print(probabilidade_errado)