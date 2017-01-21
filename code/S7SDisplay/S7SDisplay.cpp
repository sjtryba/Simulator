/*
	S7SDisplay.pp - Library for Sparkfun's seven segment serial display
	Author: Spencer Tryba
	2017-01-12
	License
*/

#include "Arduino.h"
#include "Wire.h"
#include "String.h"
#include "S7SDisplay.h"

S7SDisplay::S7SDisplay(void){

}

void S7SDisplay::SetAddress(byte address){
	_address = address;
}

bool S7SDisplay::ValidateDigit(byte command){
	/*
	Ensure the digit byte we are given does not
	evaluate to one of the control commands
	*/
	if((command < 0x76) or (command > 0x81))
		return false;
	else
		return true;
}

void S7SDisplay::WriteByte(byte value){
	/*
	Write a byte to the screen
	*/
	Wire.beginTransmission(_address);
	Wire.write(value);
	Wire.endTransmission();
}

void S7SDisplay::FactoryReset(){
	/*
	Restore the display to factory settings
	*/
	WriteByte(0x81);
}

void S7SDisplay::ClearDisplay(){
	/*
	Clear the display
	*/
	WriteByte(0x76);
}

void S7SDisplay::SetBrightness(int percent){
	/*
	Set the brightness level as a percentage of the total brightness
	*/
	if(percent < 0)
		percent = 0;
	if(percent > 100)
		percent = 100;
	
	int val = ((percent / 100.0) * 255);
	
	Wire.beginTransmission(_address);
	Wire.write(0x7A);
	Wire.write(val);
	Wire.endTransmission();
}

void S7SDisplay::SetCursorPosition(int position){
	/*
	Sets tthe cursor position with 0 being the left most write_digit
	and 3 being the right most write_digit
	*/
	if((position >= 0) and (position <= 3)){
		Wire.beginTransmission(_address);
		Wire.write(0x79);
		Wire.write(position);
		Wire.endTransmission();
	}
		
}

void S7SDisplay::WriteDigit(byte digit){
	/*
	Wtires a digit to the display at thre current cursor position.
	Each time the digit is written, the cursor moves one to the right.
	*/
	if(not ValidateDigit(digit))
		WriteByte(digit);
}

void S7SDisplay::WriteDigitToPosition(int position, byte digit){
	/*
	Write a digit to the display at a specific position.
	*/
	SetCursorPosition(position);
	WriteDigit(digit);
}

void S7SDisplay::WriteInt(int value, String fillChar = " "){
	/*
	Write an integer to the display.
	fillChar will padd the number up to four digits.
	Pad occurs on the left.
	*/
	String strValue = String(value);			// Convert the value into a character
	
	int digitsToFill = 4 - strValue.length();	// Calculate how many digits we need to fill
	
	String fillStr = "";
	
	for(int i=0; i<digitsToFill; i++)
		fillStr += fillChar;					// Create the proper length fill string
	
	String writeStr = fillStr + strValue;		// Combine the fill and value to make the final string
	Wire.beginTransmission(_address);
	for(int i = 0; i < 4; i++)
		Wire.write(writeStr[i]);
	Wire.endTransmission();
}

DoubleDisplay::DoubleDisplay(byte leftAddress, byte rightAddress){
	/*
	Double display class, made up of a left and right display.
	*/
	
	_leftAddress = leftAddress;
	_rightAddress = rightAddress;
	
	leftDisplay.SetAddress(leftAddress);
	rightDisplay.SetAddress(rightAddress);
}

void DoubleDisplay::WriteInt(long value){
	/*
	Writes an integer of 8 or less characters to a double display.
	A double display is made up of a left and right display.
	*/
	
	String strValue = String(value);	// Convert the integer to a string
	String fillChar = "0";
	
	//leftDisplay.ClearDisplay();
	//rightDisplay.ClearDisplay();
	// If the string is 4 characters or less, only disply on the right screen
	if(strValue.length() <= 4){
		leftDisplay.ClearDisplay();		// Clear the left screen
		rightDisplay.WriteInt(value);	// Write to the right screen
	}
	
	// If the string is between 4 and 8 characters, split the string
	// and display it across both screens.
	else if(4 < strValue.length() <= 8){
		String left = strValue.substring(0, strValue.length() - 4);	// Left part of the string
		String right = strValue.substring(strValue.length() - 4, strValue.length());	// Right part of the string
		
		leftDisplay.WriteInt(left.toInt());		// Write to the left screen
		rightDisplay.WriteInt(right.toInt(), fillChar);	// Write to the right screen
	}
}

void DoubleDisplay::ClearDisplay(){
		/*
	Clear the display
	*/
	
	leftDisplay.WriteByte(0x76);
	rightDisplay.WriteByte(0x76);
}