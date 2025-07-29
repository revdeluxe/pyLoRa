# TX.py

from lora_handler import LoRaHandler
import time

if __name__ == "__main__":
    lora = LoRaHandler()
    lora.setup()

    message = "Hello from TX at " + time.strftime("%H:%M:%S")
    print("📤 Sending:", message)
    lora.send(message)

    print("✅ TX complete.")
    lora.shutdown()
