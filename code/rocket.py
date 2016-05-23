import time
import functools
import numpy
import math
# from scipy.optimize import fsolve
import atmospheric_model as atmo
import touch_pot
import console
from random import randint

EARTH_RADIUS = 6.371 * 10 ** 6  # Radius of Earth in meters


class Rocket:
    def __init__(self):
        # -------------------VARIABLES-------------------
        self.flight_path_angle = 0  # [degrees]
        self.altitude = 0  # [m]
        self.velocity = 0  # [m/s]


class Stage:
    def __init__(self):
        # -------------------CONSTANTS-------------------
        self.THRUST_SEA = 0  # [N]
        self.THRUST_VAC = 0  # [N]

        self.ISP_SEA = 0  # [s]
        self.ISP_VAC = 0  # [s]

        self.MIXTURE = 0  # [ ]
        self.PROPELLANT_MASS = 0  # [kg]

        self.DEAD_MASS = 0  # [kg]
        self.PAYLOAD_MASS = 0  # [kg]


class Propellant:
    # This is a class for the fuels and oxidizers
    def __init__(self):
        # -------------------CONSTANTS-------------------
        self.MASS_MAX = 0  # [kg]
        self.PRESSURE_RANGE = [0, 0]  # [kg]
        self.FLOW_RATE_MAX = 0  # [kg/s]
        self.NAME = ""

        # -------------------VARIABLES-------------------
        self.mass = 0  # [kg]
        self.pressure = 0  # [kg]
        self.flow_rate = 0  # [kg/s]


