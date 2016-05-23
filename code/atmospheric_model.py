import math
GRAVITY = 9.81  # Acceleration due to gravity at Earth's surface [m/s^2]
EARTH_RADIUS = 6.371 * 10 ** 6  # Radius of Earth in meters


def temperature(altitude):
    """
    This function calculates the temperature of Earth's atmosphere for a given altitude.
    :param altitude: Altitude of the desired temperature in meters
    :return: Temperature of Earth's atmosphere in degrees Celsius.
    """
    if altitude > 25000:
        return -131.21 + 0.00299 * altitude
    elif 25000 >= altitude > 11000:
        return -56.46
    elif 11000 >= altitude:
        return 15.04 - 0.00649 * altitude


def pressure(altitude):
    """
    This function calculates the pressure of Earth's atmosphere for a given altitude.
    :param altitude: Altitude of the desired pressure in meters
    :return: Pressure of Earth's atmosphere in kPa.
    """
    if altitude > 25000:
        return 2.488 * ((temperature(altitude) + 273.1) / 216.6) ** -11.388
    elif 25000 >= altitude > 11000:
        return 22.65 * math.exp(1.73 - 0.000157 * altitude)
    elif 11000 >= altitude:
        return 101.29 * ((temperature(altitude) + 273.1) / 288.08) ** 5.256


def density(altitude):
    """
    This function calculates the density of Earth's atmosphere for a given altitude.
    :param altitude: Altitude of the desired density in meters
    :return: Density of Earth's atmosphere in kg/m^3.
    """
    return pressure(altitude) / (0.2869 * (temperature(altitude) + 273.1))


def gravity(altitude):
    """
    This function calculates the acceleration due to gravity at a given altitude.
    :param altitude: Altitude of the desired acceleration in meters
    :return: Acceleration due to gravity in m/s^2.
    """
    return GRAVITY / (1 + altitude / EARTH_RADIUS) ** 2
