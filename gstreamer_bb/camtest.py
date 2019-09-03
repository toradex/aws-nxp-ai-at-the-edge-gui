import common_util.overlays as overlays
import common_util.gstreamer_video_pipeline as gst_pipeline
import common_util.colors as colors
import argparse
import gc
import sys

if (sys.version_info[0] < 3):
    sys.exit("This sample requires Python 3. Please install Python 3!")


def color_by_id(id):
    """Returns a somewhat-unique color for the given class ID"""
    return [c / 255 for c in colors.COLORS[id % len(colors.COLORS)]]


def main():
    print("Hello Cenoura")

    with gst_pipeline.VideoOverlayPipeline(
            "Xnor Object Detection Demo",
            "/dev/video4") as pipeline:

        while pipeline.running:
            # Get a frame of video from the pipeline.
            frame = pipeline.get_frame()
            if frame is None:
                print("Frame is none ...")
                break

            # make the bound
            pipeline.clear_overlay()
            pipeline.add_overlay(overlays.Text("Pasta Detection", x=0, y=0,
                                               bg_color=color_by_id(-1)))

            bbox = overlays.BoundingBox(
                0.3, 0.3, 0.4, 0.4,
                "Shell",
                bg_color=color_by_id(5))
            pipeline.add_overlay(bbox)
            gc.collect()


if (__name__ == "__main__"):
    main()
