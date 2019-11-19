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
    #print(do.switch("on", "light", "table", "set")) #switch(state,what,where,action)
    #print(do.hadapter.getdevices())
    print(do.get("Humidity",""))
    """""
    state = "20"
    what = "light"
    where = "livingroom"
    action = "brighten"
    data = {
        'what': what,
        'where': where
    }
    #response = do.switch(state,what,where,action)
    
    edng = re.compile(str("on").title(), re.I)
    ending = "ed"
    if edng.search('on') or edng.search('off'):
        ending = ""
    if response is None:
        print("NotFound", data)
    elif response is 0:
        print("The " + str(what) + " is already " + str(state).title() + ending)
    elif response is 1:
        print("The " + str(what) + " can not be operated with command " + str(action).title()+" and value "+str(state).title())
    elif response is True:
        print("I have Succesfully excecuted your "+str(action).title()+" request for the "+str(what).title()+" in the "+str(where).title())
    """""
    i=1
