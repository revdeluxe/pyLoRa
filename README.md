## 🛰️ **LoRa Driver Usage Guide (Cheatsheet)**

### 📁 Project Structure

```plaintext
your_project/
├── lora_driver/
│   ├── __init__.py
│   ├── configure.py        # Environment + system check
│   ├── registers.py        # SX127x register map
│   ├── pinout.py           # Pinout config handler
│   ├── spi_driver.py       # SPI read/write abstraction
│   ├── LoRaHandler.py      # GPIO: reset, DIO0 (IRQ)
│   └── lora_module.py      # High-level LoRa interface
└── main.py                 # Your app that uses the driver
```

---

## ✅ 1. **Initialize & Setup LoRa**

```python
# main.py
from lora_driver import configure, lora_module

# Run system checks
configure.run_checks()
configure.check_spi()
configure.check_gpio()

# Create LoRa object
lora = lora_module.LoRa()

# Initialize
lora.reset()               # Optional: HW reset using GPIO
lora.set_frequency(433)    # MHz
lora.set_tx_power(14)      # dBm

# Set mode
lora.set_mode_rx()         # Standby/Receive/Transmit/etc.
```

---

## 📤 2. **Send a Packet**

```python
data = b"Hello World"
lora.send(data)
```

---

## 📥 3. **Receive a Packet**

```python
if lora.receive():
    packet = lora.read()
    print("Received:", packet)
```

---

## 🛑 4. **Shutdown Gracefully**

```python
lora.close()
```

---

## 🔧 5. **Configure Your Hardware**

Edit `pinout.py` and define your GPIO layout:

```python
self.pins = {
    "reset": 17,
    "dio0": 22,
    "cs": 8
}
```

---

## 🧪 6. **Testing SPI Manually**

```python
from lora_driver.spi_driver import SPIDriver
import lora_driver.registers as reg

spi = SPIDriver()
version = spi.read_register(reg.REG_VERSION)
print(f"Version: 0x{version:02X}")
spi.close()
```

---

## 🪪 7. **MIT License Header (add to each `.py`)**

```python
# SPDX-License-Identifier: MIT
# Copyright (c) 2025 [Your Name]
```

---

## 📝 LICENSE File

Place this in root of your repo:

```plaintext
MIT License

Copyright (c) 2025 revdeluxe

Permission is hereby granted, free of charge, to any person obtaining a copy...
```
