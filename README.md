# 🛡️ Monitoramento Inteligente Fabril de EPIs com Flask, YOLOv5 e Keras

![Ilustração do projeto](ilustracao.png)

Este projeto é uma aplicação web desenvolvida com Flask que realiza **monitoramento em tempo real** do uso correto de Equipamentos de Proteção Individual (EPIs) por meio de **redes neurais convolucionais (CNN)** e **detecção de pessoas com YOLOv5**. A solução recebe imagens de múltiplas câmeras IP, realiza inferência com modelos treinados e armazena os resultados para posterior análise.

---

## 📷 Funcionalidades

- Captura de imagens de câmeras IP em tempo real (3 alas diferentes).  
- Detecção de pessoas nas imagens com YOLOv5 (via PyTorch).  
- Classificação da imagem (uso correto ou incorreto de EPI) com Keras.  
- Processamento de imagem com OpenCV para melhoria da qualidade.  
- Interface web com Flask para:  
  - Iniciar monitoramento  
  - Visualizar ocorrências mais recentes  
  - Encerrar sistema  

---

## 🧠 Tecnologias Utilizadas

- Python 3.10  
- Flask  
- OpenCV  
- Keras  
- TensorFlow (backend do Keras)  
- PyTorch  
- YOLOv5  
- NumPy  
- Threading  

---

## 🛠️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install flask opencv-python numpy keras torch pillow
```

---

## 📁 Estrutura do Projeto

```
projeto/
│
├── execucao/
│   ├── corretas/
│   ├── erradas/
│   └── temp/
│
├── modelo_seguranca_epi.keras
├── templates/
│   ├── index.html
│   ├── sistema_fechado.html
│   └── ultimas_ocorrencias.html
│
├── app.py
└── README.md
```

---

## 🚀 Como Executar

Execute o arquivo principal do Flask:

```bash
python app.py
```

Acesse no navegador:  
📍 http://127.0.0.1:5000

---

## ⚙️ Configuração Inicial

Defina os IPs das câmeras nos campos:

```python
endereco_ip_1 = "xxx.xxx.xxx.xxx"
endereco_ip_2 = "xxx.xxx.xxx.xxx"
endereco_ip_3 = "xxx.xxx.xxx.xxx"
```

Certifique-se de que o modelo `modelo_seguranca_epi.keras` está treinado e salvo na raiz do projeto.

As pastas `execucao/corretas`, `execucao/erradas` e `execucao/temp` devem estar criadas previamente.

---

## 📷 Utilização com celular como câmera IP

Para facilitar o uso e prototipagem, você pode transformar seu celular Android em uma câmera IP usando o aplicativo **IP Webcam**. O app transmite vídeo pela rede Wi-Fi, permitindo que a aplicação Flask capture as imagens pelo IP e porta configurados no app.

---

## 🧪 Modelo de Classificação

O modelo `modelo_seguranca_epi.keras` deve ser treinado previamente com imagens rotuladas como:

- Classe 0 – Uso correto de EPI  
- Classe 1 – Uso incorreto de EPI  

---

## 🖼️ Interface Web

- Página inicial: iniciar monitoramento  
- Últimas ocorrências: exibe imagens classificadas como uso incorreto  
- Encerrar sistema: finaliza todas as threads de captura e inferência  

---

## 📄 Licença

Este projeto está licenciado sob os termos da **MIT License**.

---

## 👨‍💻 Autor

**Ray Labres**  
Monitoramento Fabril Inteligente (Ago – Nov/2024)  
Centro Universitário Nossa Senhora do Patrocínio – CEUNSP  
Equipe: Ray Labres, Elifelete Cavalcante, Gabriel Gardenal  
GitHub: https://github.com/raylabres
