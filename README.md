# 📧 AutoU Case — Classificador de Emails

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Gradio-orange.svg)
![OpenAI](https://img.shields.io/badge/API-OpenAI-green.svg)
![Status](https://img.shields.io/badge/Status-Online-success.svg)

Este é o projeto desenvolvido para o **Case Técnico da AutoU** 🚀.
O objetivo é **automatizar a leitura de emails**, classificando-os como **Produtivos** ou **Improdutivos**, e **sugerir uma resposta automática** para cada caso.

---

## 🌐 Demonstração online

🔗 [Clique aqui para acessar a aplicação](https://huggingface.co/spaces/jpabdu/email-classifier)

> A aplicação está hospedada e pronta para uso online, **sem necessidade de instalação local**.

---

## 🚀 Tecnologias usadas

* [Python 3.10+](https://www.python.org/)
* [Gradio](https://gradio.app/) → Interface web interativa
* [OpenAI GPT](https://platform.openai.com/) → Classificação e geração de resposta
* [pdfplumber](https://github.com/jsvine/pdfplumber) → Leitura de PDFs
* [nltk](https://www.nltk.org/) → Stopwords em português

---

## 🖥️ Funcionalidades

* Upload de arquivos **.txt** e **.pdf**
* Inserção direta de texto do email na interface
* Classificação automática em:

  * **Produtivo** → requer ação
  * **Improdutivo** → não requer ação
* Geração de **resposta automática contextual**
* Interface **intuitiva e simples** para o usuário final

---

## 🔧 Como rodar localmente

1. Clone este repositório:

   ```bash
   git clone https://github.com/jp-abdu/email-classifier.git
   cd email-classifier
   ```
2. Crie um ambiente virtual e instale dependências:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   pip install -r requirements.txt
   ```
3. Configure sua chave da OpenAI:

   ```bash
   env$:OPENAI_API_KEY "sua-chave"     # Windows
   export OPENAI_API_KEY="sua-chave"  # Linux/Mac
   ```
4. Rode a aplicação:

   ```bash
   python app.py
   ```

   Acesse no navegador: [http://127.0.0.1:7860](http://127.0.0.1:7860)

---

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
```

---

## 🧠 Explicação Técnica (Resumo)

* O backend em Python realiza:

  * **Leitura e pré-processamento** do texto (remoção de stopwords, tokenização)
  * **Classificação** do email como Produtivo ou Improdutivo usando **OpenAI GPT**
  * **Geração de resposta automática** contextualizada ao conteúdo do email
* A integração com Gradio permite envio de arquivos ou texto diretamente e exibe os resultados na interface.

---

## 🎥 Vídeo Demonstrativo

🔗 [Clique aqui para assistir ao vídeo](link-do-video)

> O vídeo apresenta:
>
> * Introdução pessoal e descrição do desafio
> * Demonstração do upload e classificação de emails
> * Explicação técnica do algoritmo e das decisões de implementação
> * Conclusão e aprendizados

---

## 📌 Objetivo do Desafio Simplificado

Desenvolver uma aplicação web simples que utilize inteligência artificial para:

1. **Classificar** emails em categorias predefinidas.
2. **Sugerir respostas automáticas** baseadas na classificação realizada.

**Categorias de Classificação**:

* **Produtivo:** Emails que requerem uma ação ou resposta específica.
* **Improdutivo:** Emails que não necessitam de ação imediata.

---

## ✅ Requisitos Atendidos

1. **Interface Web**

   * Upload de arquivos (.txt, .pdf) e inserção de texto manual
   * Exibição da categoria e resposta sugerida
   * Interface simples e intuitiva

2. **Backend em Python**

   * Leitura, pré-processamento e classificação de emails
   * Geração de respostas automáticas
   * Integração com a interface

3. **Hospedagem na Nuvem**

   * Aplicação hospedada no Hugging Face Spaces
   * Link online funcional fornecido

4. **Documentação e Entregáveis**

   * Código-fonte no GitHub com README detalhado
   * Exemplos de emails incluídos
   * Vídeo demonstrativo com link
