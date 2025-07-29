# RX.py

from lora_handler import LoRaHandler
import time

def on_receive(payload):
    print("📥 Received:", payload)

if __name__ == "__main__":
    lora = LoRaHandler()
    lora.setup()
    lora.set_callback(on_receive)

    print("🔄 Listening for messages...")
    try:
        while True:
            lora.loop()  # Polling loop
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("🛑 RX stopped by user.")
        lora.shutdown()
