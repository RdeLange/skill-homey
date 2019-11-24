import paho.mqtt.client as mqtt
import threading

class HomieMQTT:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/device class (optional)/zone (optional)/device name/capability/command  """

    DEVICES = []
    messages = {}
    homey_parent = ""
    homey_device = ""

    def __init__(self,host, port,root,authentication,user,password):
        try:
            self.mqttc = mqtt.Client()
            if authentication == True:
                self.mqttc.username_pw_set(username=user, password=password)
            self.mqttc.on_message = self.on_message
            print("Homey discovery started.....")
            self.mqttc.connect(host, int(port), 60)
            self.mqttc.subscribe(root+"/#", 0)
            threading.Thread(target=self.startloop).start()
        except KeyboardInterrupt:
            print("Received topics:")



    def startloop(self):
        self.mqttc.loop_forever()


    def on_message(self,mqttc, obj, msg,):
        #INITIAL VALUES
        payload = msg.payload.decode("utf-8")
        topic = str(msg.topic)
        temp = topic.split("/")
        self.homey_parent = temp[0]
        self.homey_device = temp[1]
        self.messages[topic] = payload


    def getmessages(self):
        return self.messages, self.homey_parent,self.homey_device
