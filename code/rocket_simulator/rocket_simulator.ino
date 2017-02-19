/*
 * Controlls the hardware and logic behind the rocket simulator.
 * 
 * Author: Spencer Tryba
 * Date: 2017-02-18
 * https://github.com/sjtryba/simulator
 */

/*
 * ===================================
 * =============LIBRARIES=============
 * ===================================
 */
# include <Wire.h>        // I2C communications
# include <S7SDisplay.h>  // serial 7 segment display object handling (I made this library!)
# include <Servo.h>       // servo object handling

/*
 * =================================
 * =============OBJECTS=============
 * =================================
 */
Servo att_ind_bottom; // create a servo object
Servo att_ind_left;   // create a servo object
Servo att_ind_right;  // create a servo object

/*
 * ===================================
 * =============CONSTANTS=============
 * ===================================
 */
const int ANALOG_MIN = 0;     // min value for analogRead()
const int ANALOG_MAX = 1023;  // max value for analogRead()

const int W_MIN = 68;      // min angular velocity of the servos. 0 actually is full speed in the 
                          // negative direction, but the write() method handles that for us.
const int W_MAX = 112;     // max angular velocity of the servos. Calculated by multiplying the normal
                          // max of 180 by 0.24. 0.24 is used because of the 120 degree orientation of
                          // the servos.

const int JOY_X_PIN = A0;  // analog pin connected to the X axis of the joystick
const int JOY_Y_PIN = A1;  // analog pin connected to the Y axis of the joystick
const int JOY_Z_PIN = A2;  // analog pin connected to the Z axis of the joystick

/*
 * ===================================
 * =============VARIABLES=============
 * ===================================
 */
int joy_x_val;  // joystick X value
int joy_y_val;  // joystick X value
int joy_z_val;  // joystick X value

int att_ind_bottom_velocity;  // angular velocity of the bottom servo
int att_ind_left_velocity;    // angular velocity of the left servo
int att_ind_right_velocity;   // angular velocity of the right servo

/*
 * ===============================
 * =============SETUP=============
 * ===============================
 */
void setup() {
  Serial.begin(9600);
  Wire.begin(); // initialize hardware I2C pins
  
  att_ind_bottom.attach(9); // attach the servo on pin 9 to the servo object
  att_ind_left.attach(10);  // attach the servo on pin 10 to the servo object
  att_ind_right.attach(11); // attach the servo on pin 11 to the servo object

}

/*
 * ==============================
 * =============LOOP=============
 * ==============================
 */
void loop() {
  joy_x_val = analogRead(JOY_X_PIN);  // reads the value of the joysick's X axis potentiometer (value between 0 and 1023)
  joy_y_val = analogRead(JOY_Y_PIN);  // reads the value of the joysick's Y axis potentiometer (value between 0 and 1023)
  joy_z_val = analogRead(JOY_Z_PIN);  // reads the value of the joysick's Z axis potentiometer (value between 0 and 1023)
     
  joy_x_val = map(joy_x_val, ANALOG_MIN, ANALOG_MAX, W_MIN, W_MAX);  // scale the X value to use it with the servo (value between 0 and 180)
  joy_y_val = map(joy_y_val, ANALOG_MIN, ANALOG_MAX, W_MIN, W_MAX);  // scale the Y value to use it with the servo (value between 0 and 180)
  joy_z_val = map(joy_z_val, ANALOG_MIN, 500, W_MIN, W_MAX);  // scale the Z value to use it with the servo (value between 0 and 180)

  att_ind_bottom_velocity = joy_x_val;  // combine the X, Y, and Z values from the joystick into one velocty for the bottom servo
  att_ind_left_velocity = -1.15 * joy_x_val + 2 * joy_y_val + 14;  // combine the X, Y, and Z values from the joystick into one velocty for the left servo
  att_ind_right_velocity = -1.15 * joy_x_val - 2 * joy_y_val + 372;  // combine the X, Y, and Z values from the joystick into one velocty for the right servo
  
  turnServo(att_ind_bottom, att_ind_bottom_velocity);
  turnServo(att_ind_left, att_ind_left_velocity);
  turnServo(att_ind_right, att_ind_right_velocity);
  
  //att_ind_bottom.write(att_ind_bottom_velocity);  // set the speed of the servo
  //att_ind_left.write(att_ind_left_velocity);      // set the speed of the servo
  //att_ind_right.write(att_ind_right_velocity);    // set the speed of the servo

  Serial.print(joy_x_val);
  Serial.print("\t");
  Serial.print(joy_y_val);
  Serial.print("\t");
  Serial.print(joy_z_val);
  Serial.print("\t");
  Serial.print(att_ind_bottom_velocity);
  Serial.print("\t");
  Serial.print(att_ind_left_velocity);
  Serial.print("\t");
  Serial.println(att_ind_right_velocity);
  
  delay(15);  // slow the loop down a little
}

 void turnServo(Servo &theServo, int value){
  if(value > 95 || value < 85){
    theServo.write(value);
  }
  else{
    theServo.write(90);
  }
}

