from Adafruit_I2C import Adafruit_I2C
import time


class DisplaySegment:
    """
    Defines the individual display segments of the LED
    """
    MIDDLE_TOP    = 0b00000001  # over line
    RIGHT_TOP     = 0b00000010 
    RIGHT_BOTTOM  = 0b00000100
    MIDDLE_BOTTOM = 0b00001000  # _
    LEFT_BOTTOM   = 0b00010000
    LEFT_TOP      = 0b00100000
    MIDDLE_MIDDLE = 0b01000000  # -


class DotEnum:
    """
    Defines the 'dots' on the display
    """
    # Decimal points are numbered left to right
    DECIMAL_1  = 0b00000001  # n.nnn
    DECIMAL_2  = 0b00000010  # nn.nn
    DECIMAL_3  = 0b00000100  # nnn.n
    DECIMAL_4  = 0b00001000  # nnnn.
    COLON      = 0b00010000  # nn:nn
    APOSTROPHE = 0b00100000  # nnn'n


class SevenSegmentDisplay:
    """
    Controls a Sparkfun 7 Segment display via i2c
    https://learn.sparkfun.com/tutorials/using-the-serial-7-segment-display/firmware-overview
    Note: this code is not a Sparkfun product, use at your own risk!
    """
    def __init__(self, address):
        """
        Takes a data bus to communicate over, should
        be an I2C bus that implements write_byte
        """
        self.address = address
        self.bus = Adafruit_I2C(address, busnum=2)

        # segment control registers for each digit
        # starting with the leftmost digit
        self.segment_addresses = [0x7B, 0x7C, 0x7D, 0x7E]

    def validate_digit(self, cmd):
        """
        Ensure that the digit data we're being
        provided does not evaluate to one
        of the control commands
        """
        if (cmd < 0x76) or (cmd > 0x81):
            return False
        else:
            return True

    def write_byte(self, value):
        # Adding a retry as this seems to fail quite
        # frequently on my setup
        retry_count = 2
        while retry_count > 0:
            try:
                self.bus.writeRaw8(value)
                # this will break us out of the loop
                # if the previous line didn't generate
                # an exception
                retry_count = 0
            except IOError as ex:
                print(value)
                retry_count -= 1
                # add a delay in case the bus was busy
                time.sleep(0.1)
                print('caught exception writing ' + str(hex(value)) + ' remaining: ' + str(retry_count))
                # raise
                if retry_count <= 0:
                    # rethrow the exception if we're done retrying
                    raise

    def restore_factory_defaults(self):
        """
        Restore factory defaults of the display
        """
        self.write_byte(0x81)

    def clear_display(self):
        """
        blanks the display
        """
        self.write_byte(0x76)

    def set_brightness_level(self, percent):
        """
        Sets the brightness level as a percentage
        of total brightness
        """
        if (percent < 0) or (percent > 100):
            print('invalid percentage for brightness, setting to medium level')
            percent = 50
        
        # brightness level can be set from 0 to 255
        val = int((percent / 100.0) * 255)
        # write the control address
        self.write_byte(0x7A)
        # then write the brightness level
        self.write_byte(val)

    def set_cursor_position(self, position):
        """
        sets the cursor position with 0 being the leftmost write_digit
        and 3 being the rightmost
        """
        if (position >= 0) and (position <= 3):
            self.write_byte(0x79)
            self.write_byte(position)
        else:
            print('invalid position ' + str(position))

    def set_nondigits(self, dots=[]):
        """
        enables decimal points, the colon,
        and the apostrophe, takes a list 
        of DotEnums
        """
        # default to all special "dot" LEDs off
        val = 0
        for dot in dots:
            val = val | dot

        # write the command first
        self.write_byte(0x77)
        # then the bitmask comprising all of the
        # enabled items
        # TODO: can we read the existing mask to
        # just turn on additional things???
        self.write_byte(val)

    def write_digit(self, digit):
        """
        Writes a digit to the display at
        the current cursor position. Each
        time as digit is written the cursor
        moves one to the right
        """
        if not self.validate_digit(digit):
            self.write_byte(digit)

    def write_digit_to_position(self, position, digit):
        """
        Write a digit to the display at a specified
        position
        """
        self.set_cursor_position(position)
        self.write_digit(digit)

    def write_segments(self, position, segments=[]):
        """
        Controls the individual LED segments, the
        segments list should be of type DisplaySegment
        """
        if (position >= 0) and (position <= 3):
            # default to all segments off
            val = 0
            for seg in segments:
                val = val | seg
            # write to the control register for the digit whose segments
            # we're updating
            self.write_byte(self.segment_addresses[position])
            self.write_byte(val)
        else:
            print('invalid position', position)

    def write_int(self, val, fill_char=' '):
        """
        write an integer to the display
        fill_char will pad numbers up to 
        four digits. pad occurs on the left
        """
        # write an integer value across all of the digits of the display
        str_val = str(val)
        # need to convert this to a string in case
        # we are passed a number as a fill character
        str_fill_char = str(fill_char)
        if len(str_val) > 4:
            # value has too many digits to be displayed
            print('value is too large to fit on display')
            return
        if len(str_fill_char) > 1:
            print('must use a single character for filling')
            return

        digits_to_fill = 4 - len(str_val)
        # create a string long enough to fill the empty space
        fill_str = digits_to_fill * str_fill_char
        write_str = fill_str + str_val

        for i in range(len(write_str)):
            self.write_digit_to_position(i, ord(write_str[i]))


def display_int(value, left, right):
    """
    This function displays integers up to 8 characters in length on two 4 digit 7-segment displays.
    :param value: Integer to be displayed
    :param left: SevenSegmentDisplay object: Left 4 digit 7-segment display
    :param right: SevenSegmentDisplay object: Right 4 digit 7-segment display
    :return: displays the integer on the displays
    """
    value_array = [int(i) for i in str(value)]

    # Separate the last four digits from the rest of the array
    right_values = value_array[-4:]
    left_values = value_array[:(len(value_array) - 4)]

    # Convert the arrays into integers
    right_values = int(''.join(map(str, right_values)))
    left_values = int(''.join(map(str, left_values)))

    left.write_int(left_values)
    right.write_int(right_values)
