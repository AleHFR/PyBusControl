import asyncio
import threading

# Aquivo que cria um loop que roda contantemente em background

# Cria o loop global
loop = asyncio.new_event_loop()

# Roda em background
def start_loop():
    asyncio.set_event_loop(loop)    
    loop.run_forever()

# Inicia o loop
threading.Thread(target=start_loop, daemon=True).start()