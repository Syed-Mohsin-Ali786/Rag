from openai import OpenAI
from app.config import settings

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.openrouter_api_key,
)

def generate_answer(query: str, context_chunks: list[str]) -> str:
    context = "\n\n---\n\n".join(context_chunks)
    prompt = f"""Answer the question using ONLY the context below. 
If the answer isn't in the context, say you don't know.

Context:
{context}

Question: {query}

Answer:"""

    response = client.chat.completions.create(
        model=settings.chat_model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content