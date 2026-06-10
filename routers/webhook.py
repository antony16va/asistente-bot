from fastapi import APIRouter, Request
import httpx
from app.config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE

router = APIRouter(prefix="/webhook", tags=["webhook"])

async def enviar_mensaje(numero: str, mensaje: str):
    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {"apikey": EVOLUTION_API_KEY}
    payload = {
        "number": numero,
        "text": mensaje
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, headers=headers)

@router.post("/mensajes")
async def recibir_mensaje(request: Request):
    data = await request.json()

    try:
        tipo = data.get("event")
        if tipo != "messages.upsert":
            return {"status": "ignored"}

        mensaje = data["data"]["message"].get("conversation", "")
        numero = data["data"]["key"]["remoteJid"].replace("@s.whatsapp.net", "")

        if not mensaje:
            return {"status": "ignored"}

        respuesta = f"Hola, recibí tu mensaje: {mensaje}"
        await enviar_mensaje(numero, respuesta)

        return {"status": "ok"}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error"}
