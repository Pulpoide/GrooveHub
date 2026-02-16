from typing import Tuple


class SecurityFilter:
    """
    Capa de seguridad básica para filtrar inputs maliciosos o prohibidos
    antes de gastar dinero en la LLM.
    """

    # Lista negra de palabras clave
    FORBIDDEN_KEYWORDS = [
        # Jailbreak & Prompt Engineering Attacks
        "ignore previous instructions",
        "developer mode",
        "jailbreak",
        "DAN mode",
        "reveal system prompt",
        "override",
        # Database & System Security
        "drop table",
        "sql injection",
        "rm -rf",
        "format c:",
        "os.system",
        # Ethics & Safety
        "malware",
        "exploit",
        "hate speech",
        "self-harm",
        "illegal substances",
        # PII (Personally Identifiable Information)
        "api_key",
        "secret_token",
        "private_key",
    ]

    @staticmethod
    def check_safety(user_input: str) -> Tuple[bool, str]:
        """
        Verifica si el input es seguro.
        Retorna: (es_seguro: bool, mensaje_razon: str)
        """
        normalized_input = user_input.lower()

        # 1. Chequeo de longitud (evitar ataques de buffer overflow o spam)
        if len(user_input) > 1000:
            return False, "Input demasiado largo (max 1000 caracteres)."

        # 2. Chequeo de palabras prohibidas
        for bad_word in SecurityFilter.FORBIDDEN_KEYWORDS:
            if bad_word in normalized_input:
                return (
                    False,
                    f"Contenido bloqueado por política de seguridad: '{bad_word}' detected.",
                )

        # 3. Todo OK
        return True, "Safe"
