import logging

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from agent import responder
from schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Minha Primeira API"
)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def pagina_inicial() -> str:
    return """
    <h1>API em execução</h1>
    <p>FIAP - Let's rock the future!</p>
    """

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = responder(
            message=request.message,
            conversation_id=request.conversation_id,
        )
    except Exception as error:
        logger.exception("Falha ao processar a mensagem.")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível processar a mensagem.",
        ) from error

    return ChatResponse(
        conversation_id=request.conversation_id,
        response=response,
    )


