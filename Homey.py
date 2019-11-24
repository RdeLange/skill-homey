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

    def findnode(self, what, where):
        #input => what = what, where = where
        #output => [nodename, stype, properties] or None if nothing found
        #===START===>
        wht = re.compile(what, re.I)
        whr = re.compile(where, re.I)
        result = None
        devices = self.ha.getdevicesjson()
        print(devices)
        i=0
        while i < len(devices['Devices'][0]['Nodes']):
            if whr.search(devices['Devices'][0]['Nodes'][i]['Name']) and wht.search(devices['Devices'][0]['Nodes'][i]['Name']):
                sname = devices['Devices'][0]['Nodes'][i]['Name']
                stype = devices['Devices'][0]['Nodes'][i]['Type']
                typ = re.compile(stype, re.I)
                sproperties ={}
                svalue = []
                #sproperties = {devices['Devices'][0]['Nodes'][i]['Properties'][0]['Ńame']:devices['Devices'][0]['Nodes'][i]['Properties'][0]['Value']}

                for property in devices['Devices'][0]['Nodes'][i]['Properties']:
                    sproperties[property['Name']]=property['Value']

                result = [sname,typ,sproperties]
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
            print(properties["dim"])
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
