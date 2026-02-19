import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class LLMService:
    """
    Servicio encargado de gestionar la conexión y comunicación con los proveedores de LLM.
    
    Detecta automáticamente las credenciales en el entorno (.env) y configura
    el cliente apropiado. Prioriza OpenAI (producción) si la clave está disponible; 
    de lo contrario, utiliza Groq (ideal para desarrollo rápido) sin requerir 
    cambios adicionales en el código.
    """

    def __init__(self):
        """
        Inicializa el servicio LLM, cargando las variables de entorno y
        estableciendo el cliente, el modelo y el proveedor correspondiente.
        
        Raises:
            ValueError: Si no se encuentra ninguna API Key (OpenAI o Groq) en el entorno.
        """
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
        Envía el historial de mensajes al LLM configurado y retorna el contenido generado.
        
        Aplica configuraciones estrictas como temperatura baja (0.2) para mayor 
        determinismo y fuerza el formato de respuesta a un objeto JSON.
        
        Args:
            messages (list): Lista de diccionarios representando el historial de 
                             conversación (roles 'system', 'user', 'assistant').
                             
        Returns:
            str: La respuesta cruda del modelo en formato JSON (como string).
            
        Raises:
            Exception: Si ocurre un error crítico de conexión o de la API del proveedor.
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