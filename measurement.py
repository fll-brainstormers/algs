# LEGO typestandard slot:9 autostart
from spike import PrimeHub, Motor, MotorPair, ColorSensor
from spike.control import wait_for_seconds
from hub import battery

# THE LIBRARY FOR THE BRAIN BOT 2.0

# Create your objects here.
hub = PrimeHub()

# le hub avec accès a des api plus bas niveau
import hub as hub2
measure_motor = Motor('C')
def measure_degrees():
    measure_motor.set_degrees_counted(0)
    while True:
        print('degrees:'+ str(measure_motor.get_degrees_counted()))
#13
measure_degrees()