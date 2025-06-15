# 🛡️ Sistema de Monitoramento Inteligente de EPIs em Ambiente Fabril  
### 🔍 Flask | YOLOv5 | Keras | OpenCV | PyTorch

![Ilustração do projeto](ilustracao.png)

Este projeto tem como objetivo **monitorar, em tempo real, o uso correto de Equipamentos de Proteção Individual (EPIs) no ambiente fabril**. Utilizando redes neurais convolucionais (CNN), detecção de pessoas com YOLOv5 e classificação com Keras, o sistema captura imagens de câmeras IP, detecta pessoas, classifica se estão utilizando os EPIs corretamente e registra as ocorrências para posterior análise.

---

## 📷 Funcionalidades

- 🎥 Captura de imagens de múltiplas câmeras IP (três alas diferentes).  
- 🧠 Detecção de pessoas nas imagens utilizando YOLOv5 (via PyTorch).  
- ✅ Classificação (uso correto ou incorreto de EPI) com modelos treinados em Keras.  
- 🖼️ Processamento de imagem com OpenCV para melhoria da qualidade.  
- 🌐 Interface web com Flask para:  
  - Iniciar monitoramento  
  - Visualizar ocorrências recentes  
  - Encerrar sistema  

---

## 🧠 Tecnologias Utilizadas

- Python 3.10  
- Flask  
- OpenCV  
- Keras  
- TensorFlow (backend do Keras)  
- PyTorch (YOLOv5)  
- YOLOv5  
- NumPy  
- Pillow  
- Threading  
- Jupyter Notebook  

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

Com `requirements.txt`:

```bash
pip install -r requirements.txt
```

Ou diretamente:

```bash
pip install flask opencv-python numpy keras tensorflow torch pillow jupyter matplotlib scikit-learn pandas
```

---

## 📁 Estrutura do Projeto

```plaintext
projeto/
│
├── execucao/
│   ├── corretas/           # Imagens classificadas como uso correto de EPI
│   ├── erradas/            # Imagens classificadas como uso incorreto de EPI
│   └── temp/               # Imagens temporárias da execução
│
├── modelo_seguranca_epi.keras        # Modelo treinado para classificação de EPI
├── modelo_seguranca_epi.ipynb        # Notebook de treinamento do modelo
│
├── templates/
│   ├── index.html                    # Página inicial
│   ├── sistema_fechado.html          # Página após encerrar o sistema
│   └── ultimas_ocorrencias.html      # Página de ocorrências recentes
│
├── app.py                            # Aplicação principal em Flask
└── README.md                          # Documentação do projeto
```

---

## 🔬 Notebook de Treinamento do Modelo

O projeto inclui um notebook Jupyter (`modelo_seguranca_epi.ipynb`) utilizado para o **treinamento do modelo de classificação do uso de EPIs**.

### 📚 Funcionalidades do notebook:

- Pré-processamento das imagens.  
- Criação dos datasets de treino e validação.  
- Definição da arquitetura CNN (transfer learning).  
- Treinamento e validação do modelo.  
- Exportação do modelo treinado no formato `.keras` para ser usado na aplicação.  

### ▶️ Como executar o notebook:

1. Instale as dependências (se ainda não tiver):  

```bash
pip install tensorflow matplotlib scikit-learn pandas jupyter
```

2. Execute o Jupyter Notebook:  

```bash
jupyter notebook
```

3. Abra o arquivo `modelo_seguranca_epi.ipynb`.  
4. Execute as células sequencialmente para treinar e exportar seu modelo.  

---

## 🚀 Como Executar a Aplicação

Execute o arquivo principal do Flask:  

```bash
python app.py
```

Acesse no navegador:  
📍 http://127.0.0.1:5000

---

## ⚙️ Configuração Inicial

Configure os IPs das câmeras dentro do arquivo `app.py`:  

```python
endereco_ip_1 = "xxx.xxx.xxx.xxx"
endereco_ip_2 = "xxx.xxx.xxx.xxx"
endereco_ip_3 = "xxx.xxx.xxx.xxx"
```

Ou, preferencialmente, configure utilizando um arquivo `.env`.  

Certifique-se de que o modelo `modelo_seguranca_epi.keras` está treinado e salvo na raiz do projeto.  

As pastas `execucao/corretas`, `execucao/erradas` e `execucao/temp` devem estar criadas previamente.  

---

## 📷 Utilização com celular como câmera IP

Você pode utilizar seu celular Android como câmera IP para testes utilizando o aplicativo **IP Webcam**.  
Configure o IP e porta do aplicativo no código para que o sistema Flask capture as imagens.  

---

## 🖼️ Interface Web

- **Página inicial:** iniciar monitoramento.  
- **Últimas ocorrências:** exibe imagens classificadas como uso incorreto.  
- **Encerrar sistema:** finaliza todas as threads de captura e inferência.  

---

## 📄 Licença

Este projeto está licenciado sob os termos da **MIT License**.  

---

## 👥 Equipe de Desenvolvimento

- **Ray Labres** - [GitHub](https://github.com/raylabres)  
- **Elifelete Cavalcante**  
- **Gabriel Gardenal**  

Desenvolvido como parte do projeto acadêmico para o **Centro Universitário Nossa Senhora do Patrocínio – CEUNSP** (Ago – Nov/2024).  
