import os
import requests
import json
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializar o Flask
app = Flask(__name__, static_folder='../frontend')

# Obter a chave da API do arquivo .env
api_key = os.getenv("GEMINI_API_KEY")

# URL da API do Gemini
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# Cabeçalhos para a requisição
headers = {
    "Content-Type": "application/json",
    "X-goog-api-key": api_key
}

def enviar_prompt_para_gemini(prompt):
    """Função para enviar um prompt para a API do Gemini e obter resposta"""
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    
    # Fazer a requisição para a API
    response = requests.post(url, headers=headers, json=payload)
    
    # Processar a resposta
    if response.status_code == 200:
        dados = response.json()
        if "candidates" in dados and len(dados["candidates"]) > 0:
            texto_resposta = dados["candidates"][0]["content"]["parts"][0]["text"]
            return texto_resposta
        else:
            return "Não foi possível obter uma resposta."
    else:
        return f"Erro na API: {response.status_code} - {response.text}"

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/prompt', methods=['POST'])
def handle_prompt():
    dados = request.get_json()
    prompt_usuario = dados.get("prompt")
    if not prompt_usuario:
        return jsonify({"erro": "Nenhum prompt fornecido"}), 400
    
    resposta = enviar_prompt_para_gemini(prompt_usuario)
    return jsonify({"resposta": resposta})

# Exemplo de uso
if __name__ == "__main__":
    app.run(debug=True, port=5000)