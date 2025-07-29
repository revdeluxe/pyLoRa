# lora_module.py
# High-level LoRa driver for SX127x (TX, RX, config)

from .registers import *
from .spi_driver import SPIDriver
from .lora_handler import LoRaGPIOHandler
from .pinout import Pinout
import time

class LoRa:
    def __init__(self, freq_mhz=433.0, spi_bus=0, spi_device=0):
        self.pinout = Pinout()
        self.spi = SPIDriver(bus=spi_bus, device=spi_device)
        self.gpio = LoRaGPIOHandler(self.pinout)
        self.freq_mhz = freq_mhz

        self.init_radio()

    def read(self):
        """Read received data from the LoRa module."""
        data = self.receive()
        if data is None:
            raise RuntimeError("No data received or timeout.")
        return data

    def init_radio(self):
        """Initialize LoRa radio module."""
        self.gpio.reset()

        version = self.spi.read_register(REG_VERSION)
        if version != 0x12:
            raise RuntimeError(f"Unrecognized radio version: 0x{version:02X}")

        self.sleep()
        self.set_frequency(self.freq_mhz)

        self.spi.write_register(REG_FIFO_TX_BASE_ADDR, 0x00)
        self.spi.write_register(REG_FIFO_RX_BASE_ADDR, 0x00)

        self.spi.write_register(REG_LNA, self.spi.read_register(REG_LNA) | 0x03)
        self.spi.write_register(REG_MODEM_CONFIG_3, 0x04)

        self.set_tx_power(17)  # Max: 20 with PA_DAC tweak
        self.idle()

    def idle(self):
        """Set radio to idle mode."""
        self.gpio.set_to_idle()
        self.spi.write_register(REG_OP_MODE, MODE_STDBY | MODE_LONG_RANGE_MODE)

    def sleep(self):
        """Set radio to sleep mode."""
        self.gpio.set_to_sleep()
        self.spi.write_register(REG_OP_MODE, MODE_SLEEP | MODE_LONG_RANGE_MODE)

    def set_frequency(self, freq_mhz):
        """Set frequency in MHz (e.g., 433.0, 868.0, 915.0)."""
        frf = int((freq_mhz * 1e6) / 61.03515625)
        self.spi.write_register(REG_FRF_MSB, (frf >> 16) & 0xFF)
        self.spi.write_register(REG_FRF_MID, (frf >> 8) & 0xFF)
        self.spi.write_register(REG_FRF_LSB, frf & 0xFF)

    def set_tx_power(self, power_dbm):
        """Set TX power in dBm (0 to 20)."""
        if power_dbm < 0 or power_dbm > 20:
            raise ValueError("TX power must be between 0 and 20 dBm")
        
        pa_config = self.spi.read_register(REG_PA_CONFIG)
        pa_config = (pa_config & 0xF0) | (power_dbm & 0x0F)
        self.spi.write_register(REG_PA_CONFIG, pa_config)

    def set_mode_rx(self):
        """Set radio to receive mode."""
        self.gpio.set_to_rx()
        self.spi.write_register(REG_OP_MODE, MODE_RX_CONTINUOUS | MODE_LONG_RANGE_MODE)

    def set_mode_tx(self):
        """Set radio to transmit mode."""
        self.gpio.set_to_tx()
        self.spi.write_register(REG_OP_MODE, MODE_TX | MODE_LONG_RANGE_MODE)

    def set_mode_sleep(self):
        """Set radio to sleep mode."""
        self.gpio.set_to_sleep()
        self.spi.write_register(REG_OP_MODE, MODE_SLEEP | MODE_LONG_RANGE_MODE)

    def set_mode_idle(self):
        """Set radio to idle mode."""
        self.gpio.set_to_idle()
        self.spi.write_register(REG_OP_MODE, MODE_STDBY | MODE_LONG_RANGE_MODE)

    def send(self, data: bytes):
        """Send a bytes object over LoRa."""
        self.idle()

        self.spi.write_register(REG_FIFO_ADDR_PTR, 0x00)
        self.spi.write_burst(REG_FIFO, list(data))
        self.spi.write_register(REG_PAYLOAD_LENGTH, len(data))

        self.spi.write_register(REG_OP_MODE, MODE_TX | MODE_LONG_RANGE_MODE)

        # Wait for TX Done
        if self.gpio.wait_for_dio0(timeout=2.0):
            self.spi.write_register(REG_IRQ_FLAGS, IRQ_TX_DONE_MASK)
        else:
            raise TimeoutError("TX timeout: DIO0 not triggered.")

    def receive(self):
        """Receive one packet (blocking) and return data as bytes."""
        self.spi.write_register(REG_OP_MODE, MODE_RX_SINGLE | MODE_LONG_RANGE_MODE)

        if not self.gpio.wait_for_dio0(timeout=5.0):
            return None  # Timeout

        irq_flags = self.spi.read_register(REG_IRQ_FLAGS)
        self.spi.write_register(REG_IRQ_FLAGS, irq_flags)  # Clear IRQs

        if irq_flags & IRQ_PAYLOAD_CRC_ERROR_MASK:
            return None  # Bad packet

        current_addr = self.spi.read_register(REG_FIFO_RX_CURRENT_ADDR)
        received_count = self.spi.read_register(REG_RX_NB_BYTES)

        self.spi.write_register(REG_FIFO_ADDR_PTR, current_addr)
        data = self.spi.read_burst(REG_FIFO, received_count)

        return bytes(data)
    
    def reset(self):
        """Reset the LoRa module using GPIO."""
        self.gpio.reset()
        time.sleep(0.1)

    def close(self):
        """Clean up SPI and GPIO."""
        self.spi.close()
        self.gpio.cleanup()
