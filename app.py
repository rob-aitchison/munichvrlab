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

class HelloWorld(Application):

    def init_app(self):
        """
        Register menu items with Shotgun
        """        
        params = {
            "title": "Hello, World!",
        }

        self.engine.register_command("hello_world_cmd", self.do_stuff, params)

        params2 = {
            "title": "Hello, Universe!",
        }

        self.engine.register_command("hello_universe_cmd", self.do_stuff2, params2)

    def do_stuff(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Hello, World!")
        # self.print_context()

        
    def do_stuff2(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Hello, Universe!")



    # def print_context(self):

    #     whereami = self.print_context
    #     logger.debug("RA: whereami is %s" % whereami)
    #     # logger.debug("RA: entity_type is %s" % entity_type)
    #     # logger.debug("RA: entity_ids is %s" % entity_ids)
        
