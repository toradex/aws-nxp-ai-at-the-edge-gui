#!/usr/bin/env python
import gi
import sys
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
import cairo


class Renderer():
    OVERLAY_FRAME_WIDTH = 320
    OVERLAY_FRAME_HEIGHT = 240
    OVERLAY_FRAME_DURATION = 1.0 / 30.0
    OVERLAY_CAPS = "video/x-raw,format=RGB,bpp=32,depth=32,width=%d,height=%d,red_mask=-16777216,green_mask=16711680,blue_mask=65280,alpha_mask=255,endianness=4321,framerate=1/30" % (OVERLAY_FRAME_WIDTH, OVERLAY_FRAME_HEIGHT)

    PIPELINE_SIMPLE = "appsrc name=overlay do-timestamp=true caps=\"%s\" ! xvimagesink" % (OVERLAY_CAPS)
    PIPELINE_MIX = "videotestsrc ! videomixer name=mix ! xvimagesink         appsrc name=overlay do-timestamp=true caps=\"%s\" ! mix." % (OVERLAY_CAPS)

    def __init__(self):
        # self.pipeline = Gst.parse_launch(self.PIPELINE_SIMPLE)
        self.pipeline = Gst.parse_launch(self.PIPELINE_MIX)

        bus = self.pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message::eos", self._on_eos)
        bus.connect("message::error", self._on_error)

        self.overlay = self.pipeline.get_by_name("overlay")
        self.overlay.connect('need-data', self._on_need_buffer)
        self.buffer = None
        self.buffer = Gst.Buffer.new_allocate(None, self.OVERLAY_FRAME_HEIGHT * self.OVERLAY_FRAME_WIDTH * 4, None)
        self.needs_update = True
        self.time = 0

    def start(self):
        self.pipeline.set_state(Gst.State.PLAYING)

    def stop(self):
        self.pipeline.set_state(Gst.State.PAUSED)

    def _on_eos(self, bus, msg):
        print "End of stream"
        self.loop.quit()

    def _on_error(self, bus, msg):
        error = msg.parse_error()
        print "Error: %s" % error[1]
        self.loop.quit()

    def _on_need_buffer(self, source, arg0):
        if self.needs_update:
            self.needs_update = False
            self._render()
        source.emit("push-buffer", self.buffer)

    def _render(self):
        # Would like to render into buffer using:
        #   ret, info = self.buffer.map(Gst.MapFlags.WRITE)
        #   image = cairo.ImageSurface.create_for_data(info.data, cairo.FORMAT_ARGB32, self.OVERLAY_FRAME_WIDTH, self.OVERLAY_FRAME_HEIGHT)
        # But Gst.MapInfo.data is an int (what's with that!?)
        # http://lazka.github.io/pgi-docs/api/Gst_1.0/structs/MapInfo.html#Gst.MapInfo

        # Instead, for lack of any better ideas, we let ImageSurface use its own buffer
        image = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.OVERLAY_FRAME_WIDTH, self.OVERLAY_FRAME_HEIGHT)
        context = cairo.Context(image)

        context.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        context.rectangle(0, 0, self.OVERLAY_FRAME_WIDTH, self.OVERLAY_FRAME_HEIGHT)
        context.fill()

        text = 'Hello world'
        context.select_font_face("sans-serif", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        context.set_font_size(20)
        (x, y, w, h, dx, dy) = context.text_extents(text)
        context.set_source_rgba(0.0, 0.0, 0.0, 1.0)
        context.move_to((self.OVERLAY_FRAME_WIDTH - w) / 2.0, (self.OVERLAY_FRAME_HEIGHT - h) / 2.0)
        context.show_text(text)

        # Then we copy into the Gst buffer. This is very, very, very slow (takes about 10 seconds for 720p)
        self.buffer.fill(0, image.get_data())


if __name__ == "__main__":
    Gst.init(sys.argv)
    GObject.threads_init()
    renderer = Renderer()

    loop = GObject.MainLoop()
    renderer.start()
    try:
        loop.run()
    except KeyboardInterrupt:
        loop.quit()
    renderer.stop()