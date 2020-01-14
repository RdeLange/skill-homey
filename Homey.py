"""For controlling Homey."""
import re
from .HomieAdapter import HomieAdapter
#from mycroft.util.log import getLogger

#LOGGER = getLogger(__name__)

"""	This Homey skill is partly ported from the Domoticz Skill by treussart
	Please find on https://github.com/treussart/domoticz_skill """

class Homey:
    """Class for controlling Homey."""


    def __init__(self, host, port, root, authentication, user, password,language):
        """Recover settings for accessing to Homey Homie MQTT que."""
        self.lang = language
        self.ha = HomieAdapter(host, port,root,authentication,user,password)

    def findnode(self, what, where):
        #input => what = what, where = where
        #output => [nodename, stype, properties] or None if nothing found
        #===START===>
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        result = []
        devices = self.ha.getdevicesjson()
        i=0
        while i < len(devices['Devices'][0]['Nodes']):
            if whr.search(devices['Devices'][0]['Nodes'][i]['Name']) and wht.search(devices['Devices'][0]['Nodes'][i]['Name']):
                sname = devices['Devices'][0]['Nodes'][i]['Name']
                stype = devices['Devices'][0]['Nodes'][i]['Type']
                typ = re.compile(stype, re.I)
                snode_id = devices['Devices'][0]['Nodes'][i]['Node_id']
                sproperties ={}
                for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                    sproperties[property['Name']]=property['Value']
                result = [[snode_id,sname,typ,sproperties]]
                break
            i += 1
        return result

    def findall(self, what):
        #input => what = what
        #output => [nodename, stype, properties] or None if nothing found
        #===START===>
        what = what[:len(what)-1]
        print(what)
        wht = re.compile(what, re.I)
        result = []
        devices = self.ha.getdevicesjson()
        i=0
        while i < len(devices['Devices'][0]['Nodes']):
            if wht.search(devices['Devices'][0]['Nodes'][i]['Name']):
                sname = devices['Devices'][0]['Nodes'][i]['Name']
                stype = devices['Devices'][0]['Nodes'][i]['Type']
                typ = re.compile(stype, re.I)
                snode_id = devices['Devices'][0]['Nodes'][i]['Node_id']
                sproperties ={}
                for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                    sproperties[property['Name']]=property['Value']
                result.append([snode_id,sname,typ,sproperties])
            i += 1
        return result

    def findcommand(self, type, action, actionamount,properties):
        degreesnoun = 'Degrees'
        degreenoun = 'Degree'
        lowernoun = 'lower'
        decreasenoun = 'decrease'
        highernoun = 'higher'
        increasenoun = 'increase'
        setnoun = 'set'
        dimnoun = 'dim'
        brightennoun = 'brighten'
        locknoun = 'lock'
        opennoun = 'open'
        onnoun = 'on'
        unlocknoun = 'unlock'
        closenoun = 'close'
        offnoun = 'off'

        if self.lang == 'nl-nl':
            degreesnoun = 'Graden'
            degreenoun = 'Graad'
            lowernoun = 'verminder'
            decreasenoun = 'verlaag'
            highernoun = 'verhoog'
            increasenoun = 'verhoog'
            setnoun = 'zet'
            dimnoun = 'dim'
            brightennoun = 'verhoog'
            locknoun = 'vergrendel'
            opennoun = 'open'
            onnoun = 'aan'
            unlocknoun = 'ontgrendel'
            closenoun = 'dicht'
            offnoun = 'uit'

        if type == re.compile('thermostat', re.IGNORECASE):
            dsrdst = str(actionamount).title()
            print(dsrdst)
            act = str(action).title()
            if dsrdst == "None":
                dsrdst = "0"
            rslt = re.compile(dsrdst, re.I)
            rslt2 = re.compile(act, re.I)
            try:
                temperature = properties['target-temperature'] #validate if correct => expect error
            except:
                temperature = 16
            print(temperature)

            if dsrdst.find(degreesnoun) > -1:
                dsrdst = int(dsrdst[0:2])
            elif dsrdst.find(degreenoun) > -1:
                dsrdst = int(dsrdst[0:2])
            else:
                dsrdst = 0
            cmd = False
            if rslt2.search(lowernoun) or rslt2.search(decreasenoun):
                stlvl = int(temperature) - int(dsrdst)
                if stlvl < 16:
                    stlvl = 16
                cmd = ["target-temperature/set", str(stlvl)]
            elif rslt2.search(highernoun) or rslt2.search(increasenoun):
                stlvl = int(temperature) + int(dsrdst)
                if stlvl > 25:
                    stlvl = 25
                cmd = ["target-temperature/set" , str(stlvl)]
            elif rslt2.search(setnoun):
                stlvl = int(dsrdst)
                if stlvl > 25:
                    stlvl = 25
                elif stlvl < 16:
                    stlvl = 16
                cmd = ["target-temperature/set" , str(stlvl)]
            else:
                stlvl = int(dsrdst)
                if stlvl > 25:
                    stlvl = 25
                elif stlvl < 16:
                    stlvl = 16
                cmd = ["target-temperature/set" , str(stlvl)]
            return cmd   

        if type == re.compile('light', re.IGNORECASE):
            dsrdst = str(actionamount).title()
            act = str(action).title()
            if dsrdst == "None":
                dsrdst = "25%"
            rslt = re.compile(dsrdst, re.I)
            rslt2 = re.compile(act, re.I)
            try:
                dlevel = properties['dim']
            except:
                dlevel = 0
            if dsrdst.find('%') > -1:
                if len(dsrdst) == 3:
                    dsrdst = int(dsrdst[0:2])
                elif len(dsrdst) == 4:
                    dsrdst = 100
                else:
                    dsrdst = 5
            cmd = False
            if rslt2.search(dimnoun) or rslt2.search(decreasenoun):
                stlvl = int(dlevel) - int(dsrdst)
                if stlvl < 0:
                    stlvl = 0
                cmd = ["dim/set", str(stlvl)]
            elif rslt2.search(brightennoun) or rslt2.search(increasenoun):
                stlvl = int(dlevel) + int(dsrdst)
                if stlvl > 100:
                    stlvl = 100
                cmd = ["dim/set" , str(stlvl)]
            elif rslt2.search(setnoun):
                if rslt.search(locknoun) or rslt.search(opennoun) or rslt.search(onnoun):
                    cmd = ["onoff/set","True"]
                elif rslt.search(unlocknoun) or rslt.search(closenoun) or rslt.search(offnoun):
                    cmd = ["onoff/set","False"]
                else:
                    stlvl = int(dsrdst)
                    if stlvl > 100:
                        stlvl = 100
                    elif stlvl < 0:
                        stlvl = 0
                    cmd = ["dim/set" , str(stlvl)]
            else:
                if rslt.search(locknoun) or rslt.search(opennoun) or rslt.search(onnoun):
                    cmd = ["onoff/set","True"]
                elif rslt.search(unlocknoun) or rslt.search(closenoun) or rslt.search(offnoun):
                    cmd = ["onoff/set","False"]
            return cmd

    def switch(self, actionstate, what, where, action):
        """Switch the device in Homey."""
        if not self.ha.check_mqttconnection(): return False
        result = None
        temperaturenoun = 'temperature'
        allnoun = 'all'
        onnoun = 'on'
        offnoun = 'off'

        if self.lang == 'nl-nl':
            temperaturenoun = 'temperatuur'
            allnoun = 'alle'
            onnoun = 'aan'
            offnoun = 'uit'

        if what == temperaturenoun: what = "thermostat"
        if where == allnoun:
            data = self.findall(what)
        else:
            data = self.findnode(what, where)
        if len(data) == 0: return None #node not found
        for node in data:
            result = None
            node_id = node[0]
            nodename = node[1]
            nodetype = node[2]
            nodeproperties = node[3]
            print(nodetype)
            if nodetype == re.compile('light', re.IGNORECASE):
                targetstate_onoff = ""
                if actionstate == onnoun: targetstate_onoff = "true"
                elif actionstate == offnoun: targetstate_onoff = "false"
                if nodeproperties['onoff'] == targetstate_onoff: 
                    result = 2 #targetstate is currentstate
                if result == None:
                    cmdparams = self.findcommand(nodetype, action,actionstate,nodeproperties)
                    cmd = [node_id+"/"+cmdparams[0],cmdparams[1]]
                    if cmd == False: result = 1#command not valid
                    if result == None:
                        self.ha.take_action(cmd)
                        result =  True #succesfully operated
            if nodetype == re.compile('thermostat', re.IGNORECASE):
            #    targetstate_temp = '16'
            #    if nodeproperties['target-temperature'] == targetstate_temp:
            #        result = 2 #targetstate is currentstate
                if result == None:
                    cmdparams = self.findcommand(nodetype, action,actionstate,nodeproperties)
                    if cmdparams == False: result = 1  # command not valid
                    if result == None:
                        if nodeproperties['target-temperature'] == cmdparams[1]:
                            result = 2 #targetstate is currentstate
                        if result == None:
                            cmd = [node_id+"/"+cmdparams[0],cmdparams[1]]
                            self.ha.take_action(cmd)
                            result =  True #succesfully operated



        if where == allnoun and result != None : result =3
        return result

    def get(self, what, where):
        """Get the device's data in Homey."""
        if not self.ha.check_mqttconnection(): return False
        result = []
        devices = self.ha.getdevicesjson()
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        temperaturenoun = 'Temperature'
        humiditynoun = 'Humidity'
        degreesnoun = 'Degrees'
        percentnoun = 'Percent'
        if self.lang == 'nl-nl':
            temperaturenoun = 'Temperatuur'
            humiditynoun = 'Luchtvochtigheid'
            degreesnoun = 'Graden'
            percentnoun = 'Procent'
        #TEMPERATURE
        if wht.search(temperaturenoun):
            i=0
            while i < len(devices['Devices'][0]['Nodes']):
                if whr.search(devices['Devices'][0]['Nodes'][i]['Name']):
                    for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                        if property['Name'] == "measure-temperature":
                            result.append(["current temperature",property['Value'],degreesnoun])
                        if property['Name'] == "target-temperature":
                            result.append(["target temperature", property['Value'], degreesnoun])
                i += 1

        #HUMIDITY
        if wht.search(humiditynoun):
            i=0
            while i < len(devices['Devices'][0]['Nodes']):
                if whr.search(devices['Devices'][0]['Nodes'][i]['Name']):
                    for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                        if property['Name'] == "measure-humidity":
                            result.append(["current humidity",property['Value'],percentnoun])
                i += 1

        return result
