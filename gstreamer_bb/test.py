#!/usr/bin/env python
"""Example of using cairooverlay element with PyGst

See here for why require_foreign is needed for cairo:
https://bugzilla.gnome.org/show_bug.cgi?id=694604

Cairo methods:
https://www.cairographics.org/samples/
"""

# gst-launch-1.0 v4l2src device=/dev/video14 ! autovideoconvert ! glimagesink

import common_util.overlays as overlays
import common_util.gstreamer_video_pipeline as gst_pipeline
import common_util.colors as colors
import argparse
import gc
import sys

# images
from PIL import Image
from io import BytesIO
import io
import base64
import pickle
from pprint import pprint

import os
#import mxnet as mx
import warnings
#from mxnet import gluon
#from mxnet import nd
#from gluoncv.data.transforms import image as timage
#from gluoncv import data
import pickle
import time
import array as arr
from queue import Queue
import requests
import cairo
import numpy

from gi.repository import Gst
import gi
gi.require_version('Gst', '1.0')

if (sys.version_info[0] < 3):
    sys.exit("This sample requires Python 3. Please install Python 3!")

def color_by_id(id):
    """Returns a somewhat-unique color for the given class ID"""
    return [c / 255 for c in colors.COLORS[id % len(colors.COLORS)]]

def main():
    print("Testing...")

    with gst_pipeline.VideoOverlayPipeline(
            "Pasta demo",
            "/dev/video0") as pipeline:

        while pipeline.running:
            # Get a frame of video from the pipeline.
            frame = pipeline.get_frame()
            if frame is None:
                print("Frame is none ...")
                break

            f1 = open('/dev/shm/tmp_image.jpg', 'wb')
            f1.write(frame.data)
            f1.close()

            pipeline.clear_overlay()
            pipeline.add_overlay(overlays.Text("Pasta Detection", x=0, y=0,
                                              bg_color=color_by_id(-1)))
            
            # pill to pillow
            im = Image.open('/dev/shm/tmp_image.jpg')
            im.putalpha(256) # create alpha channel
            arr = numpy.array(im)
            height, width, channels = arr.shape
            surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)
            pipeline._buffer = surface

            pipeline._render(frame)
            print('rendered')

if (__name__ == "__main__"):
    main()
