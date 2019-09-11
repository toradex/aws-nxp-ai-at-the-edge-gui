import os
import mxnet as mx
import warnings
from mxnet import gluon
from gluoncv.data.transforms import image as timage
import pickle
import time
import array as arr
from queue import Queue

class_names =['shell','elbow','penne','tortellini']

warnings.simplefilter("ignore")

ctx = mx.cpu()
net = gluon.nn.SymbolBlock.imports("pasta_inference-symbol.json",['data'], "pasta_inference-0000.params", ctx=ctx)

history = Queue(1000)

#*************************START FLASK**********************
from flask import Flask
app = Flask(__name__)

@app.route('/inference/')
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
def last_inference_web():
    global last_inference
    return last_inference.json()

#************************* END FLASK **********************

class result:
    def __init__(self, score, object,xmin,ymin,xmax,ymax):
        self.score = score
        self.object = object
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
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

def get_inference(input_image):
    global last_inference

    f1 = open('/dev/shm/tmp_image.jpg', 'wb')
    f1.write(input_image)
    f1.close()

    try: img
    except NameError: pass
    else: del(img)

    img = mx.image.imread('/dev/shm/tmp_image.jpg')
    img = timage.resize_short_within(img, 300, 1024)
    orig_img = img.asnumpy().astype('uint8')
    img = mx.nd.image.to_tensor(img)
    img = mx.nd.image.normalize(img, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225))

    t1= time.time()
    objects, scores, bounding_boxes = net(img.expand_dims(0))
    t2= time.time()

    i=0
    result_set=[]
    while (objects[0][i]>=0) :

        this_object=class_names[int(objects[0][i].asscalar())]
        this_result = result(
                    score= scores[0][i].asscalar(),
                    object= this_object,
                    xmin= bounding_boxes[0][i][0].asscalar(),
                    ymin= bounding_boxes[0][i][1].asscalar(),
                    xmax= bounding_boxes[0][i][2].asscalar(),
                    ymax= bounding_boxes[0][i][3].asscalar())
        result_set.append(this_result)

        i=i+1

    last_inference = inference(t2,t2-t1,result_set)
    history.put(last_inference, block=True, timeout=None)

    return result_set

#*************************TEST ONLY**********************
#if __name__ == "__main__":
#    f1 = open('test_image.jpg', 'rb')
#    f1_bytearray = bytearray(f1.read())
#    ret = get_inference(f1_bytearray)
#    app.run('0.0.0.0',1234)
#************************* TEST ONLY **********************
