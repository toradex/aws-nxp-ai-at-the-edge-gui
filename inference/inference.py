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
import threading

from gi.repository import Gst
import gi
gi.require_version('Gst', '1.0')

# inference framework
from dlr import DLRModel

if (sys.version_info[0] < 3):
    sys.exit("This sample requires Python 3. Please install Python 3!")

# ------------------------------------------------------------------ INFERENCE
class_names =['shell','elbow','penne','tortellini', 'farfalle']

# size used for inference
net_input_size=128
number_of_pixels = net_input_size*net_input_size
# RGB means
redmean=255*0.485
gremean=255*0.456
blumean=255*0.406
redstd=255*0.229
grestd=255*0.224
blustd=255*0.225

#bbox limits to avoid reflection
x1_limit=int(net_input_size*0.2)
x2_limit=int(net_input_size*0.8)

# load the model
model_path = '/usr/lib/python3.7/site-packages/inference-python'
device = 'cpu'
model = DLRModel(model_path + '/model/pasta_'+str(net_input_size), device)

#*************************START FLASK**********************
history = Queue(1000)
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
app = Flask(__name__)
# add cors
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
api = Api(app)

@app.route('/inference/')
@cross_origin()
def inference_web():
    global last_inference
    str_history = '{"history": ['
    while history.qsize()>0 :
        history_item = history.get(block=True, timeout=None)
        str_history = str_history + history_item.json()
        if history.qsize()>0 :
            str_history = str_history + ','
    str_history = str_history + ']}'
    return str_history

@app.route('/inference/last')
@cross_origin()
def last_inference_web():
    global last_inference
    return last_inference.json()

#************************* END FLASK **********************

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

class inference:
    def __init__(self, timestamp, inference_time,results):
        self.timestamp = timestamp
        self.inference_time = inference_time
        self.results = results
    def json(self):
        results = ('{"timestamp": "%s","inference_time": "%s",'
                    %(self.timestamp,self.inference_time))
        results = results + '"last":['
        for i in range(len(self.results)):
            results = results + self.results[i].json()
            if(i<len(self.results)-1):
                results = results + ','
        results = results +']}'
        return results

last_inference = inference(0,0,[])

def pasta_detection(image_in, width = 320, height = 240):
    global last_inference
    
    t1 = time.time()
    
    f1 = open('/dev/shm/tmp_image.jpg', 'wb')
    f1.write(image_in)
    f1.close()
    try: img
    except NameError: pass
    else: del(img)

    top = 0
    bottom = height
    left = (width/2)-(height/2)
    right = (width/2)+(height/2)
    
    img = Image.open('/dev/shm/tmp_image.jpg')
    img = img.crop((left, top, right, bottom)) 
    img = img.resize((net_input_size, net_input_size))
    image_in = np.array(img.resize((net_input_size, net_input_size)))
    image_in = image_in.reshape((number_of_pixels ,3))
    pix_val =np.transpose(image_in)
    pix_val = np.reshape(pix_val, (1,3, net_input_size,net_input_size))
    pix_val[0,0,:,:] = pix_val[0,0,:,:]-redmean
    pix_val[0,0,:,:] = pix_val[0,0,:,:]/redstd
    pix_val[0,1,:,:] = pix_val[0,1,:,:]-gremean
    pix_val[0,1,:,:] = pix_val[0,1,:,:]/grestd
    pix_val[0,2,:,:] = pix_val[0,2,:,:]-blumean
    pix_val[0,2,:,:] = pix_val[0,2,:,:]/blustd
    
    #img = Image.frombuffer('RGB', (width,height), image_in, "raw", 'RGB', 0, 1)
    #image_in = np.frombuffer(image_in, dtype=np.uint8)
    #img = Image.frombuffer('RGB', (width,height), image_in.astype('uint8'), "raw", 'RGB', 0, 1)
    #image_in = np.array(img.resize((net_input_size, net_input_size)))
    #image_in = image_in.reshape((number_of_pixels ,3))
    #pix_val =np.transpose(image_in)
    #pix_val = np.reshape(pix_val, (1,3, net_input_size,net_input_size))
    #pix_val[0,0,:,:] = pix_val[0,0,:,:]-redmean
    #pix_val[0,0,:,:] = pix_val[0,0,:,:]/redstd
    #pix_val[0,1,:,:] = pix_val[0,1,:,:]-gremean
    #pix_val[0,1,:,:] = pix_val[0,1,:,:]/grestd
    #pix_val[0,2,:,:] = pix_val[0,2,:,:]-blumean
    #pix_val[0,2,:,:] = pix_val[0,2,:,:]/blustd

    input_data = {'data': pix_val}
    t2 = time.time()
    outputs = model.run(input_data) #need to be a list of input arrays matching input names
    t3 = time.time()
    print('inference:::::::::::::::::')
    
    objects=outputs[0][0]
    scores=outputs[1][0]
    bounding_boxes=outputs[2][0]

    #print(scores)
    #print(objects)
    
    i=0
    result_set=[]
    while (scores[i]>=0.2) :

        if int(objects[i]) <= 4:
            this_object=class_names[int(objects[i])]
            this_result = result(
                        score= scores[i],
                        object= this_object,
                        xmin= (width/2-height/2)+bounding_boxes[i][0]/net_input_size*height,
                        xmax= (width/2-height/2)+bounding_boxes[i][2]/net_input_size*height,
                        ymin= bounding_boxes[i][1]/net_input_size*height,
                        ymax= bounding_boxes[i][3]/net_input_size*height,
                        #xmin= bounding_boxes[i][0]/net_input_size*width,
                        #xmax= bounding_boxes[i][2]/net_input_size*width,
                        #ymin= bounding_boxes[i][1]/net_input_size*height,
                        #ymax= bounding_boxes[i][3]/net_input_size*height,
                        time=t3)

            result_set.append(this_result)

        i=i+1

    last_inference = inference(t2,t3-t2,result_set)
    if(history.full()==False): #FLASK
       history.put(last_inference, block=True, timeout=None)
    t4 = time.time()
    #print('transformation time:',t2-t1+t4-t3)
    print('inference time:',t3-t2)
    #print('net size=',net_input_size)
    return result_set

