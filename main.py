import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List

# --- CORREÇÃO AQUI: Importação direta e robusta ---
import google.generativeai as genai
# A importação de 'types' não é mais necessária separadamente, pois
# acessaremos via 'genai.types'.

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração do Cliente Gemini ---
try:
    # A configuração agora é feita diretamente no objeto 'genai'
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
except KeyError:
    raise RuntimeError("GEMINI_API_KEY não encontrada nas variáveis de ambiente.")

# --- Configuração da API FastAPI ---
app = FastAPI(
    title="Gemini Chat API",
    description="Uma API para interagir com o Google Gemini Pro em modo de chat com streaming.",
    version="1.0.0",
)

# --- Modelos Pydantic (sem alterações aqui) ---
class Message(BaseModel):
    role: str = Field(..., description="O papel do autor da mensagem (ex: 'user' ou 'model').")
    text: str = Field(..., description="O conteúdo da mensagem.")

class ChatRequest(BaseModel):
    prompt: str = Field(..., description="A nova pergunta/prompt do usuário.")
    history: List[Message] = Field([], description="O histórico da conversa para manter o contexto.")
    model: str = Field("gemini-1.5-pro-latest", description="O modelo Gemini a ser usado.")

# --- Segurança: Dependência para validar a X-API-Key (sem alterações aqui) ---
async def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    expected_api_key = os.environ.get("APP_API_KEY")
    if not expected_api_key or x_api_key != expected_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="X-API-Key inválida ou ausente.",
        )

# --- Endpoint da API ---
@app.post(
    "/chat/stream",
    dependencies=[Depends(verify_api_key)],
    summary="Inicia uma conversa com o Gemini com resposta em streaming",
    tags=["Chat"]
)
async def generate_chat_stream(request: ChatRequest):
    try:
        # Constrói o histórico no formato que o Gemini espera
        contents = []
        for message in request.history:
            # --- CORREÇÃO AQUI: Usar genai.types ---
            contents.append({'role': message.role, 'parts': [message.text]})
        
        # Adiciona o novo prompt do usuário
        contents.append({'role': 'user', 'parts': [request.prompt]})

        # Configurações de geração
        # --- CORREÇÃO AQUI: Usar genai.types ---
        generation_config = genai.types.GenerationConfig(
            temperature=0.7,
        )
        
        # Inicializa o modelo
        model = genai.GenerativeModel(model_name=request.model)

        async def stream_generator():
            # `generate_content` com stream=True retorna um gerador
            stream = model.generate_content(
                contents=contents,
                generation_config=generation_config,
                stream=True,
            )
            for chunk in stream:
                if chunk.text:
                    yield chunk.text

        # Retorna a resposta como um fluxo de texto
        return StreamingResponse(stream_generator(), media_type="text/plain")

    except Exception as e:
        # Adiciona mais detalhes ao log de erro para facilitar a depuração
        print(f"Ocorreu um erro: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao interagir com a API Gemini: {str(e)}")

# --- Ponto de entrada para rodar com Uvicorn ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)