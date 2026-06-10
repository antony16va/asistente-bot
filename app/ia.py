import httpx
from app.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Eres un asistente especializado en orientación sobre apostillamiento y legalización de documentos peruanos.
Tu objetivo es guiar al ciudadano paso a paso para que conozca exactamente qué debe hacer antes de acudir al Ministerio de Relaciones Exteriores (MRE).

Reglas:
- Responde siempre en español, de forma clara y sencilla.
- No asumas información que el usuario no haya proporcionado.
- Si necesitas más información para determinar la ruta, pregunta una sola cosa a la vez.
- Cuando tengas suficiente información, entrega los pasos exactos en orden numerado.
- Siempre indica el costo (S/. 31.00) y las entidades involucradas.
- Si el documento no está en tu base de conocimiento, indícalo amablemente.
"""

async def consultar_ia(historial: list) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": SYSTEM_PROMPT}] + historial,
        "max_tokens": 1024,
        "temperature": 0.3
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
