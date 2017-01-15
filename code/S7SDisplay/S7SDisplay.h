/*
	SerialSevenSegmentDisplay.h - Library for Sparkfun's seven segment serial display
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
		S7SDisplay(byte address);
		boolean ValidateDigit(byte command);
		void WriteByte(byte value);
		void FactoryReset();
		void ClearDisplay();
		void SetBrightness(int percent);
		void SetCursorPosition(int position);
		void WriteDigit(byte digit);
		void WriteDigitToPosition(int position, byte digit);
		void WriteInt(int value);
	private:
		byte _address;
};

#endif