import time
import json
import os
from datetime import datetime
import tiktoken

# Precios de referencia (GPT-3.5 Turbo)
COST_PER_1K_INPUT = 0.0015
COST_PER_1K_OUTPUT = 0.0020


class MetricsTracker:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.encoder = tiktoken.get_encoding("cl100k_base")

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    @property
    def latency_ms(self) -> int:
        return int((self.end_time - self.start_time) * 1000)

    def count_tokens(self, text: str) -> int:
        if not text:
            return 0
        return len(self.encoder.encode(text))

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        input_cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT
        output_cost = (completion_tokens / 1000) * COST_PER_1K_OUTPUT
        return round(input_cost + output_cost, 6)

    # --- NUEVO MÉTODO: GUARDAR HISTORIAL ---
    def save_log(self, user_query: str, response_json: str, metrics: dict):
        """
        Guarda la ejecución en metrics/history.json
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
