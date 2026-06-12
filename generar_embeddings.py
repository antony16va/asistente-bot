import asyncio
import asyncpg
from sentence_transformers import SentenceTransformer

DB_CONFIG = {
    "host": "172.17.0.2",
    "port": 5432,
    "user": "asistente_bot",
    "password": "asistente_2026",
    "database": "asistente"
}

async def generar_embeddings():
    print("Cargando modelo de embeddings...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    conn = await asyncpg.connect(**DB_CONFIG)

    tipos = await conn.fetch(
        "SELECT n_id_pk, c_nombre, c_descripcion FROM asistente.mae_tipo_documento WHERE c_activo = 'S'"
    )

    print(f"Generando embeddings para {len(tipos)} tipos de documento...")

    for tipo in tipos:
        texto = f"{tipo['c_nombre']}. {tipo['c_descripcion'] or ''}"
        vector = model.encode(texto).tolist()
        await conn.execute(
            "UPDATE asistente.mae_tipo_documento SET embedding = $1 WHERE n_id_pk = $2",
            str(vector), tipo["n_id_pk"]
        )
        print(f"  ✓ {tipo['c_nombre']}")

    await conn.close()
    print("\nEmbeddings generados correctamente.")

asyncio.run(generar_embeddings())
