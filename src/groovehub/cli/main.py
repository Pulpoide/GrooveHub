import sys
from colorama import init, Fore, Style
from pydantic import ValidationError

from music_advisor.agent.core import MusicAgent
from music_advisor.observability.metrics import MetricsTracker
from music_advisor.models.response import AdvisorResponse


init(autoreset=True)


def print_metrics(metrics: dict):
    """
    Una función auxiliar para imprimir las métricas bonitas y separadas.
    """
    print(Fore.CYAN + Style.BRIGHT + "\n--- 📊 Métricas de la Consulta ---")
    print(f"⏱️  Latencia: {metrics['latency_ms']} ms")
    print(f"💰 Costo Est.: ${metrics['cost_usd']:.6f}")
    print(
        f"🧮 Tokens: {metrics['total_tokens']} (In: {metrics['input_tokens']} / Out: {metrics['output_tokens']})"
    )
    print(Fore.CYAN + Style.BRIGHT + "----------------------------------\n")


def main():
    print(Fore.GREEN + Style.BRIGHT + "🥁🎷🎸 Bienvenido a Groove Hub CLI 🥁🎷🎸")
    # print(Fore.CYAN + "🎼🎵🎶🎙️🎚️🎛️🎤🎧🎷🪗🎸🎹🎺🎻🪕🥁🪘🪇🪈🪉")
    print(Fore.CYAN + Style.BRIGHT + "🎵 Tienda de Instrumentos Musicales 🎵")
    print(Fore.CYAN + "-" * 50)
    print(
        Fore.BLUE
        + "\n🤖 Groov: "
        + Fore.WHITE
        + "¡Hola, soy Groov 👋! Hablá conmigo y resolvé cualquier duda."
    )

    # 1. Instanciamos el Agente y el Tracker una sola vez
    agent = MusicAgent()
    tracker = MetricsTracker()

    # 2. El Bucle Infinito (El corazón del programa)
    while True:
        try:
            # Pedir input al usuario
            user_input = input(Fore.YELLOW + "Tú: " + Fore.RESET).strip()

            # Condición de salida
            if user_input.lower() in ["salir", "exit", "quit", "chau", "adios"]:
                print(Fore.GREEN + Style.BRIGHT + "¡Que siga la música! 👋")
                break

            if not user_input:
                continue

            # --- INICIO DE LA MEDICIÓN ---
            print(Style.DIM + "thinking...", end="\r")
            tracker.start()

            # 3. Llamar al cerebro (El Agente)
            response: AdvisorResponse = agent.ask(user_input)

            # --- FIN DE LA MEDICIÓN ---
            tracker.stop()

            # 4. Cálculos de Ingeniería (Métricas)
            input_tokens = tracker.count_tokens(user_input)
            output_tokens = tracker.count_tokens(response.model_dump_json())
            cost = tracker.calculate_cost(input_tokens, output_tokens)

            # 5. Mostrar la Respuesta al Usuario
            print(Fore.BLUE + "\n🤖 Groov: " + Fore.WHITE + response.answer)

            print(
                Style.DIM
                + f"\n👀 (Confianza: {response.confidence_score * 100:.0f}% | Intención: {response.intent.value})"
            )

            print(Style.DIM + f"💭 {response.reasoning}")

            # Mostrar acciones sugeridas (si las hay)
            if response.recommended_actions:
                actions_str = ", ".join(
                    [action.value for action in response.recommended_actions]
                )
                print(
                    Fore.MAGENTA
                    + Style.BRIGHT
                    + f"\n⚡ Acciones sugeridas: [{actions_str}]"
                )

            # 6. Mostrar el reporte técnico (JSON + Métricas)
            print_metrics(
                {
                    "latency_ms": tracker.latency_ms,
                    "cost_usd": cost,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }
            )

        except KeyboardInterrupt:
            print("\n" + Fore.RED + "Programa interrumpido. ¡Adiós!")
            sys.exit(0)

        except ValidationError as e:
            tracker.stop()
            print(Fore.RED + "\n⚠️  Alerta de Alucinación:")
            print(Fore.YELLOW + "El modelo intentó usar una categoría no permitida.")
            print(Fore.WHITE + "Por favor, intenta reformular tu pregunta.\n")

        except Exception as e:
            print(Fore.RED + f"💥 Error inesperado: {e}")


if __name__ == "__main__":
    main()