def load_rocket():
    """
    This function creates a rocket object including stages and propellants. The rocket is modeled after NASA's SLS B1
    :return: Returns a rocket object loaded with stages and propellants.
    """
    # ---------------------ROCKET-INITIATION---------------------
    # NASA's Space Launch System
    rocket = Rocket()
    rocket.flight_path_angle = 89.95  # [degrees]
    rocket.altitude = 0  # [m]
    rocket.velocity = 0  # [m/s]
    rocket.current_stage = "stage1"

    # ---------------------STAGE-4-INITIATION---------------------
    # Orion capsule and service module with AJ10 engine
    rocket.stage4 = Stage()
    rocket.stage4.THRUST_VAC = 25700  # [N]
    rocket.stage4.ISP_VAC = 319  # [s]
    rocket.stage4.MIXTURE = 1.9  # [ ]
    rocket.stage4.PROPELLANT_MASS = 9276  # [kg]
    rocket.stage4.DEAD_MASS = 6185  # [kg]
    rocket.stage4.PAYLOAD_MASS = 10387  # [kg]
    rocket.stage4.DIAMETER = 5.03  # [m]
    rocket.stage4.AREA = 3.14 * rocket.stage4.DIAMETER ** 2
    rocket.stage4.DRAG_COEFFICIENT = 0.5  # Assuming a constant drag coefficient

    rocket.stage4.fuel = Propellant()
    rocket.stage4.fuel.NAME = "MMH"
    rocket.stage4.fuel.MASS_MAX = int(rocket.stage4.PROPELLANT_MASS / (rocket.stage4.MIXTURE + 1))  # [kg]
    rocket.stage4.fuel.PRESSURE_RANGE = [1613000, 1958000]  # [Pa]
    rocket.stage4.fuel.FLOW_RATE_MAX = rocket.stage4.THRUST_VAC / rocket.stage4.ISP_VAC / (
        rocket.stage4.MIXTURE + 1)  # [kg/s]
    rocket.stage4.fuel.mass = rocket.stage4.fuel.MASS_MAX  # [kg]
    rocket.stage4.fuel.pressure = numpy.mean(rocket.stage4.fuel.PRESSURE_RANGE)  # [Pa]

    rocket.stage4.oxidizer = Propellant()
    rocket.stage4.oxidizer.NAME = "MON"
    rocket.stage4.oxidizer.MASS_MAX = int(rocket.stage4.PROPELLANT_MASS * rocket.stage4.MIXTURE / (
        rocket.stage4.MIXTURE + 1))  # [kg]
    rocket.stage4.oxidizer.PRESSURE_RANGE = [1613000, 1958000]  # [Pa]
    rocket.stage4.oxidizer.FLOW_RATE_MAX = int(rocket.stage4.THRUST_VAC / rocket.stage4.ISP_VAC * rocket.stage4.MIXTURE / (
        rocket.stage4.MIXTURE + 1))  # [kg/s]
    rocket.stage4.oxidizer.mass = rocket.stage4.oxidizer.MASS_MAX  # [kg]
    rocket.stage4.oxidizer.pressure = numpy.mean(rocket.stage4.oxidizer.PRESSURE_RANGE)  # [Pa]

    rocket.stage4.total_mass = rocket.stage4.DEAD_MASS + rocket.stage4.PROPELLANT_MASS + rocket.stage4.PAYLOAD_MASS

    # ---------------------STAGE-3-INITIATION---------------------
    # Exploration stage with 4 RL10 engines

    rocket.stage3 = Stage()
    rocket.stage3.THRUST_VAC = 440000  # [N]
    rocket.stage3.ISP_VAC = 450  # [s]
    rocket.stage3.MIXTURE = 5.5  # [ ]
    rocket.stage3.PROPELLANT_MASS = 129000  # [kg]
    rocket.stage3.DEAD_MASS = int((rocket.stage3.PROPELLANT_MASS + 4 * 277) * 1.1)  # [kg] (an approx 277 = engine mass)
    rocket.stage3.PAYLOAD_MASS = rocket.stage4.DEAD_MASS + rocket.stage4.PAYLOAD_MASS + rocket.stage4.PROPELLANT_MASS
    # [kg]
    rocket.stage3.DIAMETER = 8.4  # [m]
    rocket.stage3.AREA = 3.14 * rocket.stage3.DIAMETER ** 2
    rocket.stage3.DRAG_COEFFICIENT = 0.5  # Assuming a constant drag coefficient

    rocket.stage3.fuel = Propellant()
    rocket.stage3.fuel.NAME = "LH2"
    rocket.stage3.fuel.MAS_MAX = int(rocket.stage3.PROPELLANT_MASS / (rocket.stage3.MIXTURE + 1))  # [kg]
    rocket.stage3.fuel.PRESSURE_RANGE = [220000, 230000]  # [Pa]
    rocket.stage3.fuel.FLOW_RATE_MAX = int(rocket.stage3.THRUST_VAC / rocket.stage3.ISP_VAC / (
        rocket.stage3.MIXTURE + 1))  # [kg/s]
    rocket.stage3.fuel.mass = rocket.stage3.fuel.MASS_MAX  # [kg]
    rocket.stage3.fuel.pressure = numpy.mean(rocket.stage3.fuel.PRESSURE_RANGE)  # [Pa]

    rocket.stage3.oxidizer = Propellant()
    rocket.stage3.oxidizer.NAME = "LOX"
    rocket.stage3.oxidizer.MASS_MAX = int(rocket.stage3.PROPELLANT_MASS * rocket.stage3.MIXTURE / (
        rocket.stage3.MIXTURE + 1))  # [kg]
    rocket.stage3.oxidizer.PRESSURE_RANGE = [140000, 150000]  # [Pa]
    rocket.stage3.oxidizer.FLOW_RATE_MAX = int(rocket.stage3.THRUST_VAC / rocket.stage3.ISP_VAC * rocket.stage3.MIXTURE / (
        rocket.stage3.MIXTURE + 1))  # [kg/s]
    rocket.stage3.oxidizer.mass = rocket.stage3.oxidizer.MASS_MAX  # [kg]
    rocket.stage3.oxidizer.pressure = numpy.mean(rocket.stage3.oxidizer.PRESSURE_RANGE)  # [Pa]

    rocket.stage3.total_mass = rocket.stage3.DEAD_MASS + rocket.stage3.PROPELLANT_MASS + rocket.stage3.PAYLOAD_MASS

    # ---------------------STAGE-2-INITIATION---------------------
    # Core stage with 4 RS-25 engines
    rocket.stage2 = Stage()
    rocket.stage2.THRUST_SEA = 4 * 1860000  # [N]
    rocket.stage2.THRUST_VAC = 4 * 2279000  # [N]
    rocket.stage2.ISP_SEA = 366  # [s]
    rocket.stage2.ISP_VAC = 452.3  # [s]
    rocket.stage2.MIXTURE = 6.0  # [ ]
    rocket.stage2.PROPELLANT_MASS = 894182  # [kg]
    rocket.stage2.DEAD_MASS = 85270  # [kg]
    rocket.stage2.PAYLOAD_MASS = rocket.stage3.DEAD_MASS + rocket.stage3.PAYLOAD_MASS + rocket.stage3.PROPELLANT_MASS
    # [kg]
    rocket.stage2.DIAMETER = 8.4  # [m]
    rocket.stage2.AREA = 3.14 * rocket.stage2.DIAMETER ** 2
    rocket.stage2.DRAG_COEFFICIENT = 0.5  # Assuming a constant drag coefficient

    rocket.stage2.fuel = Propellant()
    rocket.stage2.fuel.NAME = "LH2"
    rocket.stage2.fuel.MASS_MAX = int(rocket.stage2.PROPELLANT_MASS / (rocket.stage2.MIXTURE + 1))  # [kg]
    rocket.stage2.fuel.PRESSURE_RANGE = [220000, 230000]  # [Pa]
    rocket.stage2.fuel.FLOW_RATE_MAX = int(rocket.stage2.THRUST_SEA / rocket.stage2.ISP_SEA / (
        rocket.stage2.MIXTURE + 1))  # [kg/s]
    rocket.stage2.fuel.mass = rocket.stage2.fuel.MASS_MAX  # [kg]
    rocket.stage2.fuel.pressure = numpy.mean(rocket.stage2.fuel.PRESSURE_RANGE)  # [Pa]

    rocket.stage2.oxidizer = Propellant()
    rocket.stage2.oxidizer.NAME = "LOX"
    rocket.stage2.oxidizer.MASS_MAX = int(rocket.stage2.PROPELLANT_MASS * rocket.stage2.MIXTURE / (
        rocket.stage2.MIXTURE + 1))  # [kg]
    rocket.stage2.oxidizer.PRESSURE_RANGE = [140000, 150000]  # [Pa]
    rocket.stage2.oxidizer.FLOW_RATE_MAX = int(rocket.stage2.THRUST_SEA / rocket.stage2.ISP_SEA * rocket.stage2.MIXTURE / (
        rocket.stage2.MIXTURE + 1))  # [kg/s]
    rocket.stage2.oxidizer.mass = rocket.stage2.oxidizer.MASS_MAX  # [kg]
    rocket.stage2.oxidizer.pressure = numpy.mean(rocket.stage2.oxidizer.PRESSURE_RANGE)  # [Pa]

    rocket.stage2.total_mass = rocket.stage2.DEAD_MASS + rocket.stage2.PROPELLANT_MASS + rocket.stage2.PAYLOAD_MASS

    # ---------------------STAGE-1-INITIATION---------------------
    # Core stage with 4 RS-25 engines and 2 5-segment SRBs
    rocket.stage1 = Stage()
    rocket.stage1.THRUST_SEA = 32000000 + rocket.stage2.THRUST_SEA  # [N]
    rocket.stage1.THRUST_VAC = rocket.stage2.THRUST_VAC  # [N]
    rocket.stage1.ISP_SEA = 269  # [s]
    rocket.stage1.ISP_VAC = rocket.stage2.ISP_VAC  # [s]
    rocket.stage1.MIXTURE = 6.0  # [ ]
    rocket.stage1.PROPELLANT_MASS = 894182  # [kg]
    rocket.stage1.DEAD_MASS = 227500  # [kg]
    rocket.stage1.PAYLOAD_MASS = rocket.stage3.total_mass
    # [kg]
    rocket.stage1.DIAMETER = 9.9  # [m]
    rocket.stage1.AREA = 3.14 * rocket.stage1.DIAMETER ** 2
    rocket.stage1.DRAG_COEFFICIENT = 0.5  # Assuming a constant drag coefficient

    rocket.stage1.fuel = Propellant()
    rocket.stage1.fuel.NAME = "LH2"
    rocket.stage1.fuel.MASS_MAX = rocket.stage2.fuel.MASS_MAX  # [kg]
    rocket.stage1.fuel.PRESSURE_RANGE = rocket.stage2.fuel.PRESSURE_RANGE  # [Pa]
    rocket.stage1.fuel.FLOW_RATE_MAX = rocket.stage2.fuel.FLOW_RATE_MAX  # [kg/s]
    rocket.stage1.fuel.mass = 0  # [kg]
    rocket.stage1.fuel.pressure = 0  # [Pa]

    rocket.stage1.oxidizer = Propellant()
    rocket.stage1.oxidizer.NAME = "LOX"
    rocket.stage1.oxidizer.MASS_MAX = rocket.stage2.oxidizer.MASS_MAX  # [kg]
    rocket.stage1.oxidizer.PRESSURE_RANGE = rocket.stage2.oxidizer.PRESSURE_RANGE  # [Pa]
    rocket.stage1.oxidizer.FLOW_RATE_MAX = rocket.stage2.oxidizer.FLOW_RATE_MAX  # [kg/s]
    rocket.stage1.oxidizer.mass = 0  # [kg]
    rocket.stage1.oxidizer.pressure = 0  # [Pa]

    rocket.stage1.srb = Propellant()
    rocket.stage1.srb.NAME = "srb"
    rocket.stage1.srb.MASS_MAX = 1250000  # [kg]
    rocket.stage1.srb.FLOW_RATE_MAX = int(rocket.stage1.THRUST_SEA / rocket.stage1.ISP_SEA)  # [kg/s]
    rocket.stage1.srb.mass = rocket.stage1.srb.MASS_MAX  # [kg]

    rocket.stage1.total_mass = rocket.stage1.DEAD_MASS + rocket.stage1.PAYLOAD_MASS + rocket.stage1.PROPELLANT_MASS

    # Build a list containing all the stages in the rocket
    rocket.stages = [a for a in dir(rocket) if a.startswith('stage')]

    rocket.throttle = touch_pot.TouchPot(1, 0x08)

    return rocket


