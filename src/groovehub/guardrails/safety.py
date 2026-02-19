from typing import Tuple


class SecurityFilter:
    """
    Capa de seguridad preventiva diseñada para interceptar y bloquear 
    entradas maliciosas o prohibidas antes de que sean procesadas por el LLM.
    
    Ayuda a mitigar ataques de inyección de prompts, exposición de 
    información sensible y ejecución de comandos no deseados, optimizando 
    además los costos de API al descartar peticiones inválidas tempranamente.
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
        Evalúa la entrada del usuario contra reglas de seguridad estáticas,
        incluyendo límites de longitud y una lista negra de palabras clave.
        
        Args:
            user_input (str): El texto crudo ingresado por el usuario.
            
        Returns:
            Tuple[bool, str]: Una tupla donde el primer elemento indica si la 
                              entrada es segura (True) o no (False). El segundo 
                              elemento contiene un mensaje descriptivo del 
                              resultado o la razón del bloqueo.
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