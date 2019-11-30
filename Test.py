from Homey import Homey
import sys
import re
import time

do = Homey("192.168.178.100","1883","homie/homey-5d667df592e8eb0c7d3f1022",False,"rstdelange","pasw0rd")

print("sleeping")
i=0
while i == 0:
    time.sleep(2)
    #print(do.findnode("light","livingroom"))
    #print(do.findcommand(re.compile('light', re.IGNORECASE), 'dim','60',{'onoff': 'true', 'dim': '70'}))
    #print(do.findcommand(re.compile('light', re.IGNORECASE), 'turn', 'off', {'onoff': 'true', 'dim': '70'}))
    #print(do.switch("on", "light", "kitchen", "turn")) #switch(state,what,where,action)
    #print(do.hadapter.getdevices())

    if not do.ha.check_mqttconnection():
        print("Connection with broker failed")
        break
    test = 2
    if test == 1:
        #START GET TEST
        what = "Temperature"
        where = "Livingroom"
        response = do.get(what,where)
        sentence = ""
        if len(response) == 0:
            sentence = "Unfortunately I do not know what the current "+what+" in the "+ where +" is."
        if len(response) > 0:
            count = 1
            for item in response:
                if count ==1: sentence = sentence + "The " + item[0] + " in the " + where + " is " + item[1] + " " + item[2]
                elif count == len(response) and len(response) > 1:
                    sentence = sentence + " and the " + item[0] + " in the " + where + " is " + item[1] + " " + item[2]
                elif count != len(response) and len(response) > 1:
                    sentence = sentence + " ,the " + item[0] + " in the " + where + " is " + item[1] + " " + item[2]

                count =count+1

        print(sentence)

        #END GET TEST

    if test ==2:
        state = "3 degrees"
        what = "temperature"
        where = "livingroom"
        action = "decrease"
        if where == "" : where = "all"
        data = {
            'what': what,
            'where': where
        }
        response = do.switch(state,what,where,action)

        edng = re.compile(str("on").title(), re.I)
        ending = "ed"
        if edng.search('on') or edng.search('off'):
            ending = ""
        if response is None:
            print("NotFound", data)
        elif response is 2:
            print("The " + str(what) + " is already " + str(state).title() + ending)
        elif response is 1:
            print("The " + str(what) + " can not be operated with command " + str(action).title()+" and value "+str(state).title())
        elif response is True:
            print("I have Succesfully excecuted your "+str(action).title()+" request for the "+str(what).title()+" in the "+str(where).title())
        else: print("Your request has been processed succesfully")
    i=1
