# 🇵🇪 Asistente Inteligente para Apostilla y Legalización de Documentos

Sistema conversacional basado en Inteligencia Artificial orientado a ciudadanos que requieren realizar trámites de **Apostilla** y **Legalización de documentos peruanos** ante el Ministerio de Relaciones Exteriores del Perú (MRE).

El asistente opera a través de **WhatsApp** y guía al usuario paso a paso para verificar si su documento cumple con la cadena de certificación necesaria antes de acudir a Cancillería, reduciendo errores, consultas presenciales innecesarias y tiempos de atención.

---

## 🎯 Problema

Muchos ciudadanos desconocen la cadena de certificación requerida para apostillar o legalizar un documento.

Como consecuencia:

* Acuden al MRE con documentación incompleta.
* Deben realizar trámites adicionales en otras entidades.
* Se incrementan los tiempos de atención.
* Se generan consultas repetitivas en los canales de atención.

---

## 💡 Solución

El sistema utiliza **Inteligencia Artificial**, **embeddings semánticos** y **Retrieval-Augmented Generation (RAG)** para identificar el tipo de documento consultado y brindar orientación oficial basada en la cadena de certificación registrada en la base de datos.

### Funcionalidades principales

✅ Identifica automáticamente el documento consultado.

✅ Recupera la cadena oficial de certificación.

✅ Explica los pasos requeridos para completar el trámite.

✅ Indica si el documento está listo para ser presentado al MRE.

✅ Informa costos y observaciones relevantes.

✅ Atiende consultas automáticamente mediante WhatsApp.

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

### ☁ Infraestructura

* Oracle Cloud Infrastructure (OCI)
* Ubuntu Server
* Nginx

### ⚙ Backend

* Python 3.12
* FastAPI
* AsyncPG

### 🧠 Inteligencia Artificial

* Groq API
* Llama 3.3 70B Versatile
* Sentence Transformers
* all-MiniLM-L6-v2
* Retrieval-Augmented Generation (RAG)

### 🗄 Base de Datos

* PostgreSQL 17
* pgvector

### 📱 Comunicación

* Evolution API
* WhatsApp

---

## 📂 Estructura del Proyecto

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
├── requirements.txt
├── .env
└── README.md
```

---

## 🧠 Funcionamiento

### 1. Recepción de la consulta

El ciudadano envía una consulta mediante WhatsApp.

**Ejemplo:**

```text
¿Cómo puedo apostillar mi título universitario?
```

### 2. Vectorización de la consulta

La pregunta es transformada en un embedding utilizando:

```text
sentence-transformers/all-MiniLM-L6-v2
```

### 3. Búsqueda semántica

Mediante pgvector se identifica el tipo documental más similar.

**Resultado detectado:**

```text
Título Universitario
```

### 4. Recuperación del contexto

Se obtiene la cadena oficial registrada para dicho documento.

```text
Universidad
     ↓
SUNEDU
     ↓
Ministerio de Relaciones Exteriores
```

### 5. Generación de respuesta

La información recuperada se envía al modelo LLM mediante RAG.

El modelo genera una respuesta clara, estructurada y comprensible para el ciudadano.

---

## 📊 Modelo de Datos

### mae_tipo_documento

Catálogo de documentos admitidos.

**Ejemplos:**

* Título Universitario
* Partida de Nacimiento
* Certificado Médico
* Antecedentes Penales
* Documento Notarial

---

### tab_cadena_certificacion

Almacena los pasos oficiales requeridos para cada documento.

| Orden | Entidad     | Paso                  |
| ----- | ----------- | --------------------- |
| 1     | Universidad | Emisión del documento |
| 2     | SUNEDU      | Registro y validación |
| 3     | MRE         | Apostilla             |

---

### mae_entidad_certificadora

Información de las entidades certificadoras:

* Nombre
* Dirección
* Teléfono
* Página web

---

## 🔐 Variables de Entorno

```env
# Base de datos
DB_HOST=
DB_PORT=
DB_USER=
DB_PASSWORD=
DB_NAME=

# IA
GROQ_API_KEY=

# Evolution API
EVOLUTION_API_URL=
EVOLUTION_API_KEY=
EVOLUTION_INSTANCE=
```

---

## ⚙ Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/usuario/asistente-bot.git

cd asistente-bot
```

### 2. Crear entorno virtual

#### Linux

```bash
python -m venv venv

source venv/bin/activate
```

#### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear el archivo:

```text
.env
```

### 5. Generar embeddings

```bash
python generar_embeddings.py
```

### 6. Ejecutar la API

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 📌 Características Implementadas

* Atención automática vía WhatsApp.
* Integración con Evolution API.
* PostgreSQL + pgvector.
* Embeddings semánticos.
* Retrieval-Augmented Generation (RAG).
* Historial conversacional.
* Detección automática de documentos.
* Respuestas basadas en información oficial.
* Restricción temática (apostilla y legalización).
* Arquitectura completamente asíncrona.

---

## 🔮 Mejoras Futuras

* Validación automática de requisitos documentales.
* Portal web para consultas.
* Dashboard estadístico.
* Integración con Power BI.
* Soporte multicanal (Web, Telegram y Microsoft Teams).
* Integración con sistemas institucionales del MRE.
* Analítica de consultas ciudadanas.
* Panel administrativo para gestión documental.

---

## 👨‍💻 Autores

**Antony Valencia Meza**

**Güido Maidana Aquino**

**Jhojan Tarazona Gómez**

**Álvaro Espinoza Garate**

### Universidad Nacional Federico Villarreal

Estudiantes de Ingeniería de Sistemas

---

## 📄 Licencia

Proyecto desarrollado con fines académicos y de innovación tecnológica para la mejora de la orientación ciudadana en trámites de Apostilla y Legalización de Documentos.

