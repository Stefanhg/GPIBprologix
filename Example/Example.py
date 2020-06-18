import GPIB_Prologix
# 
GPIB = GPIB_Prologix.ResourceManager("COM45")

# Creates a path to use GPIB 1 and GPIB 2 
inst1 = GPIB.open_resource(1)
inst2 = GPIB.open_resource(2)

# Gets Identifcation of GPIB 1 and GPIB 2
print(inst1.query("*IDN?"))
print(inst2.query("*IDN?"))