import json
from music_advisor.models import AdvisorResponse
from music_advisor.services.llm import LLMService
from music_advisor.agent.prompts import SYSTEM_PROMPT


class MusicAgent:
    def __init__(self):
        self.llm = LLMService()

        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    def ask(self, user_query: str) -> AdvisorResponse:
        """
        Procesa la pregunta, mantiene el historial y devuelve la respuesta tipada.
        """
        # 2. Agregamos el mensaje del USUARIO a la historia
        self.history.append({"role": "user", "content": user_query})

        # 3. Enviamos TODA la historia al LLM (no solo lo último)
        raw_response = self.llm.get_completion(self.history)

        # 4. Agregamos la respuesta del ASISTENTE a la historia
        self.history.append({"role": "assistant", "content": raw_response})

        try:
            # 3. Validar y convertir con Pydantic
            parsed_data = json.loads(raw_response)
            response_model = AdvisorResponse(**parsed_data)

            return response_model

        except json.JSONDecodeError:
            # Fallback si el LLM no devolvió JSON válido
            return AdvisorResponse(
                answer="Hubo un error interno procesando tu solicitud.",
                confidence_score=0.0,
                intent="error",
                recommended_actions=["escalate_to_human"],
                reasoning="El modelo devolvió un formato inválido.",
            )

    def clear_memory(self):
        """Reinicia la conversación sin matar el programa."""
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]
