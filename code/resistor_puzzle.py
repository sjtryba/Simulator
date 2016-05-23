from itertools import combinations
import random
import seven_segment_i2c
import Adafruit_GPIO as GPIO
import time


# ------------------------------------CONSTANTS----------------------------------
RESISTOR_VALUES = [1000.0, 1100.0, 1300.0,
                   2000.0, 2100.0, 2300.0,
                   3000.0, 3300.0, 3500.0]  # Resistor values in Ohms
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

    indices = [x for x in range(number_of_resistors)]

    reciprocals = [1 / RESISTOR_VALUES[i] for i in range(number_of_resistors)]  # Reciprocal resistances (1/R)

    index_combinations = []  # Initiate a list for the index combinations

    # ------------------------------------COMBINATIONS----------------------------------
    for i in range(number_of_resistors):  # Fill in the list containing all the combinations of the resistors indices
        index_combinations.extend(combinations(indices, i + 1))

    number_of_combinations = len(index_combinations)  # Number of combinations of resistors

    # Make a list of reciprocal impedance.
    # 0 is for the first parallel group,
    # 1 is for the second parallel group,
    # 2 is for the third parallel group
    reciprocal_impedance = [[0 for x in range(3)] for x in range(number_of_combinations)]

    # Fill in the impedance lists
    for i in range(number_of_combinations):  # Loop through each combination
        for j in range(number_of_resistors):  # Loop through each resistor
            if j in index_combinations[i]:  # If the resistor is 'ON' include it in the impedance
                reciprocal_impedance[i][int(j / 3)] += reciprocals[j]

    # ------------------------------------IMPEDANCE----------------------------------
    # Only count the impedance combination that make a complete circuit
    # Specifically this means having at least one switch in each parallel combination closed
    impedance = []  # Impedance
    equivalent_impedance_index_combinations = []
    for i in range(number_of_combinations):  # Loop through each combination
        if ((indices[0] in index_combinations[i] or indices[1] in index_combinations[i] or indices[2] in
            index_combinations[i]) and  # If there is a closed switch in the first group
                (indices[3] in index_combinations[i] or indices[4] in index_combinations[i] or indices[5] in
                    index_combinations[i]) and  # If there is a closed switch in the second group
                (indices[6] in index_combinations[i] or indices[7] in index_combinations[i] or indices[8] in
                    index_combinations[i])):  # If there is a closed switch in the third group
            r_temp = [0, 0, 0]
            for j in range(3):
                r_temp[j] = 1 / reciprocal_impedance[i][j]
            impedance.append(r_temp)  # Add the impedance to the list
            equivalent_impedance_index_combinations.append(index_combinations[i])

    equivalent_impedance = [0 for x in range(len(impedance))]  # Equivalent impedance of the entire circuit

    for i in range(len(impedance)):
        equivalent_impedance[i] = sum(impedance[i])  # Sum the parallel impedance
    # equivalent_impedance = sorted(equivalent_impedance)
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

    open_loop_val = "0000"

    switches = [GPIO.get_platform_gpio()] * len(pins)
    for i in range(len(switches)):
        switches[i].setup(pins[i], GPIO.IN)

    goal = int(set_goal(load_combinations()))
    print(goal)
    goal_display.write_int(goal)

    while True:
        # Read all the switches.
        switch_states = [0] * len(switches)
        resistance = [0, 0, 0]
        for i in range(len(switches)):
            # Read the specified ADC channel using the previously set gain value.
            switch_states[i] = switches[i].input(pins[i])

        if ((switch_states[0] or switch_states[1] or switch_states[2]) and  # A closed switch in the first group
                (switch_states[3] or switch_states[4] or switch_states[5]) and  # A closed switch in the second group
                (switch_states[6] or switch_states[7] or switch_states[8])):  # A closed switch in the third group
            # The circuit is complete and we should calculate the impedance
            for i in range(0, 3):
                if switch_states[i]:
                    resistance[0] += 1 / RESISTOR_VALUES[i]  # calculate the resistance of the first group
            for i in range(3, 6):
                if switch_states[i]:
                    resistance[1] += 1 / RESISTOR_VALUES[i]  # calculate the resistance of the second group
            for i in range(6, 9):
                if switch_states[i]:
                    resistance[2] += 1 / RESISTOR_VALUES[i]  # calculate the resistance of the third group
            # Display the resistance values
            for i in range(len(resistance)):
                resistance[i] = int(1 / resistance[i])
            print(resistance)
            print(sum(resistance))
            parallel_group_display0.write_int(resistance[0])
            parallel_group_display1.write_int(resistance[1])
            parallel_group_display2.write_int(resistance[2])
            actual_display.write_int(sum(resistance))
        else:
            # The circuit is NOT complete and we should print the open loop values to the displays
            actual_display.write_int(open_loop_val)
            parallel_group_display0.write_int(open_loop_val)
            parallel_group_display1.write_int(open_loop_val)
            parallel_group_display2.write_int(open_loop_val)

        # Print the ADC values.
        # print('| {0:>1} | {1:>1} | {2:>1} | {3:>6} | {4:>1} | {5:<6} | {6:>1} | {7:>1} | {8:>1} |'.format(*switch_states))
        # Pause for half a second.
        time.sleep(0.5)

