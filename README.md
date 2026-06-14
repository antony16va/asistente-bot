# 🇵🇪 Asistente Inteligente para Apostilla y Legalización de Documentos

Sistema conversacional orientado a ciudadanos que requieren realizar trámites de Apostilla y Legalización de documentos peruanos ante el Ministerio de Relaciones Exteriores del Perú (MRE).

El asistente opera a través de WhatsApp y guía al usuario paso a paso para verificar si su documento cumple la cadena de certificación necesaria antes de acudir a Cancillería, reduciendo errores, consultas presenciales innecesarias y tiempos de atención.

---

## 🎯 Problema

Muchos ciudadanos desconocen la cadena de certificación requerida para apostillar o legalizar un documento.

Como consecuencia:

- Acuden al MRE con documentación incompleta.
- Deben realizar trámites adicionales en otras entidades.
- Se incrementan los tiempos de atención.
- Se generan consultas repetitivas en canales de atención.

---

## 💡 Solución

El sistema utiliza Inteligencia Artificial y búsqueda semántica para identificar el tipo de documento consultado y brindar orientación oficial basada en la cadena de certificación registrada en la base de datos.

El asistente:

- Identifica el documento consultado.
- Recupera la cadena oficial de certificación.
- Explica los pasos requeridos.
- Indica si el documento está listo para ser presentado al MRE.
- Informa costos y observaciones relevantes.
- Atiende automáticamente vía WhatsApp.

---

## 🏗 Arquitectura de la Solución

```text
Ciudadano
     │
     ▼
 WhatsApp
     │
     ▼
 Evolution API
     │
     ▼
 FastAPI
     │
     ├────────► PostgreSQL + pgvector
     │              │
     │              ▼
     │        Búsqueda Semántica
     │
     ▼
 Groq LLM
     │
     ▼
 Respuesta Inteligente
     │
     ▼
 WhatsApp
```
---
## 🚀 Tecnologías Utilizadas
#Infraestructura
Oracle Cloud Infrastructure (OCI)
Ubuntu Server
Nginx
#Backend
Python 3.12
FastAPI
AsyncPG
#Inteligencia Artificial
Groq API
Llama 3.3 70B Versatile
Sentence Transformers
all-MiniLM-L6-v2
#Base de Datos
PostgreSQL 17
pgvector
#Comunicación
Evolution API
WhatsApp

---
##📂 Estructura del Proyecto

```text
asistente-bot/
│
├── app/
│   ├── config.py
│   ├── database.py
│   ├── ia.py
│   └── main.py
│
├── routers/
│   └── webhook.py
│
├── generar_embeddings.py
│
├── requirements.txt
│
├── .env
│
└── README.md
```
---
## 🧠 Funcionamiento
1. Recepción del mensaje

El ciudadano envía una consulta por WhatsApp.

Ejemplo:
¿Cómo puedo apostillar mi título universitario?

2. Vectorización de la consulta

La pregunta es convertida a un embedding utilizando:
sentence-transformers/all-MiniLM-L6-v2

3. Búsqueda Semántica

El sistema identifica el tipo documental más cercano mediante pgvector.

Ejemplo:
Título Universitario

4. Recuperación de contexto

Se obtiene la cadena oficial registrada:
Universidad
↓
SUNEDU
↓
Ministerio de Relaciones Exteriores

5. Generación de respuesta

El contexto oficial es enviado al modelo LLM mediante RAG.

El modelo genera una respuesta estructurada y comprensible para el ciudadano.
---
##📊 Modelo de Datos
mae_tipo_documento

Catálogo de documentos admitidos.

Ejemplos:

- Título Universitario
- Partida de Nacimiento
- Certificado Médico
- Antecedentes Penales
- Documento Notarial

#tab_cadena_certificacion

Almacena los pasos oficiales requeridos para cada documento.

Ejemplo:
| Orden | Entidad     | Paso                  |
| ----- | ----------- | --------------------- |
| 1     | Universidad | Emisión del documento |
| 2     | SUNEDU      | Registro y validación |
| 3     | MRE         | Apostilla             |

#mae_entidad_certificadora

Información de entidades certificadoras:

Nombre
Dirección
Teléfono
Página web
---
##🔐 Variables de Entorno
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=

GROQ_API_KEY=

EVOLUTION_API_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
---
##⚙ Instalación
1. Clonar repositorio
git clone https://github.com/usuario/asistente-bot.git
cd asistente-bot

2. Crear entorno virtual
python -m venv venv
Linux:
source venv/bin/activate
Windows:
venv\Scripts\activate

3. Instalar dependencias
pip install -r requirements.txt

4. Configurar variables
Crear archivo:
.env
5. Generar embeddings
python generar_embeddings.py

6. Ejecutar API
uvicorn app.main:app --host 0.0.0.0 --port 8000
---
##📌 Características Implementadas
✅ Atención vía WhatsApp
✅ Integración con Evolution API
✅ PostgreSQL + pgvector
✅ Embeddings semánticos
✅ Retrieval Augmented Generation (RAG)
✅ Historial conversacional
✅ Detección automática de documentos
✅ Respuestas basadas en información oficial
✅ Restricción temática (solo apostilla y legalización)
✅ Arquitectura asíncrona
---
##🔮 Mejoras Futuras
Validación automática de requisitos documentales.
Portal web para consultas.
Dashboard estadístico.
Integración con Power BI.
Soporte multicanal (Web, Telegram y Microsoft Teams).
Integración con sistemas institucionales del MRE.
---
##👨‍💻 Autores
-Antony Valencia Meza
-Güido Maidana Aquino
-Jhojan Tarazona Gómez
-Alvaro Espinoza Garate

Estudiantes de Ingeniería de Sistemas
Universidad Nacional Federico Villarreal
