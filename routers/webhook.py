from fastapi import APIRouter, Request
import httpx
from app.config import EVOLUTION_API_URL, EVOLUTION_API_KEY, EVOLUTION_INSTANCE
from app.database import get_pool
from app.ia import consultar_ia

router = APIRouter(prefix="/webhook", tags=["webhook"])

async def enviar_mensaje(numero: str, mensaje: str):
    url = f"{EVOLUTION_API_URL}/message/sendText/{EVOLUTION_INSTANCE}"
    headers = {"apikey": EVOLUTION_API_KEY}
    payload = {"number": numero, "text": mensaje}
    async with httpx.AsyncClient() as client:
        await client.post(url, json=payload, headers=headers)

async def obtener_o_crear_usuario(pool, numero: str) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT n_id_pk FROM asistente.tab_usuario WHERE c_nro_whatsapp = $1", numero
        )
        if row:
            return row["n_id_pk"]
        row = await conn.fetchrow(
            "INSERT INTO asistente.tab_usuario (c_nro_whatsapp) VALUES ($1) RETURNING n_id_pk", numero
        )
        return row["n_id_pk"]

async def obtener_o_crear_sesion(pool, id_usuario: int) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """SELECT n_id_pk FROM asistente.cab_sesion
               WHERE n_id_usuario = $1 AND c_estado = 'ACTIVA'
               ORDER BY d_fecha_inicio DESC LIMIT 1""",
            id_usuario
        )
        if row:
            return row["n_id_pk"]
        row = await conn.fetchrow(
            "INSERT INTO asistente.cab_sesion (n_id_usuario) VALUES ($1) RETURNING n_id_pk", id_usuario
        )
        return row["n_id_pk"]

async def obtener_historial(pool, id_sesion: int) -> list:
    async with pool.acquire() as conn:
        rows = await conn.fetch(
            """SELECT c_rol, c_contenido FROM asistente.det_mensaje
               WHERE n_id_sesion = $1
               ORDER BY d_fecha_envio ASC LIMIT 20""",
            id_sesion
        )
        return [{"role": r["c_rol"], "content": r["c_contenido"]} for r in rows]

async def guardar_mensaje(pool, id_sesion: int, rol: str, contenido: str):
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO asistente.det_mensaje (n_id_sesion, c_rol, c_contenido) VALUES ($1, $2, $3)",
            id_sesion, rol, contenido
        )

@router.post("/mensajes")
async def recibir_mensaje(request: Request):
    data = await request.json()
    try:
        if data.get("event") != "messages.upsert":
            return {"status": "ignored"}

        mensaje = data["data"]["message"].get("conversation", "")
        numero = data["data"]["key"]["remoteJid"].replace("@s.whatsapp.net", "")
        from_me = data["data"]["key"].get("fromMe", False)

        if not mensaje or from_me:
            return {"status": "ignored"}

        pool = await get_pool()
        id_usuario = await obtener_o_crear_usuario(pool, numero)
        id_sesion = await obtener_o_crear_sesion(pool, id_usuario)
        historial = await obtener_historial(pool, id_sesion)

        await guardar_mensaje(pool, id_sesion, "user", mensaje)
        historial.append({"role": "user", "content": mensaje})

        respuesta = await consultar_ia(historial)

        await guardar_mensaje(pool, id_sesion, "assistant", respuesta)
        await enviar_mensaje(numero, respuesta)

        return {"status": "ok"}

    except Exception as e:
        print(f"Error: {e}")
        return {"status": "error"}
