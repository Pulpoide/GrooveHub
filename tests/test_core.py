import pytest
from groovehub.models.response import AdvisorResponse, UserIntent


def test_advisor_response_validation():
    """
    Prueba que Pydantic valide correctamente los datos correctos e incorrectos.
    """

    # CASO 1: Datos válidos
    valid_data = {
        "answer": "La guitarra Fender es genial.",
        "confidence_score": 0.95,
        "intent": "sales_advisory",
        "recommended_actions": ["check_stock"],
        "reasoning": "Test reasoning",
    }

    model = AdvisorResponse(**valid_data)
    assert model.intent == UserIntent.SALES_ADVISORY
    assert model.confidence_score == 0.95

    # CASO 2: Datos inválidos
    invalid_data = {
        "answer": "Esto va a fallar",
        "confidence_score": 2.0,
        "intent": "comprar_pizza",
        "recommended_actions": [],
    }

    # Verificamos que lance un error de validación
    with pytest.raises(ValueError):
        AdvisorResponse(**invalid_data)


if __name__ == "__main__":
    test_advisor_response_validation()
    print("✅ Todos los tests pasaron exitosamente.")
