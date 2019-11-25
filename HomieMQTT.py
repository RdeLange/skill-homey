import paho.mqtt.client as mqtt
import threading
import time

class HomieMQTT:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/device class (optional)/zone (optional)/device name/capability/command  """

    DEVICES = []
    messages = {}
    homey_parent = ""
    homey_device = ""
    mqttconnected = False

    def __init__(self,host, port,root,authentication,user,password):

        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                client.connected_flag = True  # set flag
                self.mqttconnected = True
                #print("connected OK")
            else:
                client.connected_flag = False
                self.mqttconnected = False
                print("Bad connection Returned code=", rc)

        def on_disconnect(client, userdata, rc):
            #logging.info("disconnecting reason  " + str(rc))
            client.connected_flag = False
            self.mqttconnected = False

        # create flag in class
        mqtt.Client.connected_flag = False
        self.mqttconnected = False

        try:
            self.mqttc = mqtt.Client()
            self.mqttc.on_connect = on_connect
            self.mqttc.on_disconnect = on_disconnect
            if authentication == True:
                self.mqttc.username_pw_set(username=user, password=password)
            self.mqttc.on_message = self.on_message
            print("Homey discovery started.....")
            self.mqttc.connect(host, int(port), 60)
            self.mqttc.subscribe(root+"/#", 0)
            threading.Thread(target=self.startloop).start()
        except:
            #print("No connection...")
            temp = 3

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
