#!/usr/bin/env python
"""Example of using cairooverlay element with PyGst

See here for why require_foreign is needed for cairo:
https://bugzilla.gnome.org/show_bug.cgi?id=694604

Cairo methods:
https://www.cairographics.org/samples/
"""

from gi.repository import Gst
import cairo
import gi
import time
gi.require_version('Gst', '1.0')
gi.require_foreign('cairo')


class GstCairoExample(object):
    """Example class to generate user interface and create new GStreamer pipeline"""

    def __init__(self):
        self.pos = 0
        # self.pipeline = Gst.parse_launch(
        #    'v4l2src device=/dev/video4 ! video/x-raw,width=640,height=480 ! cairooverlay name=overlay ! autovideoconvert ! v4l2sink device=/dev/video14')
        self.pipeline = Gst.parse_launch(
            'v4l2src device=/dev/video0 ! videoconvert ! cairooverlay name=overlay ! videoconvert ! xvimagesink')
        # self.pipeline = Gst.parse_launch('videotestsrc ! cairooverlay name=overlay ! videoconvert ! xvimagesink')
        cairo_overlay = self.pipeline.get_by_name('overlay')
        cairo_overlay.connect('draw', self.on_draw)
        self.pipeline.set_state(Gst.State.PLAYING)

    def on_draw(self, _overlay, context, _timestamp, _duration):
        """Each time the 'draw' signal is emitted"""
        print(_timestamp)
        if self.pos > 150:
            self.pos = 0
        self.pos += 1
        # context.select_font_face(
        #    'Open Sans', cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        # context.set_font_size(40)
        #context.move_to(self.pos, 100)
        # context.text_path('TORADEX')
        #context.set_source_rgb(0.5, 0.5, 1)
        # context.fill_preserve()
        #context.set_source_rgb(0, 0, 0)
        # context.set_line_width(1)

        # bound boxes

        context.stroke()


print('lets go')
Gst.init(None)
GstCairoExample()

while True:
    time.sleep(5)
