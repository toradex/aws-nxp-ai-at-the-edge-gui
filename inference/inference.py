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
import warnings
import pickle
import time
import array as arr
from queue import Queue
import requests
import cairo
import numpy as np

from gi.repository import Gst
import gi
gi.require_version('Gst', '1.0')

# inference framework
from dlr import DLRModel

if (sys.version_info[0] < 3):
    sys.exit("This sample requires Python 3. Please install Python 3!")

# ------------------------------------------------------------------ INFERENCE
class_names =['shell','elbow','penne','tortellini']

# size used for inference
size=300, 300

# RGB means
redmean=255*0.485
gremean=255*0.456
blumean=255*0.406
redstd=255*0.229
grestd=255*0.224
blustd=255*0.225

# load the model
model_path = os.path.dirname(os.path.abspath(__file__))
device = 'cpu'
model = DLRModel(model_path + '/model', device)

class result:
    def __init__(self, score, object,xmin,ymin,xmax,ymax,time):
        self.score = score
        self.object = object
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.time = time
    def json(self):
       return ('{"score": "%s","object": "%s","xmin": "%s","ymin": "%s","xmax": "%s","ymax": "%s"}'
                   %(self.score,self.object,self.xmin,self.ymin,self.xmax,self.ymax))

def pasta_detection(image_in):
    t1 = time.time()

    # save the image
    # TODO please try to get this directly from framebuffer
    f1 = open('/dev/shm/tmp_image', 'wb')
    f1.write(image_in)
    f1.close()

    # resize image
    try:
        im = Image.open('/dev/shm/tmp_image')
        im.thumbnail(size, Image.ANTIALIAS)
    except IOError:
        print("Error trying to resize the frame")

    image_in = np.array(im)
    image_in = image_in.reshape((90000 ,3))
    pix_val = np.transpose(image_in)
    pix_val = np.reshape(pix_val, (1,3, 300,300))
    pix_val[0,0,:,:] = pix_val[0,0,:,:]-redmean
    pix_val[0,0,:,:] = pix_val[0,0,:,:]/redstd
    pix_val[0,1,:,:] = pix_val[0,1,:,:]-gremean
    pix_val[0,1,:,:] = pix_val[0,1,:,:]/grestd
    pix_val[0,2,:,:] = pix_val[0,2,:,:]-blumean
    pix_val[0,2,:,:] = pix_val[0,2,:,:]/blustd
    input_data = {'data': pix_val}
    t2 = time.time()
    outputs = model.run(input_data) #need to be a list of input arrays matching input names
    t3 = time.time()
    print('inference:::::::::::::::::')
    print(outputs[0]) # class ID
    #print(outputs[1]) # scores
    #print(outputs[2]) # bbox
    print('transformation time:',t2-t1)
    print('inference time:',t3-t2)

# ------------------------------------------------------------------ END INFERENCE

def color_by_id(id):
    """Returns a somewhat-unique color for the given class ID"""
    return [c / 255 for c in colors.COLORS[id % len(colors.COLORS)]]


def main():
    print("Calling video and inference")

    with gst_pipeline.VideoOverlayPipeline(
            "Pasta demo",
            "/dev/video4") as pipeline:

        while pipeline.running:
            # Get a frame of video from the pipeline.
            frame = pipeline.get_frame()
            if frame is None:
                print("Frame is none ...")
                break

            print("Frame ok!")

            # call the inference
            pasta_detection(frame.data)
            gc.collect()

if (__name__ == "__main__"):
    main()
