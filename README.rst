Homey_skill
==============

This skill is for controlling Homey with the source voice assistant Mycroft.


Requirements
------------

-  `Python3`_.
-  `Homey`_.
-  `Mycroft`_.


Configuration
-------------

Name your devices in Homey like this: "Where What".  Mycroft will look for the device listed
in Homey. However the skill will also look for "What Where" as well.  Devices can also be
referenced by "What" alone but Mycroft will only fall back to that if it can't find the device
using "Where What" or "What Where".

Note:  Especially with weather sensors try to name your devices something that won't interfere
with other skills.  For instance naming a device "weather" could cause Mycroft to give you the
current stat for the device named "weather" if you ask "what's the weather" rather than telling
you what the current weather is via the weather skill.

Mycroft Setting for the Homey Skill
-----

The default settings for the Homey connection and configuration is the local host without
authentication.  Please make sure to provide your device Homie mqtt topic. You can find that under the mqtt hub app in the Homey application.

Usage
-----

In English :

examples device names:

-  Living room light
-  Outside temperature
-  Front door lock

example phrases:

-  Hey Mycroft turn on the living room light
-  Hey Mycroft what is the outside temperature?
-  Hey Mycroft lock the front door
-  Hey Mycroft dim the dining room dimmer 50%


.. _Python3: https://www.python.org/downloads/
.. _Mycroft: https://www.mycroft.ai/
.. _Homey: https://homey.app/nl-nl/


