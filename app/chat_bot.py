import httpx
from app.config import GROQ_API_KEY

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# =====================================================
# RESPUESTAS PREDEFINIDAS
# =====================================================

RESPUESTA_FUERA_DOMINIO = """
Puedo ayudarte únicamente con orientación sobre:

• Apostilla de documentos peruanos
• Legalización de documentos peruanos
• Requisitos previos para acudir al MRE
• Cadena de certificación de documentos

Indícame qué documento deseas apostillar o legalizar.
"""

RESPUESTA_SALUDO = """
👋 Hola.

Soy el asistente virtual de orientación para Apostilla y Legalización de documentos peruanos.

Puedo ayudarte a verificar:

• Si tu documento está listo para el MRE
• Qué certificaciones previas necesitas
• Qué entidad debe firmarlo o certificarlo
• Costos y pasos del trámite

¿Qué documento deseas apostillar o legalizar?
"""

# =====================================================
# CLASIFICADOR PROMPT
# =====================================================

CLASIFICADOR_PROMPT = """
Eres un clasificador de intenciones.

Debes responder ÚNICAMENTE con una palabra:

SALUDO
APOSTILLA
FUERA_DOMINIO

REGLAS:

SALUDO:
- saludos básicos (hola, buenas, buenos días, gracias, ok, perfecto)

APOSTILLA:
- temas de apostilla o legalización
- documentos peruanos (títulos, partidas, certificados, antecedentes)
- SUNEDU, RENIEC, MRE, Cancillería
- cualquier seguimiento de conversación previa

FUERA_DOMINIO:
- temas no relacionados (deportes, cocina, tecnología, etc.)

RESPONDE SOLO UNA PALABRA.
"""

# =====================================================
# PROMPT PRINCIPAL MRE
# =====================================================

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

# =====================================================
# CLASIFICADOR DE INTENCIÓN
# =====================================================

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


# =====================================================
# FUNCIÓN PRINCIPAL DEL CHATBOT
# =====================================================

async def consultar_ia(historial: list, contexto_bd: str = "") -> str:

    pregunta = historial[-1]["content"]

    # 1. Clasificar intención
    intencion = await clasificar_intencion(pregunta)
    print(f"INTENCION => {intencion}")

    # 2. Respuestas rápidas sin IA
    if intencion == "SALUDO":
        return RESPUESTA_SALUDO

    if intencion == "FUERA_DOMINIO":
        return RESPUESTA_FUERA_DOMINIO

    # 3. Construcción del prompt principal
    system_content = SYSTEM_PROMPT

    if contexto_bd:
        system_content += f"""

INFORMACIÓN OFICIAL DEL MRE (PRIORIDAD MÁXIMA)

{contexto_bd}
"""

    # 4. Llamada a Groq (modelo principal)
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