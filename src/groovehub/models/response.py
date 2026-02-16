from pydantic import BaseModel, Field
from enum import Enum
from typing import List, Optional

# 1. Definimos las acciones permitidas (Las "Señales")
class AdvisorAction(str, Enum):
    CHECK_STOCK = "check_stock"              # Verificar disponibilidad
    OFFER_DISCOUNT = "offer_discount"        # Si el cliente duda por precio
    ESCALATE_TO_HUMAN = "escalate_to_human"  # Si la pregunta es muy difícil o hay enojo
    SHOW_CATALOG = "show_catalog"            # Mostrar productos relacionados
    NONE = "none"                            # Solo charla, sin acción comercial

class UserIntent(str, Enum):
    SALES_ADVISORY = "sales_advisory"       # Quiere comprar o pide recomendación
    TECHNICAL_SUPPORT = "technical_support" # Tiene problemas con algo que ya compró
    SHIPPING_INFO = "shipping_info"         # Pregunta por envíos
    OFF_TOPIC = "off_topic"                 # Pregunta fuera de dominio (ej: "¿Cuál es tu película favorita?") 

# 2. Definimos la estructura de la respuesta (El Contrato)
class AdvisorResponse(BaseModel):
    answer: str = Field(
        description="La respuesta amable y técnica del asistente al cliente."
    )
    confidence_score: float = Field(
        description="Nivel de confianza en la respuesta, de 0.0 a 1.0.",
        ge=0.0, le=1.0
    )
    intent: UserIntent = Field(
        description="La clasificación de la intención del usuario."
    )
    recommended_actions: List[AdvisorAction] = Field(
        description="Lista de acciones que el sistema debería ejecutar post-respuesta."
    )
    reasoning: Optional[str] = Field(
        description="Breve explicación de por qué elegiste esas acciones y esa respuesta. (Chain of Thought)"
    )