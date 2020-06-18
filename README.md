# GPIBprologix
Very simple GPIB driver for Prologix USB-GPIB adapter

I made this Library to support a Chinese copy of a Prologix USB-GPIB adapter i bought that was made to support Prologix.

Current limitations:
- Only support for a single device connected ( Trying to access other instruments will cause it to give a error)
* Solution: Some sort of global variable telling the Library which GPIB currently is selected using ++addr (x)
