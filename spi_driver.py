# spi_driver.py
# Handles low-level SPI communication with SX127x

import spidev

class SPIDriver:
    def __init__(self, bus=0, device=0, speed=5000000):
        """Initialize SPI interface."""
        self.spi = spidev.SpiDev()
        self.spi.open(bus, device)         # /dev/spidev<bus>.<device>
        self.spi.max_speed_hz = speed      # Set SPI clock speed
        self.spi.mode = 0                  # SPI mode 0 is standard for SX127x

    def read_register(self, address):
        """Read a byte from the given register address."""
        result = self.spi.xfer2([address & 0x7F, 0x00])
        return result[1]

    def write_register(self, address, value):
        """Write a byte to the given register address."""
        self.spi.xfer2([address | 0x80, value])

    def read_burst(self, address, length):
        """Read multiple bytes starting from the given address."""
        result = self.spi.xfer2([address & 0x7F] + [0x00] * length)
        return result[1:]  # First byte is dummy

    def write_burst(self, address, values):
        """Write multiple bytes starting from the given address."""
        self.spi.xfer2([address | 0x80] + values)

    def close(self):
        """Close SPI connection."""
        self.spi.close()

if __name__ == "__main__":
    # Example usage
    spi_driver = SPIDriver()
    try:
        # Read a register
        value = spi_driver.read_register(0x01)
        print(f"Register 0x01: {value}")

        # Write to a register
        spi_driver.write_register(0x01, 0xFF)
        print("Wrote 0xFF to register 0x01")

        # Read multiple bytes
        burst_data = spi_driver.read_burst(0x02, 5)
        print(f"Burst data from 0x02: {burst_data}")

    finally:
        spi_driver.close()