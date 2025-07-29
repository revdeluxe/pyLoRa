# configure.py
# System check and configuration validator for LoRa driver environment

import os
import sys
import time

# Import required components
try:
    import spidev
    import lgpio
except ImportError as e:
    print(f"[❌] Missing required Python module: {e.name}")
    sys.exit(1)

from .spi_driver import SPIDriver
from .pinout import Pinout
from .lora_handler import LoRaGPIOHandler
from .registers import REG_VERSION

def check_spi():
    print("[🧪] Checking SPI interface...")
    if not os.path.exists("/dev/spidev0.0"):
        print("[❌] SPI device not found. You may need to enable SPI via `sudo raspi-config`.")
        return False
    try:
        spi = SPIDriver()
        version = spi.read_register(REG_VERSION)
        spi.close()
        if version == 0x12:
            print("[✅] SX127x LoRa chip detected (REG_VERSION = 0x12)")
            return True
        else:
            print(f"[⚠️] Unexpected REG_VERSION: 0x{version:02X}")
            return False
    except Exception as e:
        print(f"[❌] SPI read failed: {e}")
        return False

def check_gpio():
    print("[🧪] Checking GPIO access...")
    try:
        pinout = Pinout()
        gpio = LoRaGPIOHandler(pinout)
        gpio.cleanup()
        print("[✅] GPIO access OK (lgpio working)")
        return True
    except Exception as e:
        print(f"[❌] GPIO check failed: {e}")
        return False

def run_checks() -> bool:
    print("🔍 Running preflight system check...\n")
    spi_ok = check_spi()
    gpio_ok = check_gpio()

    if spi_ok and gpio_ok:
        print("\n✅ System ready. All LoRa dependencies satisfied.")
        return True
    else:
        print("\n❌ System check failed. Please resolve issues and try again.")
        return False

if __name__ == "__main__":
    run_checks()
