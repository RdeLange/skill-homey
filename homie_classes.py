import paho.mqtt.client as mqtt
import threading

class HomieDevice:
    # A definition of a Homie Device

    def __init__(self,device_id, topics, parent_base):
        self._device_id = device_id
        self._topic_base = parent_base+'/'+device_id

        # Load Device Properties
        self._name = topics[self._topic_base+'/$name']
        self._conventionVersion = topics[self._topic_base+'/$homie']
        self._state = topics[self._topic_base+'/$state']
        try:
            self._ip = topics[self._topic_base+'/$ip']
        except KeyError:
            self._ip = ""
        try:
            self._mac = topics[self._topic_base+'/$mac']
        except KeyError:
            self._mac = ""

        # Load Nodes that are available for this Device
        self._nodes = {}
        for node in topics[self._topic_base+'/$nodes'].split(','):
            self._nodes[node] = HomieNode(node, topics, self._topic_base)

    @property
    def deviceId(self):
        """Return the Device ID of the device."""
        return self._device_id

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def homeVersion(self):
        """Return the Homie Framework Version of the device."""
        return self._conventionVersion

    @property
    def state(self):
        """Return the State of the device."""
        return self._state

    @property
    def ip(self):
        """Return the IP of the device."""
        return self._ip

    @property
    def mac(self):
        """Return the MAC of the device."""
        return self._mac

    @property
    def uptime(self):
        """Return the Uptime of the device."""
        return self._uptime

    @property
    def uptime(self):
        """Return the Signal of the device."""
        return self._signal

    @property
    def statsInterval(self):
        """Return the Stats Interval of the device."""
        return self._statsInterval

    @property
    def firmwareName(self):
        """Return the Firmware Name of the device."""
        return self._fw_name

    @property
    def firmwareVersion(self):
        """Return the Firmware Version of the device."""
        return self._fw_version

    @property
    def firmwareChecksum(self):
        """Return the Firmware Checksum of the device."""
        return self._fw_checksum

    @property
    def nodes(self):
        """Return a Dictionary of Nodes for the device."""
        return self._nodes

    @property
    def node(self, node_name):
        """Return a specific Node for the device."""
        return self._nodes[node_name]


class HomieNode:
    # A definition of a Homie Node
    def __init__(self, node_id, topics, parent_base):

        self._node_id = node_id
        self._topic_base = parent_base+'/'+node_id
        self._type = topics[self._topic_base+'/$type']
        self._name = topics[self._topic_base+'/$name']
        self._properties = {}
        try:
            for aproperty in topics[self._topic_base + '/$properties'].split(','):
                self._properties[aproperty] = HomieProperty(
                    aproperty, topics, self._topic_base)
        except KeyError:
            self._properties = {}


    @property
    def nodeId(self):
        """Return the Node Id of the node."""
        return self._node_id

    @property
    def type(self):
        """Return the Type of the node."""
        return self._type

    @property
    def name(self):
        """Return the Name of the node."""
        return self._name

    @property
    def properties(self):
        """Return a Dictionary of properties for the node."""
        return self._properties

    @property
    def property(self, property_name):
        """Return a specific Property for the device."""
        return self._properties[property_name]


class HomieProperty:
    # A definition of a Homie Property
    def __init__(self, property_id, topics, parent_base):

        self._property_id = property_id
        self._topic_base = parent_base+'/'+property_id
        try:
            self._value = topics[self._topic_base]
        except:
            self._value = ""
        self._settable = topics[self._topic_base+'/$settable']

        try:
            self._unit = topics[self._topic_base+'/$unit']
        except KeyError:
            self._unit = ""
        self._datatype = topics[self._topic_base+'/$datatype']
        self._name = topics[self._topic_base+'/$name']
        try:
            self._format = topics[self._topic_base + '/$format']
        except KeyError:
            self._format = ""



    @property
    def propertyId(self):
        """Return the Property Id of the Property."""
        return self._property_id

    @property
    def settable(self):
        """Return the Settablity of the Property."""
        return self._settable

    @property
    def value(self):
        """Return the Name of the Property."""
        return self._value

    @property
    def unit(self):
        """Return the Unit for the Property."""
        return self._unit

    @property
    def dataType(self):
        """Return the Data Type for the Property."""
        return self._datatype

    @property
    def format(self):
        """Return the Format for the Property."""
        return self._format