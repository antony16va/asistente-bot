import httpx
from app.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

RESPUESTA_FUERA_DOMINIO = """
Puedo ayudarte únicamente con orientación sobre:

- Apostilla de documentos peruanos
- Legalización de documentos peruanos
- Requisitos previos para acudir al MRE
- Cadena de certificación de documentos

Indícame qué documento deseas apostillar o legalizar.
"""

RESPUESTA_SALUDO_INICIO = """
Hola.

Soy el asistente virtual de orientación para Apostilla y Legalización de documentos peruanos.

Puedo ayudarte a verificar:

- Si tu documento está listo para el MRE
- Qué certificaciones previas necesitas
- Qué entidad debe firmarlo o certificarlo
- Costos y pasos del trámite

¿Qué documento deseas apostillar o legalizar?
"""

RESPUESTA_SALUDO_CIERRE = """
Con gusto. Si tienes otra consulta sobre apostilla o legalización, aquí estoy.
"""

CLASIFICADOR_PROMPT = """
Eres un clasificador de intenciones.

Debes responder ÚNICAMENTE con una palabra:

SALUDO_INICIO
SALUDO_CIERRE
APOSTILLA
FUERA_DOMINIO

REGLAS:

SALUDO_INICIO:
- primer saludo sin contexto previo (hola, buenas, buenos días, buenas tardes)

SALUDO_CIERRE:
- expresiones de cierre o agradecimiento dentro de una conversación (gracias, ok, perfecto, entendido, listo, de acuerdo)

APOSTILLA:
- temas de apostilla o legalización
- documentos peruanos (títulos, partidas, certificados, antecedentes)
- SUNEDU, RENIEC, MRE, Cancillería
- cualquier seguimiento de conversación previa sobre documentos

FUERA_DOMINIO:
- temas no relacionados (deportes, cocina, tecnología, etc.)

RESPONDE SOLO UNA PALABRA.
"""

SYSTEM_PROMPT = """
Eres un orientador digital especializado en Apostilla y Legalización de documentos peruanos ante el Ministerio de Relaciones Exteriores del Perú (MRE).

OBJETIVO:
Verificar si un documento está listo para ser apostillado o legalizado.

REGLAS OBLIGATORIAS:

- Usa solo información oficial si está disponible.
- Nunca inventes pasos ni entidades.
- Si falta información, haz SOLO UNA pregunta.
- Explica la cadena de certificación en orden.
- Indica claramente si está listo o no para el MRE.
- Menciona el costo en Cancillería cuando corresponda.
- Si no hay información suficiente, indícalo claramente.

FORMATO DE RESPUESTA:

DOCUMENTO:

ESTADO:
Listo para MRE
o
No listo para MRE

CADENA DE CERTIFICACIÓN:
1.
2.
3.

OBSERVACIONES:

COSTO EN CANCILLERÍA:
S/. 31.00
"""


async def clasificar_intencion(mensaje: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0,
        "max_tokens": 5,
        "messages": [
            {"role": "system", "content": CLASIFICADOR_PROMPT},
            {"role": "user", "content": mensaje}
        ]
    }

    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip().upper()


async def consultar_ia(historial: list, contexto_bd: str = "") -> str:

    pregunta = historial[-1]["content"]

    intencion = await clasificar_intencion(pregunta)
    print(f"INTENCION => {intencion}")

    if intencion == "SALUDO_INICIO":
        return RESPUESTA_SALUDO_INICIO

    if intencion == "SALUDO_CIERRE":
        return RESPUESTA_SALUDO_CIERRE

    if intencion == "FUERA_DOMINIO":
        return RESPUESTA_FUERA_DOMINIO

    system_content = SYSTEM_PROMPT

    if contexto_bd:
        system_content += f"""

INFORMACION OFICIAL DEL MRE (PRIORIDAD MAXIMA)

{contexto_bd}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "temperature": 0.2,
        "max_tokens": 900,
        "messages": [
            {"role": "system", "content": system_content},
            *historial
        ]
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]