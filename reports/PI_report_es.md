# Reporte de Proyecto (PI): Asistente de IA Groove Hub

**Autor:** Joaquin Dario Olivero
**Fecha:** Febrero 2026
**Proyecto:** Groove Hub CLI

---

## 1. Visión de la Arquitectura
Groove Hub ha sido diseñado como un microservicio modular bajo el patrón **Service-Agent-Schema**, alejándose de los scripts lineales simples para adoptar una arquitectura robusta orientada a objetos. El objetivo principal fue desacoplar la lógica de negocio de la naturaleza probabilística del Modelo de Lenguaje (LLM).

### Componentes Principales:
* **El Agente (Gestor de Estado):** Gestiona el historial de la conversación y orquesta el flujo entre el usuario y el LLM. Implementa un mecanismo de memoria a corto plazo para mantener el contexto.
* **Capa de Esquema (Validación):** Utiliza **Pydantic** para forzar un contrato estricto. El LLM está obligado a responder en formato JSON. Si el modelo genera una estructura no conforme o inventa categorías inválidas, el sistema intercepta el error antes de que llegue al usuario.
* **Capa de Servicio (Abstracción):** Actúa como un adaptador camaleónico. Detecta automáticamente las claves de API disponibles (OpenAI o Groq) e instancia el cliente correcto, permitiendo una transición fluida entre desarrollo (Groq/Llama3) y producción (OpenAI/GPT-4).

## 2. Técnicas de Prompting y Justificación
Para garantizar una alta confiabilidad y reducir alucinaciones, implementamos una estrategia de **Few-Shot Chain-of-Thought (CoT)**.

1. **Configuración de Contexto:** El System Prompt define explícitamente la personalidad ("Groov") y resuelve ambigüedades del dominio (por ejemplo, instruyendo al modelo que "batería" se refiere a instrumentos musicales y no a acumuladores de energía).
2. **Enfoque de Razonamiento Primero (CoT):** Instruimos al modelo para que genere un campo de `"reasoning"` (razonamiento) *antes* de la `"answer"` (respuesta) final. Esto obliga al LLM a "pensar" y clasificar la intención del usuario de forma lógica antes de comprometerse con una respuesta, mejorando drásticamente la precisión del `intent`.
3. **Aprendizaje con Ejemplos (Few-Shot):** Proporcionamos ejemplos distintos de Entrada -> Razonamiento -> Salida dentro del prompt. Esto guía al modelo sobre el tono esperado, la estructura JSON y el manejo de casos borde (como preguntas fuera de tema).

## 3. Resumen de Métricas
La observabilidad se implementa a través de un `MetricsTracker` personalizado que utiliza **Tiktoken** para una contabilidad precisa.

* **Latencia:** Mide el tiempo de generación puro del modelo.
* **Uso de Tokens:** Rastrea por separado los tokens de entrada (Prompt) y salida (Completion).
* **Costo Estimado:** Calcula el costo en USD por consulta basado en los niveles de precios del modelo.
* **Puntaje de Confianza:** Una métrica de autoevaluación generada por el modelo sobre la calidad de su respuesta.

### Sample Log Entry
```json
{
  "timestamp": "2026-02-16T16:06:55.711269",
  "query_preview": "Baterías para Jazz, que me recomiendas?",
  "metrics": {
    "latency_ms": 1101,
    "cost_usd": 0.000391,
    "total_tokens": 201
  }
}
```

## 4. Desafíos Enfrentados
* **Cumplimiento Estricto de JSON:** Los LLM ocasionalmente añaden texto conversacional fuera del bloque JSON. Lo resolvimos con mecanismos de reintento de parseo e instrucciones de prompt más estrictas.
* **Compatibilidad de APIs:** Cambiar entre Groq y OpenAI requirió normalizar las llamadas, ya que sus SDK manejan las URLs base y los nombres de modelos de forma diferente.
* **Manejo de Ambigüedades:** Las pruebas iniciales mostraron confusión con términos como "platillos" o "baterías". Esto se resolvió refinando el contexto en el System Prompt.

## 5. Mejoras Potenciales
* **Integración RAG (Generación Aumentada por Recuperación):** Actualmente, el stock es generado por el modelo. Conectar al agente a una base de datos vectorial con inventario real permitiría ofrecer productos reales.
* **Interfaz Web:** Migrar la CLI a una arquitectura FastAPI + React para soportar catálogos visuales y mayor interactividad.
* **Procesamiento Asíncrono:** Implementar `asyncio` para manejar múltiples solicitudes de usuarios de forma concurrente, mejorando la escalabilidad.