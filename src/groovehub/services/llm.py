import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class LLMService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1"
        )
        self.model = "llama-3.3-70b-versatile" 

    def get_completion(self, messages: list) -> str:
        """
        Envía una lista de mensajes al LLM y retorna el contenido crudo.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2, 
                response_format={"type": "json_object"}
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error crítico conectando con Groq: {e}")
            raise e