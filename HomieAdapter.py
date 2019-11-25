from HomieMQTT import HomieMQTT
from homie_classes import HomieDevice

class HomieAdapter:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/node/property/command  """

    DEVICES = []

    def __init__(self,host, port,root,authentication,user,password):
        self.homieroot = root
        self.homiemqtt = HomieMQTT(host,port,root,authentication,user,password)
        #print("sleeping....")
        #time.sleep(10)

    def getmessages(self):
        result1, result2, result3 = self.homiemqtt.getmessages()
        return result1, result2, result3

    def getdevices(self):
        message, parent, deviceid = self.homiemqtt.getmessages()
        device=HomieDevice(deviceid,message,parent)
        return deviceid, message, parent, device


    def getdevicesjson(self):
        message, parent, deviceid = self.homiemqtt.getmessages()
        device = HomieDevice(deviceid, message, parent)
        result_devices = []
        i = 0
        result_nodes = []
        for node in device._nodes:
            properties = device._nodes[node]._properties
            result_properties = []
            ha_type = ""
            for prop in properties:
                ha_type = device._nodes[node]._type
                if ha_type == "sensor":
                    if prop.find("measure") > -1:
                        ha_type = prop[8:]
                result_properties.append(
                    {"Name": prop, "Settable": properties[prop]._settable, "Unit": properties[prop]._unit,
                     "Value": properties[prop]._value, "Datatype": properties[prop]._datatype,
                     "Format": properties[prop]._format})
            result_nodes.append({"Node_id": device._nodes[node]._node_id, "Name": device._nodes[node]._name.replace(u'\xa0', ' '), "Type": ha_type,
                                 "Topicbase": device._nodes[node]._topic_base, "Properties": result_properties})
            i = i + 1
        result_devices.append({"Nodes": result_nodes})
        result = {'Devices': result_devices}
        return result

    def take_action(self,cmd):
        action = cmd[0]
        payload = cmd[1]
        root = self.homieroot
        topic = root+"/"+action
        self.homiemqtt.mqttc.publish(topic,str(payload))
        print("topic: "+topic+"=>"+payload)





