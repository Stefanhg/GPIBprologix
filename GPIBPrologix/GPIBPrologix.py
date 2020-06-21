import serial
import sys

# Global variable used to store which GPIB is under control currently
currentGPIB = None

class ResourceManager():
	GPIBcom = None
	readTimeout = None

	def __init__(self, comport, readTimeout=1000, serialBaud=115200, serialTimeout=1):
		global GPIBcom
		try:
			GPIBcom = serial.Serial(comport, baudrate=serialBaud, timeout=serialTimeout )
			GPIBcom.write(("++read_tmo_ms " + str(readTimeout) + "\n").encode())
		except serial.SerialException:
			print("Cannot connect to Serial port. Port already in use")
			sys.exit(1)

	def close(self):
		GPIBcom.close()
		
	class open_resource():
		# This address is the instance's address
		resourceAddress = None

		def selectAddress(self, address):
			global currentGPIB
			GPIBcom.write(("++addr " + str(address) + "\n").encode())
			currentGPIB = address

		def __init__(self, address):
			self.resourceAddress = address
			self.selectAddress(address)

		def write(self, data):
			if(currentGPIB != self.resourceAddress):
				self.selectAddress(self.resourceAddress)
			GPIBcom.write((data + "\n").encode())

		def read(self):
			GPIBcom.write(b"++read eoi\n")
			data = GPIBcom.readline().decode('utf-8').rstrip()
			return(data)

		def query(self, data):
			self.write(data)
			data = self.read()
			return(data)