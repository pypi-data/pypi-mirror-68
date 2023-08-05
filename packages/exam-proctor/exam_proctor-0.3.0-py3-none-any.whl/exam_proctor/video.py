import time
import cv2
import mss
import numpy
from datetime import datetime, timedelta
from threading import Thread
from . import glb
from .models import *
import os
import hashlib
import traceback

FPS = 2
VIDEO_DURATION = timedelta(minutes=5)
# VIDEO_DURATION = timedelta(minutes=1)
# FORMAT = "XVID"
FORMAT = "mp4v"

EXT = ".mp4" if FORMAT == "mp4v" else ".avi"


class Screencast(Thread):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session
        self.end = False
        self.close_videos()

    def close_video(self, v, ts_end):
        fp = glb.get_path(v.name)
        with open(fp, 'rb') as r:
            content = r.read()
            v.size = len(content)
            v.hash = hashlib.sha256(content).hexdigest()
        v.ts_end = ts_end
        v.save()

    def close_videos(self):
        n = datetime.now()
        vs = Video.select().where(Video.session == self.session, Video.ts_end == None)
        for v in vs:
            self.close_video(v, n)

    def close(self):
        self.end = True

    def run(self):
        td = timedelta(seconds=1 / FPS)
        webcam = cv2.VideoCapture(0)
        prefix = self.session.session_id[:5]
        query = (Video
                 .select(peewee.fn.MAX(Video.position).alias('maxpos'))
                 .where(Video.session == self.session, Video.type=="screen")
        )
        n = query[0].maxpos
        if n is None:
            n = 0

        with mss.mss() as sct:
            # Part of the screen to capture
            # monitor = {"top": 40, "left": 0, "width": 800, "height": 640}
            # Full combination of screens
            monitors = sct.monitors[1:]

            # display screen resolution, get it from your OS settings
            sizes = []

            # define the codec
            fourcc = cv2.VideoWriter_fourcc(*FORMAT)

            try:
                w_cam, h_cam = webcam.get(3), webcam.get(4)
                while w_cam > 640 or h_cam > 480:
                    w_cam //= 2
                    h_cam //= 2
            except BaseException as e:
                traceback.print_exc()
                w_cam, h_cam = 640, 480
            sizes.append((int(w_cam), int(h_cam)))
            print(sizes)

            for i, m in enumerate(monitors):
                sizes.append((m['width'] // 2, m['height'] // 2))

            while not self.end:
                ts_start = datetime.now()
                ts_end = ts_start + VIDEO_DURATION
                videos = []
                outs = []
                n += 1
                for i, size in enumerate(sizes):
                    v = Video(
                        session=self.session,
                        ts_create=ts_start,
                        ts_end=None,
                        position=n,
                        type="screen",
                        name="{}_{}_{}{}".format(prefix, i, n, EXT),
                    )
                    v.save()
                    outs.append(cv2.VideoWriter(glb.get_path(v.name), fourcc, float(FPS), size))
                    videos.append(v)

                while not self.end and ts_end > datetime.now():
                    last_time = datetime.now()
                    for i, s in enumerate(sizes):
                        # Get raw pixels from the screen, save it to a Numpy array
                        try:
                            if i == 0:
                                ret, img = webcam.read()
                            else:
                                img = numpy.array(sct.grab(monitors[i - 1]))
                            frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            frame = cv2.resize(frame, s)
                            outs[i].write(frame)
                        except BaseException as e:
                            traceback.print_exc()

                    cur_time = datetime.now()
                    next_time = last_time + td
                    if next_time > cur_time:
                        t = (next_time - cur_time).microseconds / 1000000
                        print(t)
                        time.sleep(t)
                    else:
                        print("Too late")

                for v, o in zip(videos, outs):
                    try:
                        o.release()
                        self.close_video(v, ts_end)
                    except BaseException as e:
                        traceback.print_exc()

            webcam.release()


if __name__ == '__main__':
    s = Session.select().where(Session.session_id=="test")[0]
    s.save()
    sc = Screencast(s)
    sc.start()


def cleanup_videos():
    ext = EXT.lower()
    for f in os.listdir(glb.PATH):
        fp = os.path.join(glb.PATH, f)
        if fp.lower().endswith(ext):
            try:
                os.remove(fp)
            except:
                pass


def check_video_permissions():
    with mss.mss() as sct:
        monitors = sct.monitors[1:]
        sizes = []
        for i, m in enumerate(monitors):
            sizes.append((m['width'] // 2, m['height'] // 2))

        for i, s in enumerate(sizes):
            try:
                sct.grab(monitors[i])
            except BaseException:
                traceback.print_exc()

