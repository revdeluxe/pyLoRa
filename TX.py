# TX.py

from lora_module import LoRa
import time

def main():
    lora = LoRa()
    lora.begin()  # or initialize whatever is needed

    payload = "Test from TX"
    print("📤 Sending:", payload)
    lora.send(payload.encode('utf-8'))

    print("✅ Message sent.")
    lora.close()

if __name__ == "__main__":
    main()