def pre_launch(rocket):
    """
    This function will 'fill' the rocket with fuel and is meant to be called shortly after the system boots.
    :param control: An object containing all of the display and control objects
    :param rocket: An input rocket containing stage classes and fuel sub-classes.
    :return: Nothing is returned at this time
    """
    # Create the displays for the fuel and oxidizer, this should be moved elsewhere and imported as an object
    # fuel_display = console.PropellantDisplay(0x04, 0x05)
    oxidizer_display = console.PropellantDisplay(0x70, 0x71)

    # The oxidizer always has a larger mass than the fuel so we will fill until the oxidizer is full
    while rocket.stage1.oxidizer.mass < rocket.stage1.oxidizer.MASS_MAX:
        rocket.stage1.oxidizer.mass += randint(175, 200)  # Add a random amount of oxidizer to the tank
        rocket.stage1.fuel.mass += randint(175, 200)  # Add a random amount of fuel to the tank

        # Check that we didn't over fill the tanks and set them to full if we do.
        if rocket.stage1.oxidizer.mass > rocket.stage1.oxidizer.MASS_MAX:
            rocket.stage1.oxidizer.mass = rocket.stage1.oxidizer.MASS_MAX
        if rocket.stage1.fuel.mass > rocket.stage1.fuel.MASS_MAX:
            rocket.stage1.fuel.mass = rocket.stage1.fuel.MASS_MAX

        # Display the oxidizer and fuel masses
        oxidizer_display.display(rocket.stage1.oxidizer.mass)
        # fuel_display.display(rocket.stage1.fuel.mass)


