# 🥁 Groove Hub CLI

**Groove Hub** es un asistente inteligente de línea de comandos (CLI) diseñado para músicos. Actúa como un experto en ventas y soporte técnico para instrumentos musicales, impulsado por Inteligencia Artificial (**Llama 3 / GPT-4**) y controlado por una arquitectura de ingeniería de software robusta.

A diferencia de un chat convencional, **Groove Hub** garantiza respuestas estructuradas (JSON), valida la seguridad de los inputs, recuerda el contexto de la conversación y mantiene un registro detallado de métricas y costos.


## 🚀 Características Principales

* **🧠 Memoria Conversacional:** El asistente (**Groov**) mantiene el contexto de la charla para una experiencia fluida y natural.
* **🦎 Soporte Multi-Provider:** Detecta automáticamente tu configuración. Prioriza **OpenAI** (producción) pero permite usar **Groq** (desarrollo rápido y gratuito) sin cambiar el código.
* **🛡️ Seguridad Avanzada (LLM Hardening):** Implementa defensa en profundidad contra *Prompt Injection*. Utiliza **Input Isolation** (XML tags), estrategia **Sandwich Defense** (recordatorios de sistema efímeros) y limpieza de Markdown para garantizar la inmutabilidad de las instrucciones del sistema.
* **📊 Observabilidad:** Registra logs detallados de cada interacción (Tokens, Latencia, Costo estimado) en `metrics/metrics.json`.
* **🧪 Testeado:** Cuenta con una suite de pruebas automatizadas con `pytest`.

## 📂 Estructura del Proyecto
```text
groovehub/
├── metrics/
│   └── metrics.json
├── reports/
│   └── PI_report_en.md
├── src/
│   └── groovehub/
│       ├── agent/
│       │   ├── prompts/
│       │   │   └── main_prompt.py
│       │   ├── init.py
│       │   └── core.py
│       ├── cli/
│       │   └── main.py
│       ├── guardrails/
│       │   ├── init.py
│       │   └── safety.py
│       ├── models/
│       │   ├── init.py
│       │   └── response.py
│       ├── observability/
│       │   ├── init.py
│       │   └── metrics.py
│       └── services/
│           ├── init.py
│           └── llm.py
├── tests/
│   └── test_core.py
├── .env
├── .env.example
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
└── uv.lock
```

## 🛠️ Instalación y Uso

Este proyecto utiliza **uv** para una gestión de dependencias moderna y ultra-rápida.

### Prerrequisitos
* Python 3.12+
* `uv` instalado
* API Key de **Groq** (Recomendada para desarrollo) o **OpenAI**.

### Pasos de Instalación

1.  **Clonar el repositorio:**
    `git clone https://github.com/Pulpoide/groovehub.git`
    `cd groovehub`

2.  **Configurar Variables de Entorno:**
    Crea un archivo `.env` en la raíz con tu clave:
    `GROQ_API_KEY=gsk_tu_clave_aqui...` o `OPENAI_API_KEY=sk_tu_clave_aqui...`

3.  **Instalar Dependencias:**
    `uv sync`

4.  **Ejecutar la Aplicación:**
    `uv run groove`


## 🧪 Ejecutar Tests

Para verificar la integridad del sistema y la validación de esquemas:
`uv run pytest`


## 👤 Autor

**Joaquin Dario Olivero** Desarrollador de Software & Baterista  
📍 Córdoba, Argentina.