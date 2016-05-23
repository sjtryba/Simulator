import seven_segment_i2c


class PropellantDisplay:
    def __init__(self, left_address, right_address):
        # -------------------VARIABLES-------------------
        self.left_display = seven_segment_i2c.SevenSegmentDisplay(1, left_address)
        self.right_display = seven_segment_i2c.SevenSegmentDisplay(1, right_address)

    def display(self, value):
        if len(str(value)) <= 4:
            self.right_display.write_int(value)
        elif 4 < len(str(value)) <= 8:
            value_array = [int(i) for i in str(value)]

            # Separate the last four digits from the rest of the array
            right_values = value_array[-4:]
            left_values = value_array[:(len(value_array) - 4)]

            # Convert the arrays into integers
            right_values = int(''.join(map(str, right_values)))
            left_values = int(''.join(map(str, left_values)))

            # Display both values
            self.left_display.write_int(left_values)
            self.right_display.write_int(right_values, 0)
