from itertools import combinations
import random
import seven_segment_i2c
import Adafruit_GPIO as GPIO
import time


# ------------------------------------CONSTANTS----------------------------------
RESISTOR_VALUES = [10,   30,   50,
                  100,  300,  500,
                 1000, 3000, 5000]  # Resistor values in Ohms
# Location of resistors:
# 0 1 2 (parallel group 1)
# 3 4 5 (parallel group 2)
# 6 7 8 (parallel group 3)


def set_goal(combos):
    """
    This function returns a random value from the input list
    :param combos: an array of possible circuit impedance
    """
    return random.choice(combos)


def load_combinations():
    """
    This function calculates the effective impedance for all possible combinations of the resistor puzzle.
    It also returns the error propagation for the given combinations.
    The puzzle consists of 3 groups of resistor in series. Each group has three resistor in parallel.
    """

    # ------------------------------------VARIABLES----------------------------------
    number_of_resistors = len(RESISTOR_VALUES)  # Number of resistors in the puzzle
    resistor_combinations = []  # Initiate a list for the index combinations

    # ------------------------------------COMBINATIONS----------------------------------
    for i in range(number_of_resistors):  # Fill in the list containing all the combinations of the resistors indices
        resistor_combinations.extend(combinations(RESISTOR_VALUES, i + 1))

    equivalent_impedance = [0 for i in range(len(resistor_combinations))]  # Equivalent impedance of the entire circuit

    for i in range(len(resistor_combinations)):
        equivalent_impedance[i] = sum(resistor_combinations[i])  # Sum the parallel impedance
    # equivalent_impedance = sorted(equivalent_impedance)
    # print(equivalent_impedance)
    return equivalent_impedance


def main():
    # Generate the display objects
    goal_display = seven_segment_i2c.SevenSegmentDisplay(address=0x71)
    actual_display = seven_segment_i2c.SevenSegmentDisplay(address=0x72)
    parallel_group_display0 = seven_segment_i2c.SevenSegmentDisplay(address=0x73)
    parallel_group_display1 = seven_segment_i2c.SevenSegmentDisplay(address=0x74)
    parallel_group_display2 = seven_segment_i2c.SevenSegmentDisplay(address=0x75)

    # Set up the input pins for the switches
    pins = ["P8_7",  "P8_9",  "P8_11",
            "P8_8",  "P8_10", "P8_12",
            "P8_14", "P8_16", "P8_18"]

    switches = [GPIO.get_platform_gpio()] * len(pins)
    for i in range(len(switches)):
        switches[i].setup(pins[i], GPIO.IN)

    # Set the goal impedance of the circuit
    goal = set_goal(load_combinations())

    # Set a fake actual resistance to get the while loop started
    # actual = 0

    # Display the goal impedance of the circuit
    goal_display.write_int(goal)

    while True:  # actual != goal:
        # Read all the switches.
        switch_states = [0] * len(switches)
        resistance = [0, 0, 0]
        for i in range(len(switches)):
            switch_states[i] = switches[i].input(pins[i])

        # Calculate the resistance of the display groups
        for i in range(0, 3):
            if switch_states[i]:
                resistance[0] += RESISTOR_VALUES[i]  # Calculate the resistance of the first group
        for i in range(3, 6):
            if switch_states[i]:
                resistance[1] += RESISTOR_VALUES[i]  # Calculate the resistance of the second group
        for i in range(6, 9):
            if switch_states[i]:
                resistance[2] += RESISTOR_VALUES[i]  # Calculate the resistance of the third group

        # I'm not sure what this does, I can't remember why I added it. I think it was because the 'resistance' array
        # was not appending properly, although I can't see how this would fix that...
        for i in range(len(resistance)):
            resistance[i] = resistance[i]

        actual = sum(resistance)

        # Display the resistance values
        parallel_group_display0.write_int(resistance[0])
        parallel_group_display1.write_int(resistance[1])
        parallel_group_display2.write_int(resistance[2])
        actual_display.write_int(actual)

        # Delay for a small amount of time
        time.sleep(0.25)

if __name__ == '__main__':
    main()
