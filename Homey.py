"""For controlling Homey."""
import re
from .HomieAdapter import HomieAdapter
from mycroft.util.log import getLogger

LOGGER = getLogger(__name__)

"""	This Homey skill is partly ported from the Domoticz Skill by treussart
	Please find on https://github.com/treussart/domoticz_skill """

class Homey:
    """Class for controlling Homey."""


    def __init__(self, host, port, root, authentication, user, password):
        """Recover settings for accessing to Homey Homie MQTT que."""
        self.ha = HomieAdapter(host, port,root,authentication,user,password)

    def findnode(self, what, where):
        #input => what = what, where = where
        #output => [nodename, stype, properties] or None if nothing found
        #===START===>
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        result = None
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
                result = [snode_id,sname,typ,sproperties]
                break
            i += 1
        return result

    def findcommand(self, type, action, actionamount,properties):
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
            if rslt2.search('dim') or rslt2.search('decrease'):
                stlvl = int(dlevel) - int(dsrdst)
                if stlvl < 0:
                    stlvl = 0
                cmd = ["dim/set", str(stlvl)]
            elif rslt2.search('brighten') or rslt2.search('increase'):
                stlvl = int(dlevel) + int(dsrdst)
                if stlvl > 100:
                    stlvl = 100
                cmd = ["dim/set" , str(stlvl)]
            elif rslt2.search('set'):
                stlvl = int(dsrdst)
                if stlvl > 100:
                    stlvl = 100
                elif stlvl < 0:
                    stlvl = 0
                cmd = ["dim/set" , str(stlvl)]
            else:
                if rslt.search('lock') or rslt.search('open') or rslt.search('on'):
                    cmd = ["onoff/set","True"]
                elif rslt.search('unlock') or rslt.search('close') or rslt.search('off'):
                    cmd = ["onoff/set","False"]
            return cmd

    def switch(self, actionstate, what, where, action):
        """Switch the device in Homey."""
        if not self.ha.check_mqttconnection(): return False
        result = None
        data = self.findnode(what, where)
        if data == None: return None #node not found
        node_id = data[0]
        nodename = data[1]
        nodetype = data[2]
        nodeproperties = data[3]
        if nodetype == re.compile('light', re.IGNORECASE):
            targetstate_onoff = ""
            if actionstate == "on": targetstate_onoff = "true"
            elif actionstate == "off": targetstate_onoff = "false"
            if nodeproperties['onoff'] == targetstate_onoff: return 0 #targetstate is currentstate
            cmdparams = self.findcommand(nodetype, action,actionstate,nodeproperties)
            cmd = [node_id+"/"+cmdparams[0],cmdparams[1]]
            if cmd == False: return 1#command not valid
            self.ha.take_action(cmd)
            return True #succesfully operated
        return 1

    def get(self, what, where):
        """Get the device's data in Homey."""
        if not self.ha.check_mqttconnection(): return False
        result = []
        devices = self.ha.getdevicesjson()
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        #TEMPERATURE
        if wht.search("Temperature"):
            i=0
            while i < len(devices['Devices'][0]['Nodes']):
                if whr.search(devices['Devices'][0]['Nodes'][i]['Name']):
                    for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                        if property['Name'] == "measure-temperature":
                            result.append(["current temperature",property['Value'],"Degrees"])
                        if property['Name'] == "target-temperature":
                            result.append(["target temperature", property['Value'], "Degrees"])
                i += 1

        #HUMIDITY
        if wht.search("Humidity"):
            i=0
            while i < len(devices['Devices'][0]['Nodes']):
                if whr.search(devices['Devices'][0]['Nodes'][i]['Name']):
                    for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                        if property['Name'] == "measure-humidity":
                            result.append(["current humidity",property['Value'],"Percent"])
                i += 1

        return result
