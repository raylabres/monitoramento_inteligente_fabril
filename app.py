from flask import Flask, render_template, url_for, redirect, send_from_directory
import cv2
import shutil
import numpy as np
from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import threading
import os
import torch
from datetime import datetime
import json

app = Flask(__name__)

executando = False

# Pastas usadas
PASTA_TEMP = "execucao/temp"
PASTA_CORRETA = "execucao/corretas"
PASTA_ERRADA = "execucao/erradas"
PASTA_ENDERECOS = "execucao/enderecos_ips"
ARQUIVO_IPS = os.path.join(PASTA_ENDERECOS, "ips.json")

def garantir_pastas():
    os.makedirs(PASTA_ENDERECOS, exist_ok=True)

def criar_arquivo_ips_padrao():
    garantir_pastas()
    if not os.path.isfile(ARQUIVO_IPS):
        with open(ARQUIVO_IPS, "w") as f:
            json.dump(["", "", "", ""], f, indent=4)
        print(f"Arquivo criado: {ARQUIVO_IPS}")
    else:
        print("Arquivo já existe.")

criar_arquivo_ips_padrao()

def carregar_ips():
    garantir_pastas()
    if not os.path.exists(ARQUIVO_IPS):
        # Criar arquivo padrão com 4 strings vazias
        with open(ARQUIVO_IPS, "w") as f:
            json.dump(["", "", "", ""], f, indent=4)
        return ["", "", "", ""]

    with open(ARQUIVO_IPS, "r") as f:
        try:
            ips = json.load(f)
            if not isinstance(ips, list):
                return ["", "", "", ""]
            return ips
        except json.JSONDecodeError:
            return ["", "", "", ""]


@app.route('/')
def index():
    ips = carregar_ips()
    while len(ips) < 4:
        ips.append("")
    return render_template('index.html', ip1=ips[0], ip2=ips[1], ip3=ips[2], ip4=ips[3])

@app.route("/executar")
def executar():
    global executando
    executando = True

    garantir_pastas()

    ips = carregar_ips()

    # Montar URLs das câmeras
    urls_ala = []
    for idx, ip in enumerate(ips, start=1):
        urls_ala.append((f"Ala {idx}", f"http://{ip}:8080/shot.jpg"))

    if len(urls_ala) == 0:
        return "Nenhum IP configurado. Por favor, configure os IPs no arquivo ips.json em execucao/enderecos_ips."

    modelo = load_model("modelo_seguranca_epi.keras")

    # Limpar pastas
    for pasta in [PASTA_TEMP, PASTA_CORRETA, PASTA_ERRADA]:
        for arquivo in os.listdir(pasta):
            caminho_arquivo = os.path.join(pasta, arquivo)
            os.remove(caminho_arquivo)

    def obter_imagem(caminho):
        img = image.load_img(caminho, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        img_cv = cv2.cvtColor(x[0], cv2.COLOR_RGB2BGR)
        imagem_tratada = cv2.resize(img_cv, (224, 224), interpolation=cv2.INTER_CUBIC)
        imagem_tratada = cv2.GaussianBlur(imagem_tratada, (5, 5), 0)
        imagem_tratada = cv2.convertScaleAbs(imagem_tratada, alpha=1.5, beta=50)
        imagem_cinza = cv2.cvtColor(imagem_tratada, cv2.COLOR_BGR2GRAY)
        imagem_equalizada = cv2.equalizeHist(imagem_cinza)
        imagem_tratada = cv2.cvtColor(imagem_equalizada, cv2.COLOR_GRAY2BGR)
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        imagem_tratada = cv2.filter2D(imagem_tratada, -1, kernel)

        x_tratada = np.expand_dims(imagem_tratada, axis=0)
        x_tratada = preprocess_input(x_tratada)

        return img, x_tratada

    def detectar_pessoa(caminho_imagem):
        model = torch.hub.load('yolov5', 'custom', path='yolov5s.pt', source='local')
        img = cv2.imread(caminho_imagem)
        results = model(img)
        results_df = results.pandas().xyxy[0]
        return any(results_df['name'] == 'person')

    def processar_ala(ala, url_ala):
        while executando:
            try:
                cap = cv2.VideoCapture(url_ala)
                ret, frame = cap.read()
                if not ret:
                    break

                data = datetime.now()
                data_str = data.strftime("Data - %d-%m-%Y Hora - %H-%M-%S")
                caminho_imagem = f"{PASTA_TEMP}/{ala} - {data_str}.jpg"
                cv2.imwrite(caminho_imagem, frame)

                pessoa_na_imagem = detectar_pessoa(caminho_imagem)

                if pessoa_na_imagem:
                    img, x = obter_imagem(caminho_imagem)
                    probabilidade = modelo.predict(x)[0]

                    prob_correto = probabilidade[0] * 100
                    prob_errado = probabilidade[1] * 100

                    print(f"{ala} - Probabilidade correto: {prob_correto:.2f}%")
                    print(f"{ala} - Probabilidade errado: {prob_errado:.2f}%")

                    if prob_errado > prob_correto:
                        shutil.move(caminho_imagem, f"{PASTA_ERRADA}/{ala} - {data_str}.jpg")
                    else:
                        os.remove(caminho_imagem)
                else:
                    os.remove(caminho_imagem)

            except Exception as erro:
                print(f"Erro na {ala}: {erro}")

            finally:
                cap.release()
                cv2.destroyAllWindows()

    threads = []
    for ala, url in urls_ala:
        t = threading.Thread(target=processar_ala, args=(ala, url))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    return redirect(url_for('index'))


@app.route("/ultimas_ocorrencias")
def ultimas_ocorrencias():
    image_folder = PASTA_ERRADA
    images = os.listdir(image_folder)

    formatted_images = [
        {
            'path': url_for('get_image', filename=image),
            'name': image.rsplit('/', 1)[-1].rsplit('.', 1)[0].replace('-', ' - ')
        } for image in images if image.lower().endswith(('png', 'jpg', 'jpeg'))
    ]

    return render_template("ultimas_ocorrencias.html", images=formatted_images)


@app.route("/sistema_fechado")
def sistema_fechado():
    global executando
    executando = False
    return render_template("sistema_fechado.html")


@app.route("/retornar")
def retornar():
    ips = carregar_ips()
    while len(ips) < 4:
        ips.append("")
    return render_template('index.html', ip1=ips[0], ip2=ips[1], ip3=ips[2], ip4=ips[3])

@app.route("/atualizar")
def atualizar():
    return redirect(url_for('ultimas_ocorrencias'))


@app.route('/get_image/<path:filename>')
def get_image(filename):
    return send_from_directory(PASTA_ERRADA, filename)

if __name__ == '__main__':
    garantir_pastas()
    app.run(debug=True)