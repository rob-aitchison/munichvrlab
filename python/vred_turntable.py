# Copyright (c) 2017 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.

import os
import sys
import sgtk

import vrScenegraph
import vrNodeUtils
import vrFileIO
import vrCamera
import vrMovieExport

import subprocess

HookBaseClass = sgtk.get_hook_baseclass()


class VREDTurntablePublishPlugin(HookBaseClass):
    """
    Plugin for publishing VRED turntable.
    """
    @property
    def name(self):
        """
        One line name describing the plugin
        """
        return "Publish VRED Turntable"

    @property
    def description(self):
        """
        Verbose, multi-line description of what the plugin does. This can
        contain simple html for formatting.
        """

        return """
        <p>This plugin publishes a VRED turntable for the current session.</p>
        """

    @property
    def item_filters(self):
        """
        List of item types that this plugin is interested in.

        Only items matching entries in this list will be presented to the
        accept() method. Strings can contain glob patters such as *, for example
        ["maya.*", "file.maya"]
        """
        return ["vred.session"]

    def accept(self, settings, item):
        """
        Method called by the publisher to determine if an item is of any
        interest to this plugin. Only items matching the filters defined via the
        item_filters property will be presented to this method.
        A publish task will be generated for each item accepted here. Returns a
        dictionary with the following booleans:
            - accepted: Indicates if the plugin is interested in this value at
                all. Required.
            - enabled: If True, the plugin will be enabled in the UI, otherwise
                it will be disabled. Optional, True by default.
            - visible: If True, the plugin will be visible in the UI, otherwise
                it will be hidden. Optional, True by default.
            - checked: If True, the plugin will be checked in the UI, otherwise
                it will be unchecked. Optional, True by default.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        :returns: dictionary with boolean keys accepted, required and enabled
        """
        publisher = self.parent
        engine = publisher.engine
        accepted = True

        return {
            "accepted": accepted,
            "visible": True,
            "checked": False,
            "enabled": True
        }

    def validate(self, settings, item):
        """
        Validates the given item to check that it is ok to publish. Returns a
        boolean to indicate validity.

        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        :returns: True if item is valid, False otherwise.
        """

        return True

    def publish(self, settings, item):
        """
        Executes the publish logic for the given item and settings.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """
        super(VREDTurntablePublishPlugin, self).publish(settings, item)

        self.logger.info("Publishing Turntable")

        publisher = self.parent
        version_data = item.properties["sg_version_data"]
        publish_data = item.properties["sg_publish_data"]

        self.cleanTempDir()

        self.importCamera()
        self.renderTurntable()
        self.makeMovie()

        publisher = self.parent
        path = item.properties["path"]

        # allow the publish name to be supplied via the item properties. this is
        # useful for collectors that have access to templates and can determine
        # publish information about the item that doesn't require further, fuzzy
        # logic to be used here (the zero config way)
        publish_name = item.properties.get("publish_name")
        if not publish_name:

            self.logger.debug("Using path info hook to determine publish name.")

            # use the path's filename as the publish name
            path_components = publisher.util.get_file_path_components(path)
            publish_name = path_components["filename"]

        # self.logger.info("Creating Version...")
        # version_data = {
        #     "project": item.context.project,
        #     "code": publish_name,
        #     "description": item.description,
        #     "entity": self._get_version_entity(item),
        #     "sg_task": item.context.task
        # }
        # version = publisher.shotgun.create("Version", version_data)
        # self.logger.info("Version created!")

        path = "c:/temp/turntable/turntable.mp4"
        upload_path = path.decode("utf-8")

        # if sys.platform.startswith("win"):
        #         upload_path = path.decode("utf-8")
        # else:
        #     upload_path = path

        self.parent.shotgun.upload(
            "Version",
            version_data["id"],
            upload_path,
            "sg_uploaded_movie"
        )

        midframe = "C:/temp/turntable/turntable4.png"

        self.parent.shotgun.upload_thumbnail(
            "Version",
            version_data["id"],
            midframe
        )

    def finalize(self, settings, item):
        """
        Execute the finalization pass. This pass executes once all the publish
        tasks have completed, and can for example be used to version up files.
        :param settings: Dictionary of Settings. The keys are strings, matching
            the keys returned in the settings property. The values are `Setting`
            instances.
        :param item: Item to process
        """
        self.logger.info("Turntable published successfully")

    def importCamera(self):
        check = vrScenegraph.findNode("ADSK_Turntable_Offset")
        checkname = check.getName()
        print checkname
        node = vrScenegraph.getSelectedNode()
        center = vrNodeUtils.getBoundingBoxCenter(node, 1)
        
        if checkname == "ADSK_Turntable_Offset":
            print ("Camera already exists in your Scene")
        else:
            print ("Camera is loaded into your Sceen")
            vrFileIO.load("C:/temp/SG_ADSK_Turntable_Offset.osb")
        
        
        vrScenegraph.findNode("ADSK_Turntable_Offset").setTranslation(center.x(),center.y(),center.z() )
        print "Camera was moved to" , center
        vrCamera.jumpViewPoint("ICV")

    def renderTurntable(self):
        rotateZ = vrScenegraph.findNode("Rotate_Z")
        amount = 10
        for i in range(0,amount):
            if i !=0:
                imageNum = 360/amount
            else:
                imageNum = 0
            rotateVal = imageNum*i
            rotateZ.setRotation(0,0,rotateVal)
            filename = "c:/temp/turntable/turntable"+str(i)+".png"
            width = 720
            height = 432
            vrMovieExport.createSnapshotFastInit(width, height, 0)
            vrMovieExport.createSnapshotFast(filename)
            #createSnapshot(filename, width, height, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0)

    def makeMovie(self):
        subprocess.check_call("ffmpeg -i c:/temp/turntable/turntable%d.png -vcodec libx264 -pix_fmt yuv420p  -g 30 -b:v 2000k -vprofile high -bf 0 -crf 26 c:/temp/turntable/turntable.mp4")

    def cleanTempDir(self):
        dir = "C:/temp/turntable"
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))

    def _get_version_entity(self, item):
        """
        Returns the best entity to link the version to.
        """

        if item.context.entity:
            return item.context.entity
        elif item.context.project:
            return item.context.project
        else:
            return None
