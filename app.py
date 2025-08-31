# Esse é meu projeto do case AutoU :)
# Aqui eu construí uma aplicação web usando Gradio + OpenAI
# O objetivo é classificar emails como Produtivo ou Improdutivo e sugerir automaticamente uma resposta para cada um.

import os, io, re, pdfplumber
import gradio as gr
import nltk
from nltk.corpus import stopwords
from openai import OpenAI

# Baixo stopwords automaticamente (para não quebrar no deploy)
nltk.download('stopwords', quiet=True)

# Carrego a chave da API
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

if not OPENAI_KEY:
    raise ValueError("⚠️ Variável de ambiente OPENAI_API_KEY não encontrada!")

print("DEBUG: Chave OpenAI carregada, começa com:", OPENAI_KEY[:5])

# Cliente OpenAI
client = OpenAI(api_key=OPENAI_KEY)

# Stopwords em português
PT_STOPWORDS = set(stopwords.words('portuguese'))

# Função para extrair texto de arquivos .pdf ou .txt
def extract_text_from_file(file_obj):
    # Se for objeto Gradio, pode ser NamedString, tempfile, ou string
    # Tenta extrair nome e conteúdo corretamente
    if hasattr(file_obj, "name") and hasattr(file_obj, "read"):
        name = file_obj.name
        data = file_obj.read()
    elif hasattr(file_obj, "name") and hasattr(file_obj, "value"):
        name = file_obj.name
        data = file_obj.value
    elif isinstance(file_obj, str):
        name = file_obj
        # Tenta abrir e ler o arquivo
        try:
            with open(file_obj, "rb") as f:
                data = f.read()
        except Exception:
            data = file_obj.encode('utf-8')
    else:
        name = "uploaded.txt"
        data = file_obj

    # Garante que o nome do arquivo seja uma string
    if not isinstance(name, str):
        name = str(name)

    if name.lower().endswith('.pdf'):
        try:
            with pdfplumber.open(io.BytesIO(data)) as pdf:
                pages = [p.extract_text() or "" for p in pdf.pages]
                return "\n".join(pages)
        except Exception as e:
            print(f"Erro ao processar PDF: {e}")
            # Tenta tratar como texto simples se falhar como PDF
            if isinstance(data, bytes):
                return data.decode('utf-8', errors='ignore')
            return str(data)
    else:
        # Tentativa de decodificação com várias codificações comuns
        if isinstance(data, bytes):
            for encoding in ['utf-8', 'latin1', 'cp1252']:
                try:
                    return data.decode(encoding)
                except UnicodeDecodeError:
                    continue
            # Se todas falharem, usa ignore para garantir algum resultado
            return data.decode('utf-8', errors='ignore')
        return str(data)

# Limpeza básica de texto
def simple_clean(text):
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Classificação do email (Produtivo / Improdutivo)
def classify_with_openai(text):
    prompt = (
        "Você é um classificador de emails.\n"
        "Classifique o email abaixo em UMA DAS DUAS etiquetas: 'Produtivo' ou 'Improdutivo'.\n"
        "Responda APENAS com a palavra 'Produtivo' ou 'Improdutivo', sem nenhuma explicação adicional.\n"
        "\n"
        "Emails PRODUTIVOS são emails que tratam de solicitação, dúvida, pedido, problema, suporte, relatório, atualização, encaminhamento, agendamento, informação técnica.\n"
        "Emails IMPRODUTIVOS são emails que tratam de felicitações, agradecimentos, mensagens de parabéns, cumprimentos, elogios, mensagens motivacionais, comunicados sem ação, respostas de encerramento, mensagens de boas festas, aniversários, celebrações.\n"
        "\n"
        "Exemplo 1:\nEmail: 'Olá, preciso do status do ticket #123, o sistema deu erro ao salvar.'\nResposta: Produtivo\n"
        "Exemplo 2:\nEmail: 'Feliz Natal! Desejo ótimas festas a todos.'\nResposta: Improdutivo\n"
        "Exemplo 3:\nEmail: 'Agradeço pelo suporte, tudo resolvido.'\nResposta: Improdutivo\n"
        "Exemplo 4:\nEmail: 'Favor enviar o relatório da semana.'\nResposta: Produtivo\n"
        "Exemplo 5:\nEmail: 'Feliz aniversário para toda a equipe, desejo muito sucesso!'\nResposta: Improdutivo\n"
        "Exemplo 6:\nEmail: 'Bom dia, gostaria de agendar uma reunião para discutir o projeto.'\nResposta: Produtivo\n"
        "Exemplo 7:\nEmail: 'Parabéns pelo excelente trabalho realizado.'\nResposta: Improdutivo\n"
        "Exemplo 8:\nEmail: 'O sistema está apresentando lentidão, podem verificar?'\nResposta: Produtivo\n"
        "Exemplo 9:\nEmail: 'Obrigado pela atenção.'\nResposta: Improdutivo\n"
        "Com esses exemplos em mente:\n"
        f"Agora classifique:\nEmail: '''{text}'''\nResposta:"
    )
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=50,
        temperature=0.0
    )
    response_content = resp.choices[0].message.content.strip()
    
    # Procura especificamente pelas palavras "Produtivo" ou "Improdutivo" em qualquer lugar da resposta
    if "produtivo" in response_content.lower() and "improdutivo" not in response_content.lower():
        return "Produtivo"
    elif "improdutivo" in response_content.lower():
        return "Improdutivo"
    
    # Se não encontrar uma classificação clara, analisa o conteúdo do email para fazer uma decisão mais informada baseada nas categorias definidas
    produtivo_keywords = ["solicitação", "dúvida", "pedido", "problema", "suporte", 
                          "relatório", "atualização", "encaminh", "agend", "informação",
                          "erro", "sistema", "acesso", "urgente", "preciso", "verificar"]
    
    improdutivo_keywords = ["felicitações", "agradec", "parabéns", "obrigado", "elogio", 
                           "motivacional", "boas festas", "aniversário", "celebração"]
    
    text_lower = text.lower()
    
    # Conta ocorrências de palavras-chave
    produtivo_count = sum(1 for word in produtivo_keywords if word in text_lower)
    improdutivo_count = sum(1 for word in improdutivo_keywords if word in text_lower)
    
    # Decide com base na contagem de palavras-chave
    if produtivo_count > improdutivo_count:
        return "Produtivo"
    else:
        return "Improdutivo"