def update(rocket):
    """
    This function updates the rocket's altitude, velocity and flight path angle (fpa).
    We take the previous values of altitude, velocity and fpa and use them along with a delta t as inputs for a root
    solving function to find new values of altitude, velocity and fpa.
    :param rocket: An input rocket containing stage classes and fuel sub-classes.
    :return: Returns the rocket object with updated altitude, velocity and fpa
    """


def functions(rocket, variables, delta_time):
    """
    This function defines the functions that characterize the rockets altitude, velocity and flight path angle (fpa).
    :param delta_time: A vector of times time[0] = t0, time[1] = t1
    :param rocket: An input rocket containing stage classes and fuel sub-classes.
    :param variables: Variables we are trying to solve for
    :return: Returns functions that characterize the variables. In a format that works with a root solving algorithm.
    0 = ...
    """

    altitude = variables[0]
    velocity = variables[1]
    flight_path_angle = variables[2]

    altitude_old = rocket.altitude
    velocity_old = rocket.velocity
    flight_path_angle_old = rocket.flight_path_angle

    time_old = delta_time[0]
    time_new = delta_time[1]

    area = rocket.current_stage + ".AREA"
    drag_coefficient = rocket.current_stage + ".DRAG_COEFFICIENT"
    mass = rocket.current_stage + ".total_mass"

    f = numpy.zeros(3)

    f[0] = -(atmo.gravity(altitude) - velocity ** 2 / (EARTH_RADIUS + altitude)) * math.cos(flight_path_angle)\
           - velocity * (flight_path_angle - flight_path_angle_old) / (time_new - time_old)

    f[1] = (time_new - time_old) * velocity * math.sin(flight_path_angle) + altitude - altitude_old

    f[2] = (time_new - time_old) * ((thrust(rocket) - (0.5 * atmo.density(altitude) * velocity ** 2 *
           getattr_nest(rocket, area) * getattr_nest(rocket, drag_coefficient))) / getattr_nest(rocket, mass) \
           - atmo.gravity(altitude) * math.sin(flight_path_angle)) + velocity_old - velocity


