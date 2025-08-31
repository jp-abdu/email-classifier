# 📧 AutoU Case — Classificador de Emails

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Gradio-orange.svg)
![OpenAI](https://img.shields.io/badge/API-OpenAI-green.svg)
![Status](https://img.shields.io/badge/Status-Online-success.svg)

Este é meu projeto desenvolvido para o **Case Técnico da AutoU** 🚀.  
O objetivo é **automatizar a leitura de emails**, classificando-os como **Produtivos** ou **Improdutivos**, e **sugerir uma resposta automática** para cada caso.  

---

## 🌐 Demonstração online
🔗 [Clique aqui para acessar a aplicação](https://huggingface.co/spaces/jpabdu/email-classifier)  

---

## 🚀 Tecnologias usadas
- [Python 3.10+](https://www.python.org/)
- [Gradio](https://gradio.app/) → Interface web interativa
- [OpenAI GPT](https://platform.openai.com/) → Classificação e geração de resposta
- [pdfplumber](https://github.com/jsvine/pdfplumber) → Leitura de PDFs
- [nltk](https://www.nltk.org/) → Stopwords em português

---

## 🖥️ Funcionalidades
- Upload de arquivos **.txt** e **.pdf**  
- Classificação automática em:  
  - **Produtivo** → requer ação  
  - **Improdutivo** → não requer ação  
- Geração de **resposta automática** contextual  
- Interface intuitiva e simples para o usuário final  

---

## 🔧 Como rodar localmente

1. Clone este repositório:
   ```bash
   git clone https://github.com/jp-abdu/email-classifier.git
   cd email-classifier
2. Crie um ambiente virtual e instale dependências:
    ```bash 
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows
    pip install -r requirements.txt
3. Configure sua chave da OpenAI:
    ```bash
    env$:OPENAI_API_KEY "sua-chave"     # Windows
4. Rode a aplicação:
    ```bash
    python app.py
    Acesse no navegador: http://127.0.0.1:7860

## 📂 Estrutura do Projeto
  ```bash
  email-classifier/
  │── app.py              # aplicação principal (Gradio + OpenAI)
  │── requirements.txt    # dependências
  │── README.md           # documentação
  │── samples/            # exemplos de emails
  │     ├── produtivo1.txt
  │     ├── produtivo2.txt
  │     ├── improdutivo1.txt
  │     └── improdutivo2.txt