# Geração da resposta automática
def generate_suggested_reply(text, category):
    if category == "Produtivo":
        system = "Você é um assistente que sugere respostas formais e objetivas para e-mails de trabalho."
        user_prompt = (
            f"O seguinte email foi recebido:\n\n{text}\n\n"
            "Gere uma resposta breve (2-4 frases) propondo próximos passos, pedindo informações se necessário, "
            "e encerrando cordialmente com apenas 'Atenciosamente.' no final. "
            "NÃO INCLUA campos como '[Seu Nome]', '[Seu Cargo]' ou '[Seu Contato]' na resposta."
        )
    else:
        system = "Você é um assistente que sugere respostas curtas e educadas para e-mails não urgentes."
        user_prompt = (
            f"O seguinte email foi recebido:\n\n{text}\n\n"
            "Gere uma resposta cordial e curta (1-2 frases) agradecendo ou reconhecendo, sem abrir ticket. "
            "Termine apenas com 'Atenciosamente.'. "
            "NÃO INCLUA campos como '[Seu Nome]', '[Seu Cargo]' ou '[Seu Contato]' na resposta."
        )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":system},{"role":"user","content":user_prompt}],
        max_tokens=200,
        temperature=0.6
    )
    # Remove qualquer linha que contenha [Seu Nome], [Seu Cargo], ou [Seu Contato]
    content = resp.choices[0].message.content.strip()
    filtered_lines = [line for line in content.splitlines() 
                     if "[Seu Nome]" not in line and "[Seu Cargo]" not in line and "[Seu Contato]" not in line]
    return "\n".join(filtered_lines)

# Função principal de processamento
def process(email_text, uploaded_file):
    try:
        if uploaded_file is not None:
            raw = extract_text_from_file(uploaded_file)
            print(f"DEBUG: Arquivo processado, primeiros 100 caracteres: {raw[:100]}")
        else:
            raw = email_text or ""
        
        text = simple_clean(raw)
        
        if not text or len(text.strip()) < 2:
            return ("", "", "Erro: email vazio ou inválido")
        
        # Registra o texto que será enviado para classificação
        print(f"DEBUG: Texto para classificação [{len(text)} caracteres]: {text[:200]}...")
        
        # Realiza a classificação
        category = classify_with_openai(text)
        print(f"DEBUG: Categoria classificada: {category}")
        
        # Gera resposta sugerida
        suggested = generate_suggested_reply(text, category)
        
        # Exibe um preview do email para confirmar o texto foi processado corretamente
        preview = text[:300]+"..." if len(text)>300 else text
        
        return (category, suggested, preview)
    except Exception as e:
        print(f"ERRO no processamento: {str(e)}")
        return ("Erro", f"Ocorreu um erro durante o processamento: {str(e)}", "Falha no processamento do email")

# Interface Gradio
with gr.Blocks() as demo:
    gr.Markdown("# Classificador de Emails")
    gr.Markdown("Suba um email (.txt/.pdf) ou cole o texto abaixo para ver a classificação e a resposta sugerida.")
    with gr.Row():
        with gr.Column(scale=2):
            txt = gr.Textbox(label="Cole o texto do email", lines=12)
            file = gr.File(label="Ou faça upload do arquivo (.txt / .pdf)")
            btn = gr.Button("Processar Email")
        with gr.Column(scale=1):
            out_cat = gr.Label(label="Categoria")
            out_reply = gr.Textbox(label="Resposta sugerida", lines=6)
            out_excerpt = gr.Textbox(label="Preview do email")
    btn.click(fn=process, inputs=[txt, file], outputs=[out_cat, out_reply, out_excerpt])

# Execução local
if __name__ == "__main__":
    demo.launch()
