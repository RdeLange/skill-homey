import paho.mqtt.client as mqtt
import threading
import time

class HomieMQTT:
    """ Class for controlling Homie Convention.
        The Homie Convention follows the following format:
        root/system name/device class (optional)/zone (optional)/device name/capability/command  """

    DEVICES = []
    messages = {}
    homie_parent = ""
    homie_device = ""

    def __init__(self,host, port,root,authentication,user,password):
        self.mq_host = host
        self.mq_port = port
        self.mq_root = root
        self.mq_authentication = authentication
        self.mq_user = user
        self.mq_password = password
        #self.reconnect(force=True)
        threading.Thread(target=self.reconnect,args=(True,)).start()

 #       try:
 #           self.mqttc = mqtt.Client()
 #           if authentication == True:
 #               self.mqttc.username_pw_set(username=user, password=password)
 #           self.mqttc.on_message = self.on_message
 #           print("Homey discovery started.....")
 #           self.mqttc.connect(host, int(port), 60)
 #           self.mqttc.subscribe(root+"/#", 0)
 #           threading.Thread(target=self.startloop).start()
 #       except:
            #print("No connection...")
  #          temp = 3

    def reconnect(self, force=False):
        if force == True:
            self.mq_connected = False
        while not self.mq_connected:
            try:
                self.mqttc = mqtt.Client(client_id='Homie Adapter')
                if self.mq_authentication == True:
                    self.mqttc.username_pw_set(username=self.mq_user, password=self.mq_password)
                self.mqttc.on_connect = self.on_connect
                self.mqttc.on_message = self.on_message
                self.mqttc.connect(host=self.mq_host,port=int(self.mq_port))
                threading.Thread(target=self.startloop).start()
                self.mq_connected = True
                print("Connected to MQ!")
            except Exception as ex:
                print("Could not connect to MQ: {0}".format(ex))
                print("Trying again in 5 seconds...")
                time.sleep(5)
        self.notify()

    def startloop(self):
        self.mqttc.loop_forever()


    def on_message(self,mqttc, obj, msg,):
        #INITIAL VALUES
        payload = msg.payload.decode("utf-8")
        topic = str(msg.topic)
        temp = topic.split("/")
        self.homie_parent = temp[0]
        self.homie_device = temp[1]
        self.messages[topic] = payload

    def on_connect(self, client, userdata, flags, rc):
        self.mqttc.subscribe(self.mq_root+"/#", 0)

    def notify(self):
        #self.reconnect()
        threading.Thread(target=self.reconnect,args=(False,)).start()

    def getmessages(self):
        print(self.mq_root)
        temp = self.mq_root.split("/")
        self.homie_parent = temp[0]
        self.homie_device = temp[1]
        return self.messages, self.homie_parent,self.homie_device
