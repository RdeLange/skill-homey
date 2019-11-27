import paho.mqtt.client as mqtt
import json
import time
import threading

class HomeyAdapter:
    """Class for controlling Domoticz."""
    DEVICES = []

    def __init__(self,host, port,protocol,authentication,login,password):

        try:
            self.mqttc = mqtt.Client()
            self.mqttc.on_message = self.on_message
            print("Homey discovery started.....")
            self.mqttc.connect(host, int(port), 60)
            self.mqttc.subscribe(root+"/#", 1)
            threading.Thread(target=self.startloop).start()


        except KeyboardInterrupt:
            print("Received topics:")
            print(self.getdevices())

    def startloop(self):
        self.mqttc.loop_forever()

    def definedevice(self,payload):
        devicetype = "unknown"
        if payload.find("onoff") > -1:
            devicetype = "Light/Switch"
        if payload.find("dim") > -1:
            devicetype = "Light/Switch"
        if payload.find("measure-humidity") > -1:
            devicetype = "climate"
        if payload.find("measure-temperature") > -1:
            devicetype = "climate"
        return devicetype

    def updatedevice(self,root,deviceid,devicename,devicetype,devicestatus):
        ii = 0
        founddevice = 0
        while ii < len(self.DEVICES):
            if self.DEVICES[ii][0] == root + "/" + deviceid + "/" + devicename + "/":
                founddevice = 1
                if devicetype != "unknown":
                    self.DEVICES[ii][2] = devicetype
            ii += 1
        if founddevice == 0:
            self.DEVICES.append([root + "/" + deviceid + "/" + devicename + "/", devicename, devicetype, devicestatus])

    def updatelightstatus(self,topic,payload,root,deviceid,devicename):
        i = 0

        data = topic.split("/")

        if data[3] == "onoff" and len(data) == 4:
            while i < len(self.DEVICES):
                if self.DEVICES[i][0] == root + "/" + deviceid + "/" + devicename + "/":
                    self.DEVICES[i][3][0] = payload.decode("utf-8")
                i += 1

        if data[3] == "dim" and len(data) == 4:
            while i < len(self.DEVICES):
                if self.DEVICES[i][0] == root + "/" + deviceid + "/" + devicename + "/":
                    self.DEVICES[i][3][1] = payload.decode("utf-8")
                i += 1

    def updateclimatestatus(self,topic,payload,root,deviceid,devicename):
        i = 0
        data = topic.split("/")
        if data[3] == "measure-humidity" and len(data) == 4:
            while i < len(self.DEVICES):
                if self.DEVICES[i][0] == root + "/" + deviceid + "/" + devicename + "/":
                    self.DEVICES[i][3][1] = payload.decode("utf-8")
                i += 1
        if data[3] == "measure-temperature" and len(data) == 4:
            while i < len(self.DEVICES):
                if self.DEVICES[i][0] == root + "/" + deviceid + "/" + devicename + "/":
                    self.DEVICES[i][3][0] = payload.decode("utf-8")
                i += 1

    def take_action(self,actionline,idx):
        al = actionline.split("=")
        action = al[0]
        payload = al[1]
        root = self.DEVICES[idx-1][0]
        topic = root+action
        if payload == "on":
            payload = "True"
        if payload == "off":
            payload = "False"
        self.mqttc.publish(topic,str(payload))
        print("topic: "+topic+"=>"+payload)

    def on_message(self,mqttc, obj, msg,):
        #INITIAL VALUES
        payload = str(msg.payload)
        #print(msg.topic + " Payload -> " + payload)
        devicetype = "unknown"
        devicename = "unknown"
        devicestatus = []
        devicestatus.append("")
        devicestatus.append("")
        devicestatus.append("")
        devicestatus.append("")
        devicestatus.append("")
        data = msg.topic.split("/")
        root = data[0]
        deviceid = data[1]
        devicename = data[2]
        if devicename.find("$") == -1:

            #FIND DEVICETYPE
            result = msg.topic.find("$properties")
            if result > -1:
                devicetype = self.definedevice(payload)

            #CREATE NEW DEVICE OR UPDATE DEVICE
            self.updatedevice(root,deviceid,devicename,devicetype,devicestatus)

        #CHECK IF DEVICE IS LIGHT AND UPDATE VALUE IF APPLICABLE
        if msg.topic.find("onoff") > -1 or msg.topic.find("dim") > -1:
            self.updatelightstatus(msg.topic, msg.payload, root,deviceid,devicename)

        #CHECK IF DEVICE IS CLIMATE AND UPDATE VALUE IF APPLICABLE
        if msg.topic.find("measure-humidity") > -1 or msg.topic.find("measure-temperature") > -1:
            self.updateclimatestatus(msg.topic, msg.payload, root,deviceid,devicename)

    def getdevices(self):
        results = []
        count =1
        for device in self.DEVICES:
            if device[2] == "Light/Switch":
                if device[3][0] == "true":
                    device_status = "On"
                    device_data = "On"
                else:
                    device_status = "Off"
                    device_data = "Off"
                results.append({ "idx":count, "Name": device[1], "Type": device[2] , "Status":device_status, "Level":device[3][1],"Data":device_data })
            elif device[2] =="climate":
                if device[3][0] !="":
                    results.append(
                        {"idx": count, "Name": device[1], "Type": "Temperature", "Status": "",
                         "Level": "", "Data": device[3][0]})
                if device[3][1] !="":
                    results.append(
                        {"idx": count, "Name": device[1], "Type": "Humidity", "Status": "",
                         "Level": "", "Data": device[3][1]})

            else:
                results.append({ "idx":count, "Name": device[1], "Type": device[2] , "Status":device[3][0], "Level":device[3][1],"Data":device[3][0] })
            count=count+1

                #print(results)
        result=json.dumps({'result': results})
        #print(self.DEVICES)
        return result

