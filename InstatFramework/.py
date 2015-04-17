import datetime
import sys
every_list = []
log_file = open('instatLog.txt', 'a')

from Temperature import *

from r_pi import Fake_ThermoStat
myThermoStat = Fake_ThermoStat.Fake_ThermoStat()   
print "Welcome to instat \n==================== "

try:
    a = ('NUM', 1.0)
    
    while 1:
        for e in every_list:
            if eval(e['condition'] + "()"):
                eval(e['func']+ "()")
        
except IndexError:
    sys.stderr.write("ERROR: Nothing lives at that index.\n")
    sys.exit()
except TypeError:
    sys.stderr.write("ERROR: You seem to be using the wrong type for something.\n")
    sys.exit()
except KeyboardInterrupt:
    sys.stderr.write("\nThank you for using CoZy!\n")
    sys.exit()
except:
    sys.stderr.write("ERROR: Hmmm...that's odd. I don't quite know what went wrong.\n")
    sys.exit()
