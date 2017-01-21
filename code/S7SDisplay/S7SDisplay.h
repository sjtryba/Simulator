/*
	S7SDisplay.h - Library for Sparkfun's seven segment serial display
	Author: Spencer Tryba
	2017-01-12
	License
*/

#ifndef S7SDisplay_h
#define S7SDisplay_h
#include "Arduino.h"
#include "string.h"

class S7SDisplay{
	public:
		S7SDisplay(void);
		void SetAddress(byte address);
		boolean ValidateDigit(byte command);
		void WriteByte(byte value);
		void FactoryReset();
		void ClearDisplay();
		void SetBrightness(int percent);
		void SetCursorPosition(int position);
		void WriteDigit(byte digit);
		void WriteDigitToPosition(int position, byte digit);
		void WriteInt(int value, String fillChar);
	private:
		byte _address;
};

class DoubleDisplay{
	public:
		DoubleDisplay(byte leftAddress, byte rightAddress);
		void WriteInt(long value);
		void ClearDisplay();
	private:
		byte _leftAddress;
		byte _rightAddress;
		S7SDisplay leftDisplay;
		S7SDisplay rightDisplay;
		//leftDisplay(byte leftAddress);
		//rightDisplay(byte rightAddress);
};
#endif