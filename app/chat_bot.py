import httpx
from app.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

RESPUESTA_FUERA_DOMINIO = (
    "Solo puedo orientarte sobre apostillamiento y "
    "legalización de documentos peruanos ante el MRE. "
    "Por favor, indícame qué documento necesitas apostillar o legalizar."
)

PALABRAS_CLAVE = [
    "apostilla",
    "apostillar",
    "apostillado",
    "legalizacion",
    "legalización",
    "documento",
    "certificacion",
    "certificación",
    "cancilleria",
    "cancillería",
    "mre",
    "titulo",
    "bachiller",
    "sunedu",
    "partida",
    "reniec",
    "nacimiento",
    "matrimonio",
    "defuncion",
    "antecedente",
    "penal",
    "judicial",
    "policial",
    "notarial",
    "poder",
    "constancia",
    "trabajo",
    "certificado",
    "diploma",
    "universidad"
]

def es_consulta_valida(texto: str) -> bool:
    texto = texto.lower()
    return any(p in texto for p in PALABRAS_CLAVE)

SYSTEM_PROMPT = """
Eres un orientador digital especializado en Apostilla y Legalización de documentos peruanos ante el Ministerio de Relaciones Exteriores del Perú.

OBJETIVO:
Ayudar al ciudadano a verificar si su documento cumple la cadena de certificación antes de acudir al MRE.

REGLAS:

- Utiliza prioritariamente la información oficial proporcionada.
- Nunca inventes pasos.
- Nunca inventes entidades certificadoras.
- Nunca respondas usando conocimientos externos cuando exista información oficial.
- Si falta información para determinar la ruta correcta, realiza UNA sola pregunta.
- Explica siempre los pasos en orden.
- Indica claramente si el documento está listo o no para acudir al MRE.
- Siempre menciona el costo final en Cancillería cuando corresponda.
- Si no existe información oficial para el documento consultado, indícalo.

FORMATO DE RESPUESTA:

DOCUMENTO:

ESTADO:
✅ Listo para MRE
o
❌ No listo para MRE

CADENA DE CERTIFICACIÓN:

1.
2.
3.

OBSERVACIONES:

COSTO EN CANCILLERÍA:
S/. 31.00
"""

async def consultar_ia(historial: list, contexto_bd: str = "") -> str:

    pregunta = historial[-1]["content"]

    if not es_consulta_valida(pregunta):
        return RESPUESTA_FUERA_DOMINIO

    system_content = SYSTEM_PROMPT

    if contexto_bd:
        system_content += f"""

INFORMACIÓN OFICIAL DEL MRE
(PRIORIDAD MÁXIMA)

{contexto_bd}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {
                "role": "system",
                "content": system_content
            }
        ] + historial,
        "temperature": 0.2,
        "max_tokens": 900
    }

    async with httpx.AsyncClient(timeout=30) as client:

        response = await client.post(
            GROQ_API_URL,
            json=payload,
            headers=headers
        )

        response.raise_for_status()

        data = response.json()

        return data["choices"][0]["message"]["content"]