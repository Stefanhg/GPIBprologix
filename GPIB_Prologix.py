import serial
import sys

currentGPIB = None

class ResourceManager():
	GPIBcom = None
	
	def __init__(self, comport, serialBaud=115200, serialTimeout=1, serialParity='N'):
		global GPIBcom
		

		try:
			GPIBcom = serial.Serial(comport, baudrate=serialBaud, bytesize=8, parity=serialParity, stopbits=1, timeout=serialTimeout, xonxoff=0, rtscts=0)
		except serial.SerialException:
			print("Cannot connect to Serial port. Port already in use")
			sys.exit(1)

	class open_resource():
		resourceAddress = None
		
		def selectAddress(self, address):
			global currentGPIB
			# Sends address to USB-GPIB adapter
			GPIBcom.write(("++addr " + str(address) + "\n").encode())
			currentGPIB = address

		def __init__(self, address):
			self.resourceAddress = address
			self.selectAddress(address)
		
		def write(self, data):
			if(currentGPIB != self.resourceAddress):
				self.selectAddress(self.resourceAddress)
			GPIBcom.write(str(data + "\n").encode())
		
		def read(self):
			GPIBcom.write(b"++read eoi\n")
			data = GPIBcom.readline()
			return(data.decode('utf-8').rstrip())

		def query(self, data):
			self.write(data)
			data = self.read()
			return(data)
	
