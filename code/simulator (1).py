import rocket
import time


def main():
    sls = rocket.load_rocket()  # create rocket object
    rocket.pre_launch(sls)

if __name__ == '__main__':
    main()
"""
load rocket

main loop

    get current time
    calculate delta t
    calculate new mass from throttle input and flow rate data
        map flow rate to throttle control
        new mass = old mass - flow rate * delta t
    calculate change in flight path angle, velocity, and altitude with a root finding function

"""

# stage1 separation

# Set the initial conditions of stage 2 to the final conditions of stage 1
# stage2.fuel.mass = stage1.fuel.mass
# stage2.fuel.pressure = stage1.fuel.pressure
# stage2.fuel.flow_rate = stage1.fuel.flow_rate

# stage2.oxidizer.mass = stage1.oxidizer.mass
# stage2.oxidizer.pressure = stage1.oxidizer.pressure
# stage2.oxidizer.flow_rate = stage1.oxidizer.flow_rate
