from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver

from config import MODEL_NAME

SYSTEM_PROMPT = (
    "Você é um assistente de uma plataforma de cursos. "
    "Ajude a pessoa a organizar os estudos usando apenas "
    "as informações fornecidas na conversa. "
    "Se faltar um dado necessário, pergunte."
)

model = init_chat_model(MODEL_NAME)
checkpointer = InMemorySaver()

agent = create_agent(
    model=model,
    tools=[],
    system_prompt=SYSTEM_PROMPT,
    checkpointer=checkpointer,
)

def responder(message: str, conversation_id: str) -> str:
    result = agent.invoke(
        {
            "messages": [
                {"role": "user", "content": message}
            ]
        },
        config={
            "configurable": {
                "thread_id": conversation_id
            }
        },
    )
    return result["messages"][-1].text
