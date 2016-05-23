import smbus


class TouchPot:
    """
    Controls a Sparkfun touch potentiometer via i2c
    """
    def __init__(self, i2c_bus_number, address):
        """
        Takes a data bus to communicate over, should
        be an I2C bus that implements write_byte
        """
        self.address = address
        self.bus = smbus.SMBus(i2c_bus_number)
        self.MIN_VALUE = 0
        self.MAX_VALUE = 127

    def get_current_value(self):
        """
        :return: Returns the current potentiometer reading
        """
        return self.bus.read_byte(self.address)
