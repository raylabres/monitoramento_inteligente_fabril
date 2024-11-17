from flask import Flask, render_template, url_for, redirect, send_from_directory
import cv2
import shutil
from time import sleep
import numpy as np
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import threading
import os
import torch
import sys
from datetime import datetime

app = Flask(__name__)

executando = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/executar")
def executar():
    global executando
    executando = True

    # Variáveis úteis
    pasta_temp = "execucao/temp"
    pasta_correta = "execucao/corretas"
    pasta_errada = "execucao/erradas"
    url_ala_1 = "http://10.118.128.232:8080/shot.jpg"
    url_ala_2 = "http://10.118.128.51:8080/shot.jpg"
    url_ala_3 = "http://10.118.130.141111:8080/shot.jpg"

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

    def detectar_pessoa(caminho_imagem):
        model = torch.hub.load('ultralytics/yolov5', 'yolov5s', verbose=False) # Carregar o modelo YOLOv5
        img = cv2.imread(caminho_imagem) # Carregar a imagem
        results = model(img)  # Realizar a inferência

        # Processar os resultados
        results_df = results.pandas().xyxy[0]  # Extrai as caixas delimitadoras como DataFrame

        # Verificar se há detecções de "pessoas"
        if any(results_df['name'] == 'person'):
            return True
        else:
            return False

    def ala_1():
        #cont = 0
        while executando:
            try:
                ala = "Ala 1"

                cap = cv2.VideoCapture(url_ala_1)  # Captura de vídeo
                ret, frame = cap.read()
                if not ret:
                    break
                
                #cv2.imshow('Video', frame) # Exibir o frame capturado
                #cont += 1
                data = datetime.now()
                data = data.strftime("Data - %d-%m-%Y Hora - %H-%M-%S")
                caminho_imagem = f"{pasta_temp}/{ala} - {data}.jpg"
                cv2.imwrite(caminho_imagem, frame)

                pessoa_na_imagem = detectar_pessoa(caminho_imagem)

                if pessoa_na_imagem:
                    img, x = obter_imagem(caminho_imagem)
                    probabilidade = modelo.predict([x])
                    probabilidade = probabilidade[0]
        
                    probabilidade_correto = probabilidade[0] * 100
                    probabilidade_errado = probabilidade[1] * 100

                    print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
                    print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

                    if probabilidade_errado > probabilidade_correto:
                        shutil.move(caminho_imagem, f"{pasta_errada}/{ala} - {data}.jpg")
                    else:
                        os.remove(caminho_imagem)
                    
                    cap.release()
                    cv2.destroyAllWindows()
                else:
                    os.remove(caminho_imagem)
            except Exception as erro:
                print(f"Erro na camera: {erro}")
            
            finally:
                cap.release()
                cv2.destroyAllWindows()


    def ala_2():
        cont = 0
        while executando:
            try:
                ala = "Ala 2"

                cap = cv2.VideoCapture(url_ala_2)  # Captura de vídeo
                ret, frame = cap.read()
                if not ret:
                    break
                
                #cv2.imshow('Video', frame) # Exibir o frame capturado
                #cont += 1
                data = datetime.now()
                data = data.strftime("Data - %d-%m-%Y Hora - %H-%M-%S")
                caminho_imagem = f"{pasta_temp}/{ala} - {data}.jpg"
                cv2.imwrite(caminho_imagem, frame)

                pessoa_na_imagem = detectar_pessoa(caminho_imagem)

                if pessoa_na_imagem:
                    img, x = obter_imagem(caminho_imagem)
                    probabilidade = modelo.predict([x])
                    probabilidade = probabilidade[0]
        
                    probabilidade_correto = probabilidade[0] * 100
                    probabilidade_errado = probabilidade[1] * 100

                    print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
                    print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

                    if probabilidade_errado > probabilidade_correto:
                        shutil.move(caminho_imagem, f"{pasta_errada}/{ala} - {data}.jpg")
                    else:
                        os.remove(caminho_imagem)
                    
                else:
                    os.remove(caminho_imagem)
            except Exception as erro:
                print(f"Erro na camera: {erro}")

            finally:
                cap.release()
                cv2.destroyAllWindows()

    def ala_3():
        cont = 0
        while executando:
            try:
                ala = "Ala 3"

                cap = cv2.VideoCapture(url_ala_3)  # Captura de vídeo
                ret, frame = cap.read()
                if not ret:
                    break
                
                #cv2.imshow('Video', frame) # Exibir o frame capturado
                #cont += 1
                data = datetime.now()
                data = data.strftime("Data - %d-%m-%Y Hora - %H-%M-%S")
                caminho_imagem = f"{pasta_temp}/{ala} - {data}.jpg"
                cv2.imwrite(caminho_imagem, frame)

                pessoa_na_imagem = detectar_pessoa(caminho_imagem)

                if pessoa_na_imagem:
                    img, x = obter_imagem(caminho_imagem)
                    probabilidade = modelo.predict([x])
                    probabilidade = probabilidade[0]
        
                    probabilidade_correto = probabilidade[0] * 100
                    probabilidade_errado = probabilidade[1] * 100

                    print(f"Probabilidade de ser a classe 0 (correto): {probabilidade_correto}")
                    print(f"Probabilidade de ser a classe 1 (errado): {probabilidade_errado}")

                    if probabilidade_errado > probabilidade_correto:
                        shutil.move(caminho_imagem, f"{pasta_errada}/{ala} - {data}.jpg")
                    else:
                        os.remove(caminho_imagem)
                    
                else:
                    os.remove(caminho_imagem)
            except Exception as erro:
                print(f"Erro na camera: {erro}")

            finally:
                cap.release()
                cv2.destroyAllWindows()

    thread_ala_1 = threading.Thread(target=ala_1)
    thread_ala_2 = threading.Thread(target=ala_2)
    thread_ala_3 = threading.Thread(target=ala_3)

    thread_ala_1.start()
    thread_ala_2.start()
    thread_ala_3.start()

    thread_ala_1.join()
    thread_ala_2.join()
    thread_ala_3.join()

    #print("Todas as Thread foram finalizadas!")

    return redirect(url_for('index'))  

@app.route("/ultimas_ocorrencias")
def ultimas_ocorrencias():
    # Atualizando a lógica para buscar as imagens
    image_folder = os.path.join('execucao', 'erradas')
    images = os.listdir(image_folder)

    # Formatar os nomes das imagens
    formatted_images = [
        {
            'path': url_for('get_image', filename=image),
            # Ajustando a formatação do nome da imagem para manter os hífens
            'name': image.rsplit('/', 1)[-1].rsplit('.', 1)[0].replace('-', ' - ')  # Mantém os hífens entre os elementos
        } for image in images if image.endswith(('png', 'jpg', 'jpeg'))
    ]

    return render_template("ultimas_ocorrencias.html", images=formatted_images)

@app.route("/sistema_fechado")
def sistema_fechado():
    global executando
    executando = False
    return render_template("sistema_fechado.html")

@app.route("/retornar")
def retornar():
    return render_template("index.html")

@app.route("/atualizar")
def atualizar():
    return redirect(url_for('ultimas_ocorrencias'))

@app.route('/get_image/<path:filename>')
def get_image(filename):
    return send_from_directory(os.path.join('execucao', 'erradas'), filename)

if __name__ == '__main__':
    app.run(debug=True)
