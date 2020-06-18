import GPIB_Prologix


GPIB = GPIB_Prologix.GPIBprologix("COM45", 2)
print(GPIB.query("*IDN?"))
print(GPIB.query("READ?"))