if __name__ == '__main__':
    main()

"""
    # ------------------------------------ERROR-PROPAGATION----------------------------------
    # We're looking for the error propagation in the combination calculation.
    # We start by finding the partial derivatives of the equivalent resistance equation with respect to each resistor.

    denominator = [0 for i in range(number_of_resistors)]
    numerator = [0 for i in range(number_of_resistors)]

    for i in range(number_of_resistors):
        if 0 <= i < 3:
            denominator[i] = (resistor_values[0] * resistor_values[1] +
                              resistor_values[0] * resistor_values[2] +
                              resistor_values[1] * resistor_values[2]) ^ 2
            if i == 0:
                numerator[i] = resistor_values[1] ^ 2 * resistor_values[2] ^ 2
            elif i == 1:
                numerator[i] = resistor_values[0] ^ 2 * resistor_values[2] ^ 2
            elif i == 2:
                numerator[i] = resistor_values[0] ^ 2 * resistor_values[1] ^ 2

        elif 3 <= i < 6:
            denominator[i] = (resistor_values[3] * resistor_values[4] +
                              resistor_values[3] * resistor_values[5] +
                              resistor_values[4] * resistor_values[5]) ^ 2
            if i == 3:
                numerator[i] = resistor_values[4] ^ 2 * resistor_values[5] ^ 2
            elif i == 4:
                numerator[i] = resistor_values[3] ^ 2 * resistor_values[5] ^ 2
            elif i == 5:
                numerator[i] = resistor_values[3] ^ 2 * resistor_values[4] ^ 2

        elif 6 <= i < 9:
            denominator[i] = (resistor_values[6] * resistor_values[7] +
                              resistor_values[6] * resistor_values[8] +
                              resistor_values[7] * resistor_values[8]) ^ 2
            if i == 6:
                numerator[i] = resistor_values[7] ^ 2 * resistor_values[8] ^ 2
            elif i == 7:
                numerator[i] = resistor_values[6] ^ 2 * resistor_values[8] ^ 2
            elif i == 8:
                numerator[i] = resistor_values[6] ^ 2 * resistor_values[7] ^ 2

    derivative = [0 for i in range(number_of_resistors)]
    for i in range(number_of_resistors):
        derivative[i] = numerator[i] / denominator[i]
    print(derivative)
    print(equivalent_impedance_index_combinations[0:8])
    print(equivalent_impedance[0:8])

# was working on the error propagation. I have the derivatives calculated. now we need to create the square root term
# including only those terms used and the resistors connected to the circuit.
"""