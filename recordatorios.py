# recordatorios.py

import time
from datetime import datetime
from memory.memory import obtener_pendientes

def revisar_recordatorios():

    print("🔔 Sistema de recordatorios activo...")

    recordados = set()

    while True:
        ahora = datetime.now().strftime("%Y-%m-%d")

        for p in obtener_pendientes():
            clave = f"{p['texto']}_{p.get('fecha')}"

            if (
                p.get("fecha") == ahora
                and not p.get("completado")
                and clave not in recordados
            ):
                print(f"\n⏰ RECORDATORIO: {p['texto']}\n")

                # 🔊 OPCIONAL (Bloque 4)
                try:
                    import winsound
                    winsound.Beep(1000, 500)
                except:
                    pass

                recordados.add(clave)

        time.sleep(60)