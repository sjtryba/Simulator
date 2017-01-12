# from Adafruit_I2C import Adafruit_I2C
# import seven_segment_i2c
# import time
import rocket


def main():
    # i2c = seven_segment_i2c.SevenSegmentDisplay(1, 0x71)
    # i2c = Adafruit_I2C(0x71)
    sls = rocket.load_rocket()
    rocket.pre_launch(sls)

if __name__ == '__main__':
    main()
