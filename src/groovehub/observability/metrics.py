import time
import json
import os
from datetime import datetime
import tiktoken

# Precios de referencia (GPT-3.5 Turbo)
COST_PER_1K_INPUT = 0.0015
COST_PER_1K_OUTPUT = 0.0020


class MetricsTracker:
    """
    Clase encargada de rastrear y calcular las métricas de rendimiento y costos 
    de las interacciones con el LLM.
    
    Maneja el cálculo de latencia, conteo de tokens usando tiktoken y 
    estimación de costos basados en precios de referencia. También persiste 
    el historial de interacciones en un archivo local JSON.
    """
    
    def __init__(self):
        """Inicializa los contadores de tiempo y el codificador de tokens."""
        self.start_time = 0
        self.end_time = 0
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def start(self):
        """Inicia el cronómetro para medir la latencia."""
        self.start_time = time.time()

    def stop(self):
        """Detiene el cronómetro para finalizar la medición de latencia."""
        self.end_time = time.time()

    @property
    def latency_ms(self) -> int:
        """
        Calcula la latencia transcurrida desde que se llamó a start() hasta stop().
        
        Returns:
            int: Tiempo de ejecución en milisegundos.
        """
        return int((self.end_time - self.start_time) * 1000)

    def count_tokens(self, text: str) -> int:
        """
        Cuenta la cantidad de tokens en un texto dado usando el codificador cl100k_base.
        
        Args:
            text (str): El texto que se desea tokenizar.
            
        Returns:
            int: La cantidad de tokens calculada. Devuelve 0 si el texto está vacío.
        """
        if not text:
            return 0
        return len(self.encoder.encode(text))

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """
        Calcula el costo estimado de la llamada al modelo.
        
        Args:
            prompt_tokens (int): Cantidad de tokens consumidos en la entrada (prompt).
            completion_tokens (int): Cantidad de tokens generados en la salida.
            
        Returns:
            float: Costo total estimado en dólares, redondeado a 6 decimales.
        """
        input_cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT
        output_cost = (completion_tokens / 1000) * COST_PER_1K_OUTPUT
        return round(input_cost + output_cost, 6)

    def save_log(self, user_query: str, response_json: str, metrics: dict):
        """
        Guarda un registro detallado de la ejecución en metrics/metrics.json.
        
        Crea el directorio si no existe y maneja el caso en que el archivo JSON 
        previo esté corrupto, reiniciando el historial.
        
        Args:
            user_query (str): El mensaje original enviado por el usuario.
            response_json (str): La respuesta del LLM en formato JSON (como string).
            metrics (dict): Diccionario con las métricas calculadas (tokens, costo, etc.).
        """
        # 1. Asegurar que la carpeta existe
        log_dir = "metrics"
        os.makedirs(log_dir, exist_ok=True)
        file_path = os.path.join(log_dir, "metrics.json")

        # 2. Crear el registro actual
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "query_preview": user_query[:50] + "..."
            if len(user_query) > 50
            else user_query,
            "metrics": metrics,
            "response_data": json.loads(response_json),
        }

        # 3. Leer archivo existente (si hay) y agregar
        history = []
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                history = []  # Si el archivo está corrupto, empezamos de nuevo

        history.append(log_entry)

        # 4. Guardar todo de nuevo
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)