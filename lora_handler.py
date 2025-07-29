# LoRaHandler.py
# Handles GPIO operations (reset, interrupt, etc.) using lgpio

import lgpio
import time

class LoRaGPIOHandler:
    def __init__(self, pinout):
        """
        :param pinout: instance of Pinout class containing pin mapping
        """
        self.pinout = pinout
        self.handle = lgpio.gpiochip_open(0)  # Assumes /dev/gpiochip0

        # Claim pins
        lgpio.gpio_claim_output(self.handle, self.pinout.pins['RST'], 1)
        lgpio.gpio_claim_input(self.handle, self.pinout.pins['DIO0'])

        if 'DIO1' in self.pinout.pins:
            lgpio.gpio_claim_input(self.handle, self.pinout.pins['DIO1'])

    def reset(self):
        """Resets the LoRa module by toggling the RST pin."""
        rst_pin = self.pinout.pins['RST']
        lgpio.gpio_write(self.handle, rst_pin, 0)
        time.sleep(0.1)
        lgpio.gpio_write(self.handle, rst_pin, 1)
        time.sleep(0.1)

    def wait_for_dio0(self, timeout=2.0):
        """Waits for DIO0 to go HIGH within timeout (polling)."""
        dio0 = self.pinout.pins['DIO0']
        start = time.time()
        while time.time() - start < timeout:
            if lgpio.gpio_read(self.handle, dio0) == 1:
                return True
            time.sleep(0.001)
        return False

    def attach_interrupt(self, callback, pin='DIO0', edge=lgpio.RISING_EDGE):
        """Attach interrupt to given pin (default: DIO0)"""
        gpio_pin = self.pinout.pins[pin]
        lgpio.gpio_claim_alert(self.handle, gpio_pin, edge)
        lgpio.set_alert_func(self.handle, gpio_pin, callback)

    def cleanup(self):
        """Close the GPIO handle."""
        lgpio.gpiochip_close(self.handle)
