from Homey import Homey
import sys
import re
import time

do = Homey("192.168.178.100","1883","mqtt",False,"rstdelange","pasw0rd")

print("sleeping")
i=0
while i == 0:
    time.sleep(2)
    #print(do.findid("light","kitchen", 1))
    #print(do.findcmd("off", "on", "20"))
    #print(do.switch("on", "light", "kitchen", "turn")) #switch(state,what,where,action)
    #print(do.hadapter.getdevices())
    print(do.get("Humidity",""))
    i=1
