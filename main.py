# TENSHI - Punto de entrada principal

from modules.orchestrator import responder
from memory.memory import limpiar_historial

def main():
    print("=" * 40)
    print("        Bienvenido a TENSHI 🤖")
    print("=" * 40)
    print("Escribe 'salir' para terminar.")
    print("Escribe 'limpiar' para borrar la memoria.")
    print("-" * 40)

    while True:
        entrada = input("\nTú: ").strip()

        if entrada.lower() == "salir":
            print("TENSHI: ¡Hasta luego! 👋")
            break
        elif entrada.lower() == "limpiar":
            limpiar_historial()
        elif entrada == "":
            continue
        else:
            print("TENSHI: pensando...")
            respuesta = responder(entrada)
            print(f"\nTENSHI: {respuesta}")

if __name__ == "__main__":
    main()