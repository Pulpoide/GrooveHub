import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMService:
    def __init__(self):

        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.groq_api_key = os.getenv("GROQ_API_KEY")

        if self.openai_api_key:
            self.client = OpenAI(api_key=self.openai_api_key)
            self.model = "gpt-3.5-turbo"
            self.provider = "OpenAI"

        elif self.groq_api_key:
            self.client = OpenAI(
                api_key=self.groq_api_key, base_url="https://api.groq.com/openai/v1"
            )
            self.model = "llama-3.3-70b-versatile"
            self.provider = "Groq"
        else:
            raise ValueError(
                "❌ No se encontró API Key. Configura OPENAI_API_KEY o GROQ_API_KEY en tu .env"
            )

    def get_completion(self, messages: list) -> str:
        """
        Envía mensajes al LLM configurado y retorna el contenido crudo.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"},
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error crítico conectando con {self.provider}: {e}")
            raise e
