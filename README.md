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
