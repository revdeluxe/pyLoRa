# pinout.py
# Holds GPIO pin mapping and allows safe pin reconfiguration

class Pinout:
    pinout_version = "1.0.0"

    def __init__(self, cs=8, rst=22, dio0=4, dio1=17):
        # Default pin assignments (BCM numbers)
        self.pins = {
            "CS": cs,        # SPI Chip Select
            "RST": rst,      # Reset pin
            "DIO0": dio0,    # Interrupt for RX Done
            "DIO1": dio1     # Optional: for CAD or RX timeout
        }

    def __getstate__(self):
        return self.__dict__

    def list_pins(self):
        """Returns the current pinout dictionary."""
        return self.pins

    def __setpinout__(self, pin_name, value):
        """Change pin assignment safely."""
        if pin_name in self.pins:
            self.pins[pin_name] = value
        else:
            raise AttributeError(f"{pin_name} is not a valid pin name.")
