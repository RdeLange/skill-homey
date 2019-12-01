# Copyright 2016 Mycroft AI, Inc.
#
# This file is part of Mycroft Core.
#
# Mycroft Core is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Mycroft Core is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Mycroft Core.  If not, see <http://www.gnu.org/licenses/>.

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from os.path import dirname, abspath
from .Homey import Homey
import sys
import re

__author__ = 'R. de Lange'

"""	This Homey skill is partly ported from the Domoticz Skill by treussart
	Please find on https://github.com/treussart/domoticz_skill """

sys.path.append(abspath(dirname(__file__)))
LOGGER = getLogger(__name__)


class HomeySkill(MycroftSkill):

    def __init__(self):
        super(HomeySkill, self).__init__(name="HomeySkill")

    def initialize(self):
        homey_switch_intent = IntentBuilder("SwitchIntent")\
            .optionally("TurnKeyword")\
            .require("StateKeyword")\
            .require("WhatKeyword")\
            .optionally("WhereKeyword").build()
        self.register_intent(homey_switch_intent,
                             self.handle_homey_switch_intent)

        homey_infos_intent = IntentBuilder("InfosIntent")\
            .require("InfosKeyword")\
            .require("WhatKeyword")\
            .require("WhereKeyword")\
            .optionally("StateKeyword").build()
        self.register_intent(homey_infos_intent,
                             self.handle_homey_infos_intent)
        self.homey = Homey(
            self.settings.get("hostname"),
            self.settings.get("port"),
            self.settings.get("device"),
            self.settings.get("authentication"),
            self.settings.get("username"),
            self.settings.get("password"))

    def handle_homey_switch_intent(self, message):
        state = message.data.get("StateKeyword")
        what = message.data.get("WhatKeyword")
        where = message.data.get("WhereKeyword")
        action = message.data.get("TurnKeyword")
        if where ==None: where = "all"
        data = {
            'what': what,
            'where': where
        }
        where.replace(" ","")
        print(where)
        LOGGER.debug("message : " + str(message.data))
        response = self.homey.switch(state, what, where, action)
        edng = re.compile(str(state).title(), re.I)
        ending = "ed"
        if edng.search('on') or edng.search('off'):
            ending = ""
        data['stateverb'] = str(state).title()+ending
        data['state'] = str(state).title()
        if response == False: self.speak_dialog("NoConnection",data)
        elif response is None:
            self.speak_dialog("NotFound", data)
        elif response is 2:
            self.speak_dialog("AlreadyTarget", data)
        elif response is 1:
            self.speak_dialog("OpsError", data)
        else:
            self.speak_dialog("OpsSuccess", data)

    def handle_homey_infos_intent(self, message):
        what = message.data.get("WhatKeyword")
        where = message.data.get("WhereKeyword")
        data = {
            'what': what,
            'where': where
        }
        where.replace(" ", "")
        print(where)
        response = self.homey.get(what, where)
        sentence = ""
        if response == False: self.speak_dialog("NoConnection",data)
        elif len(response) == 0:
            self.speak_dialog("NotFound", data)
        elif len(response) > 0:
            count = 1
            for item in response:
                d = data
                d['measurement'] = item[0]
                d['value'] = item[1]
                d['unit'] = item[2]
                if count ==1: self.speak_dialog("SensorRead1",d)
                elif count == len(response) and len(response) > 1:
                    sentence = self.speak_dialog("SensorRead2",d)
                elif count != len(response) and len(response) > 1:
                    self.speak_dialog("SensorRead3",d)

                count =count+1
        #LOGGER.debug("result : " + str(sentence))
        #self.speak(str(sentence))

    def stop(self):
        pass


def create_skill():
    return HomeySkill()
