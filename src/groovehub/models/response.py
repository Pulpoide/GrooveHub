from pydantic import BaseModel, Field
from enum import Enum


# 1. Definimos las acciones permitidas
class AdvisorAction(str, Enum):
    """Acciones permitidas que el sistema puede ejecutar post-respuesta."""
    CHECK_STOCK = "check_stock"          # Verificar disponibilidad
    OFFER_DISCOUNT = "offer_discount"    # Si el cliente duda por precio
    ESCALATE_TO_HUMAN = "escalate_to_human"  # Si la pregunta es muy difícil o hay enojo
    SHOW_CATALOG = "show_catalog"        # Mostrar productos relacionados
    NONE = "none"                        # Solo charla, sin acción comercial


class UserIntent(str, Enum):
    """Clasificación estricta de la intención del usuario para enrutar la lógica."""
    SALES_ADVISORY = "sales_advisory"    # Quiere comprar o pide recomendación
    TECHNICAL_SUPPORT = "technical_support"  # Tiene problemas con algo que ya compró
    SHIPPING_INFO = "shipping_info"      # Pregunta por envíos
    OFF_TOPIC = "off_topic"              # Pregunta fuera de dominio
    ERROR = "error"                      # Fallback interno en caso de fallo del LLM


# 2. Definimos la estructura de la respuesta
class AdvisorResponse(BaseModel):
    """
    Modelo de datos principal que estructura la salida del LLM.
    Asegura que la respuesta siempre tenga el formato correcto para ser 
    procesada por la aplicación de consola.
    """
    answer: str = Field(
        description="La respuesta amable y técnica del asistente al cliente."
    )
    confidence_score: float = Field(
        description="Nivel de confianza en la respuesta, de 0.0 a 1.0.", ge=0.0, le=1.0
    )
    intent: UserIntent = Field(
        description="La clasificación de la intención del usuario."
    )
    recommended_actions: list[AdvisorAction] = Field(
        description="Lista de acciones que el sistema debería ejecutar post-respuesta."
    )
    reasoning: str | None = Field(
        default=None,
        description="Breve explicación de por qué elegiste esas acciones y esa respuesta. (Chain of Thought)"
    )