import sys
from colorama import init, Fore, Style
from pydantic import ValidationError

from groovehub.agent.core import MusicAgent
from groovehub.observability.metrics import MetricsTracker
from groovehub.models.response import AdvisorResponse
from groovehub.guardrails.safety import SecurityFilter


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
    print("\033[H\033[J", end="")

    print(
        Fore.MAGENTA
        + Style.BRIGHT
        + r"""
   _____                           _   _       _     
  / ____|                         | | | |     | |    
 | |  __ _ __ ___   _____   _____ | |_| |_   _| |__  
 | | |_ | '__/ _ \ / _ \ \ / / _ \|  _  | | | | '_ \ 
 | |__| | | | (_) | (_) \ V /  __/| | | | |_| | |_) |
  \_____|_|  \___/ \___/ \_/ \___||_| |_|\__,_|_.__/ 
    """
        + Style.RESET_ALL
    )
    print(Style.DIM + "  Music Instrument Advisor v1.0\n")

    print(
        Fore.CYAN
        + "🤖 Groov:"
        + Fore.WHITE
        + " ¡Hola! Soy tu experto musical. ¿En qué te ayudo hoy?"
    )
    print(Style.DIM + "   (Escribe 'salir' o 'exit' para terminar)\n")

    agent = MusicAgent()
    tracker = MetricsTracker()

    while True:
        try:
            # Pedir input al usuario
            user_input = input(Fore.GREEN + "➜ " + Fore.WHITE).strip()

            # Condición de salida
            if user_input.lower() in ["salir", "exit", "quit", "chau", "adios"]:
                print(Fore.GREEN + Style.BRIGHT + "¡Que siga la música! 👋")
                break

            if not user_input:
                continue

            # Capa de seguridad
            is_safe, reason = SecurityFilter.check_safety(user_input)
            if not is_safe:
                print(Fore.RED + f"🚫 ALERTA DE SEGURIDAD: {reason}")
                continue

            # --- INICIO DE LA MEDICIÓN ---
            print(Style.DIM + "thinking...", end="\r")
            tracker.start()

            # Llamar al cerebro (El Agente)
            response: AdvisorResponse = agent.ask(user_input)

            # --- FIN DE LA MEDICIÓN ---
            tracker.stop()

            # Cálculos de Ingeniería (Métricas)
            input_tokens = tracker.count_tokens(user_input)
            output_tokens = tracker.count_tokens(response.model_dump_json())
            cost = tracker.calculate_cost(input_tokens, output_tokens)

            # Mostrar la Respuesta al Usuario
            print(Fore.CYAN + "\n🤖 Groov: " + Fore.WHITE + response.answer)
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

            # Mostrar el reporte técnico (JSON + Métricas)
            print_metrics(
                {
                    "latency_ms": tracker.latency_ms,
                    "cost_usd": cost,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "total_tokens": input_tokens + output_tokens,
                }
            )

            # Preparar datos para el reporte
            metrics_data = {
                "latency_ms": tracker.latency_ms,
                "cost_usd": cost,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "total_tokens": input_tokens + output_tokens,
            }
            # Guardar el archivo con el reporte
            tracker.save_log(
                user_query=user_input,
                response_json=response.model_dump_json(),
                metrics=metrics_data,
            )

        except KeyboardInterrupt:
            print("\n" + Fore.RED + "Programa interrumpido. ¡Adiós!")
            sys.exit(0)

        except ValidationError as e:
            tracker.stop()
            print(Fore.RED + "\n⚠️  Alerta de Alucinación:")
            print(Fore.YELLOW + "El modelo intentó usar una categoría no permitida.")
            print(Fore.WHITE + "Por favor, intenta reformular tu pregunta.\n")
            print(Fore.RED + "\n" + e)

        except Exception as e:
            print(Fore.RED + f"💥 Error inesperado: {e}")


if __name__ == "__main__":
    main()
