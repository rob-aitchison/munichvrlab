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

import subprocess

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
            "title": "Tiguan Collab",
        }

        self.engine.register_command("collaboration_cmd", self.collaboration, params2)

        params3 = {
            "title": "Open with VARJO",
        }

        self.engine.register_command("powerwall_cmd", self.powerwall, params3)

    def augmented(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Augmented Script Requested")
        
        chosen_file = self.shotgun.find_one(entity_type, [["id", "is", entity_ids[0]]], ["path", "task", "entity"])
        tk = sgtk.sgtk_from_path(chosen_file["path"]["local_path_windows"])
        context = tk.context_from_path(chosen_file["path"]["local_path_windows"])

        software_launcher = sgtk.platform.create_engine_launcher(tk, context, "tk-vred")
        software_versions = software_launcher.scan_software()
        launch_info = software_launcher.prepare_launch(software_versions[-1].path, "")
        env = os.environ.copy()
        for k in launch_info.environment:
            env[k] = launch_info.environment[k]
        subprocess.Popen([launch_info.path, launch_info.args, chosen_file["path"]["local_path_windows"], '-postpython', 'load(\'//10.146.20.210/Demo/VRED/Augmented/SRG_Augmented_V9.vpb\')'], env=env)

        self.engine.log_info("Augmented Script Launched")


    def collaboration(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Tiguan Collab Script Requested")

        chosen_file = self.shotgun.find_one(entity_type, [["id", "is", entity_ids[0]]], ["path", "task", "entity"])
        tk = sgtk.sgtk_from_path(chosen_file["path"]["local_path_windows"])
        context = tk.context_from_path(chosen_file["path"]["local_path_windows"])

        software_launcher = sgtk.platform.create_engine_launcher(tk, context, "tk-vred")
        software_versions = software_launcher.scan_software()
        launch_info = software_launcher.prepare_launch(software_versions[-1].path, "")
        env = os.environ.copy()
        for k in launch_info.environment:
            env[k] = launch_info.environment[k]
        subprocess.Popen([launch_info.path, launch_info.args, chosen_file["path"]["local_path_windows"], '-postpython', 'load(\'//10.146.20.210/Demo/VRED/Collaboration/Collab_2019_2_VW_Tiguan_35_VARJO.vpb\')'], env=env)
        filepath='C:/Batch/DEMO4_ps.bat'
        subprocess.Popen(filepath, shell=True, stdout = subprocess.PIPE)

        self.engine.log_info("Tiguan Collab Script Launched")


    def powerwall(self, entity_type, entity_ids):
        # this message will be displayed to the user
        self.engine.log_info("Open with VARJO Script Requested")

        chosen_file = self.shotgun.find_one(entity_type, [["id", "is", entity_ids[0]]], ["path", "task", "entity"])
        tk = sgtk.sgtk_from_path(chosen_file["path"]["local_path_windows"])
        context = tk.context_from_path(chosen_file["path"]["local_path_windows"])

        software_launcher = sgtk.platform.create_engine_launcher(tk, context, "tk-vred")
        software_versions = software_launcher.scan_software()
        launch_info = software_launcher.prepare_launch(software_versions[-1].path, "")
        env = os.environ.copy()
        for k in launch_info.environment:
            env[k] = launch_info.environment[k]
        subprocess.Popen([launch_info.path, launch_info.args, chosen_file["path"]["local_path_windows"], '-postpython', 'setDisplayMode(VR_DISPLAY_VARJO)'], env=env)

        self.engine.log_info("Open with VARJO Script Launched")
