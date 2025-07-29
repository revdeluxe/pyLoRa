# TX.py

from lora_module import LoRa
from lora_handler import LoRaGPIOHandler
from configure import run_checks, check_spi, check_gpio

def configure_lora():
    """
    Run preflight checks and configure LoRa module.
    """
    print("🔧 Configuring LoRa module...")
    if not check_spi():
        print("[❌] SPI check failed. Please resolve issues and try again.")
        return False
    if not check_gpio():
        print("[❌] GPIO check failed. Please resolve issues and try again.")
        return False
    if not run_checks():
        print("[❌] System check failed. Please resolve issues and try again.")
        return False
    print("[✅] LoRa module configured successfully.")
    return True

def main():
    if not configure_lora():
        return
    lora = LoRa()
    lora.reset()               # Optional: HW reset using GPIO
    lora.set_frequency(433)    # MHz
    lora.set_tx_power(14)      # dBm

    payload = "Test from TX"
    print("📤 Sending:", payload)
    lora.send(payload.encode('utf-8'))

    print("✅ Message sent.")
    lora.close()

if __name__ == "__main__":
    main()
