import asyncio
import asyncpg
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}

async def generar_embeddings():

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    conn = await asyncpg.connect(**DB_CONFIG)

    tipos = await conn.fetch("""
        SELECT
            n_id_pk,
            c_nombre,
            c_descripcion
        FROM asistente.mae_tipo_documento
        WHERE c_activo = 'S'
    """)

    for tipo in tipos:

        pasos = await conn.fetch("""
            SELECT c_descripcion_paso
            FROM asistente.tab_cadena_certificacion
            WHERE n_id_tipo_documento = $1
            AND c_activo = 'S'
            ORDER BY n_orden
        """, tipo["n_id_pk"])

        texto = f"""
        Tipo de documento:
        {tipo['c_nombre']}

        Descripción:
        {tipo['c_descripcion'] or ''}

        Cadena de certificación:
        {' '.join(
            p['c_descripcion_paso']
            for p in pasos
        )}
        """

        vector = model.encode(texto).tolist()

        await conn.execute(
            """
            UPDATE asistente.mae_tipo_documento
            SET embedding = $1
            WHERE n_id_pk = $2
            """,
            str(vector),
            tipo["n_id_pk"]
        )

        print(
            f"Embedding generado: "
            f"{tipo['c_nombre']}"
        )

    await conn.close()

asyncio.run(
    generar_embeddings()
)
