"""For controlling Homey."""
import urllib
import urllib.request
import json
import re
#from HomeyAdapter import HomeyAdapter
from HomieAdapter import HomieAdapter
#from mycroft.util.log import getLogger

#LOGGER = getLogger(__name__)

"""	This Homey skill is partly ported from the Domoticz Skill by treussart
	Please find on https://github.com/treussart/domoticz_skill """

class Homey:
    """Class for controlling Homey."""


    def __init__(self, host, port, root, authentication, user, password):
        """Recover settings for accessing to Homey Homie MQTT que."""
        self.ha = HomieAdapter(host, port,root,authentication,user,password)

    def findid(self, what, where, state):
        i = 0
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        #f = urllib.request.urlopen(self.url + "/json.htm?type=devices&filter=all&used=true")
        #f = self.ha.getdevicesjson()
        deviceid, message, parent, device = self.ha.getdevices()
        #print(f)
        #response = f.read()
        #payload = json.loads(f)
        idx = False
        stype = False
        dlevel = False
        result = None

        for node in device._nodes:
            print(node)
            if whr.search(node) and wht.search(node):
                stype = device._nodes[node]._type
                typ = re.compile(stype, re.I)
                dlevel = "100"
                if typ.search("Group") or typ.search("Scene"):
                    stype = "scene"
                elif typ.search("light"):
                    stype = "light"
                    properties = device._nodes[node]._properties
                    for prop in properties:
                        if prop == "dim":
                            dlevel = properties[prop]._value
                else:
                    stype = "light"
                idx = device._nodes[node]._node_id
                rslt = re.compile(" " + str(state).title(), re.I)
                print(rslt)
                if stype == "light":
                    properties = device._nodes[node]._properties
                    print(properties["onoff"]._value)
                    if rslt.search(" " + properties["onoff"]._value):
                        result = 0
                    else:
                        result = 1
                    break

        return [idx, result, stype, dlevel]


    def findcmd(self, state, action, dlevel):
        dsrdst = str(state).title()
        act = str(action).title()
        if dsrdst == "None":
            dsrdst = "25%"
        rslt = re.compile(dsrdst, re.I)
        rslt2 = re.compile(act, re.I)
        if dsrdst.find('%') > -1:
            if len(dsrdst) == 3:
                dsrdst = int(dsrdst[0:2])
            elif len(dsrdst) == 4:
                dsrdst = 100
            else:
                dsrdst = 5
        cmd = False
        if rslt2.search('dim') or rslt2.search('decrease'):
            stlvl = int(dlevel) - int(dsrdst)
            if stlvl < 0:
                stlvl = 0
            cmd = "dim/set=" + str(stlvl)
        elif rslt2.search('brighten') or rslt2.search('increase'):
            stlvl = int(dlevel) + int(dsrdst)
            if stlvl > 100:
                stlvl = 100
            cmd = "dim/set=" + str(stlvl)
        elif rslt2.search('set'):
            stlvl = int(dsrdst)
            if stlvl > 100:
                stlvl = 100
            elif stlvl < 0:
                stlvl = 0
            cmd = "dim/set=" + str(stlvl)
        else:
            if rslt.search('lock') or rslt.search('open') or rslt.search('on'):
                cmd = "onoff/set=on"
            elif rslt.search('unlock') or rslt.search('close') or rslt.search('off'):
                cmd = "onoff/set=off"
        return cmd

    def switch(self, state, what, where, action):
        """Switch the device in Homey."""
        data = []
        data = self.findid(what, where, state)
        print(data)
        idx = data[0]
        result = data[1]
        stype = data[2]
        dlevel = data[3]
        if result is 1:
            #print("check")
            cmd = self.findcmd(state, action, dlevel)
            if cmd:
                print(cmd)
                self.hadapter.take_action(cmd,idx)
                result = True
            else:
                result = 1
                #LOGGER.debug("no command found")
        return result

    def get(self, what, where):
        """Get the device's data in Homey."""
        try:
            f = self.hadapter.getdevices()
            # response = f.read()
            payload = json.loads(f)
            #payload = json.loads(response.decode('utf-8'))
            wht = re.compile(what, re.I)
            i = 0
            if where is not None:
                whr = re.compile(where, re.I)
                while i < len(payload['result']):
                    if whr.search(payload['result'][i]['Name']) and wht.search(payload['result'][i]['Type']):
                        break
                    elif i is len(payload['result']) - 1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            elif where is None:
                while i < len(payload['result']):
                    if wht.search(payload['result'][i]['Type']):
                        break
                    elif i is len(payload['result']) - 1:
                        payload['result'][i]['Data'] = None
                        break
                    i += 1
            return payload['result'][i]
        except IOError as e:
            #LOGGER.error(str(e) + ' : ' + str(e.read()))
            temp = 3
