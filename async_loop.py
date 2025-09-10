import asyncio
import threading

# Cria o loop global
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Roda em background
def start_loop():
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()