def thrust(rocket):
    """
    This function gets the value from the touch pot throttle and maps it to the rocket thrust limits.
    :param rocket: An input rocket containing stage classes and fuel sub-classes.
    :return: Returns a thrust in Newtons
    """
    current_value = rocket.throttle.get_current_value()

    if rocket.altitude > 25000:  # If the rocket is in space use the vacuum max thrust value
        max_thrust = rocket.current_stage + ".THRUST_VAC"
    else:  # If the rocket is still in the atmosphere use the sea-level max thrust value
        max_thrust = rocket.current_stage + ".THRUST_SEA"

    min_thrust = 0

    return translate(current_value, [rocket.throttle.MIN_VALUE, rocket.throttle.MAX_VALUE],
                     [min_thrust, getattr_nest(rocket, max_thrust)])


def translate(value, range1, range2):
    """
    This function maps an input value from range1 to range2
    :param value: The input value to be mapped
    :param range1: The range of the original value
    :param range2: The range of the target value
    :return: Returns value mapped to range2
    """
    span1 = range1[1] - range1[0]
    span2 = range2[1] - range2[0]

    normalized_value = (value - range1[0]) / float(span1)

    return range2[0] + (normalized_value * span2)


def setattr_nest(obj, attr, val):
    """
    This function is an adaptation of the setattr function. This one allows attributes of nested classes to be adjusted.
    :param obj: Top tear class
    :param attr: Lower tear class
    :param val: Value that is to be set to ojb.attr
    :return:
    """
    pre, _, post = attr.rpartition('.')
    return setattr(getattr_nest(obj, pre) if pre else obj, post, val)


def getattr_nest(obj, attr):
    """
    This function is an adaptation of the getattr function. This one allows attributes of nested classes to be recovered
    :param obj: Top tear class
    :param attr: Lower tear class
    :return: returns obj.attr
    """
    return functools.reduce(getattr, [obj] + attr.split('.'))
