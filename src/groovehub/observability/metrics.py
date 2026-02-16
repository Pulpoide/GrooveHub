import time
import tiktoken  

# Precios de referencia (GPT-3.5 Turbo) por 1K tokens
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
        """
        Cuenta los tokens exactos usando tiktoken.
        """
        if not text:
            return 0
        return len(self.encoder.encode(text))

    def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        input_cost = (prompt_tokens / 1000) * COST_PER_1K_INPUT
        output_cost = (completion_tokens / 1000) * COST_PER_1K_OUTPUT
        return round(input_cost + output_cost, 6)