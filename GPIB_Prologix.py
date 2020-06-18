import serial
import sys

class GPIBprologix():
	GPIBcom = None
	def __init__(self, comport, address, serialBaud=115200, serialTimeout=1, serialParity='N'):
			global GPIBcom
			try:
				GPIBcom = serial.Serial(comport, baudrate=serialBaud, bytesize=8, parity=serialParity, stopbits=1, timeout=serialTimeout, xonxoff=0, rtscts=0)
				# Sends address to USB-GPIB adapter
				GPIBcom.write(("++addr " + str(address) + "\n").encode())
			except serial.SerialException:
				print("Cannot connect to Serial port. Port already in use")
				sys.exit(1)
	def write(self, data):
		GPIBcom.write(str(data + "\n").encode())
	
	def read(self):
		GPIBcom.write(b"++read eoi\n")
		data = GPIBcom.readline()
		return(data.decode('utf-8').rstrip())

	def query(self, data):
		self.write(data)
		data = self.read()
		return(data)
