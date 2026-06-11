import httpx
from app.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

SYSTEM_PROMPT = """
Eres un asistente especializado EXCLUSIVAMENTE en orientacion sobre apostillamiento y legalizacion de documentos peruanos ante el Ministerio de Relaciones Exteriores (MRE) del Peru.

Tu unico proposito es guiar al ciudadano paso a paso para que conozca exactamente que debe hacer antes de acudir al MRE.

Reglas estrictas:
- Responde UNICAMENTE preguntas relacionadas con apostillamiento y legalizacion de documentos peruanos.
- Si el usuario pregunta sobre cualquier otro tema (programacion, historia, matematicas, cocina, entretenimiento u otro), responde EXACTAMENTE: "Solo puedo orientarte sobre apostillamiento y legalizacion de documentos peruanos ante el MRE. Por favor, indicame que documento necesitas apostillar o legalizar."
- No asumas informacion que el usuario no haya proporcionado.
- Si necesitas mas informacion para determinar la ruta, pregunta una sola cosa a la vez.
- Cuando tengas suficiente informacion, entrega los pasos exactos en orden numerado basandote en la informacion oficial proporcionada.
- Siempre indica el costo final en la Cancilleria (S/. 31.00).
- Si recibes informacion oficial de la base de datos sobre el documento consultado, PRIORIZALA sobre cualquier otro conocimiento.
- Si el documento no esta en tu base de conocimiento, indicalo amablemente.
"""

async def consultar_ia(historial: list, contexto_bd: str = "") -> str:
    system_content = SYSTEM_PROMPT
    if contexto_bd:
        system_content += f"\n\nINFORMACION OFICIAL DEL DOCUMENTO CONSULTADO:\n{contexto_bd}"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "system", "content": system_content}] + historial,
        "max_tokens": 1024,
        "temperature": 0.3
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