# ------------------------------------------------------------------ END INFERENCE

def save_pickle(frame):
    f=open('arquivo.pickle', 'wb')
    pickle.dump(frame, f)

def color_by_id(id):
    """Returns a somewhat-unique color for the given class ID"""
    return [c / 255 for c in colors.COLORS[id % len(colors.COLORS)]]

def draw_bb(pipeline, frame, width = 320, height = 240):
    #im = Image.frombuffer('RGB', (width,height), frame, "raw", 'RGB', 0, 1)
    im = Image.open('/dev/shm/tmp_image.jpg')
    im.putalpha(256) # create alpha channel
    arr = np.array(im)
    _height, _width, channels = arr.shape
    surface = cairo.ImageSurface.create_for_data(arr, cairo.FORMAT_RGB24, width, height)
    pipeline._buffer = surface
    pipeline._render(frame)

def main():
    print("Calling video and inference")
    infCount = 0

    with gst_pipeline.VideoOverlayPipeline(
            "Pasta demo",
            "/dev/video4") as pipeline:

        while pipeline.running:
            # Get a frame of video from the pipeline.
            frame = pipeline.get_frame()
            if frame is None:
                print("Frame is none ...")
                break

            #print("Frame ok!")
            #save_pickle(frame.data)
            #break

            # call the inference
            ret = pasta_detection(frame.data)
            infCount = infCount + 1
            
            # put the overlays on the queue
            pipeline.clear_overlay()
            infCount = infCount + 1
            pipeline.add_overlay(overlays.Text("Pasta Detection " + str(infCount), x=0, y=0,
                                              bg_color=color_by_id(-1)))

            if ret != None:
                for item in ret:
                    bbox = overlays.BoundingBox(
                        (item.xmin)/320,
                        (item.ymin)/240,
                        (item.xmax - item.xmin)/320,
                        (item.ymax - item.ymin)/240,
                        item.object,
                        bg_color=color_by_id(5))
                    pipeline.add_overlay(bbox)
                    #print("Detected: " + item.object)
                    #print(item.score)
                    #print(item.time)

            # draw bound boxes
            draw_bb(pipeline, frame.data, 320, 240)

            gc.collect()

if (__name__ == "__main__"):
    thread1 = threading.Thread(target = main)
    thread1.start()

if __name__ == '__main__':
    print("Flask working well")
    app.run(host='0.0.0.0', port='5003')
else:
    print(__name__)
    print("Flask not working")
