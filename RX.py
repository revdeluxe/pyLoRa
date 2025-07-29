# RX.py

from lora_module import LoRa
import time

def main():
    lora = LoRa(freq_mhz=433.0)
    print("🔄 Listening for messages... (Ctrl+C to exit)")

    try:
        while True:
            data = lora.receive()
            if data:
                text = data.decode('utf-8', errors='ignore')
                print(f"📥 Received: {text}")
            # Continue listening
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("🛑 RX stopped by user")
    finally:
        lora.close()

if __name__ == "__main__":
    main()
