# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

# The code was taken from the documentation here: https://support.shotgunsoftware.com/hc/en-us/articles/219032918-Shotgun-Integration#Developing%20Apps%20for%20Shotgun

from sgtk.platform import Application

import sgtk

logger = sgtk.platform.get_logger(__name__)

class MunichVRLab(Application):

    def init_app(self):
        """
        Register menu items with Shotgun
        """        
        params = {
            "title": "Augmented",
        }

        self.engine.register_command("augmented_cmd", self.augmented, params)

        params2 = {
            "title": "Collaboration",
        }

        self.engine.register_command("collaboration_cmd", self.collaboration, params2)

        params3 = {
            "title": "Play Video",
        }

        self.engine.register_command("playvideo_cmd", self.playvideo, params3)

        params4 = {
            "title": "Powerwall",
        }

        self.engine.register_command("powerwall_cmd", self.powerwall, params4)

    def augmented(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Augmented Script Requested")
        self.engine.log_info("self is %s" % self)

    def collaboration(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Collaboration Script Requested")

    def playvideo(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Play Video Script Requested")

    def powerwall(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Powerwall Script Requested")


