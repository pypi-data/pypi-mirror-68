from .models import Session, Video
from threading import Thread
from datetime import datetime, timedelta
from time import sleep
from pprint import pprint
import ffsend
from . import glb


DELTA_UPDATE = 60
SEND_SERVICE_URL = 'https://send.firefox.com/'


class VideoUploader(Thread):
    def __init__(self):
        super().__init__()
        self.end = False

    def close(self):
        self.end = True

    def run(self):
        while not self.end:
            print("Checking for videos to upload")
            vs = Video.select().where(Video.upload_url.is_null() & ~Video.ts_end.is_null())
            for v in vs:
                try:
                    print("Uploading")
                    upload_url, token = ffsend.upload(SEND_SERVICE_URL, glb.get_path(v.name))
                    v.upload_url = upload_url
                    v.save()
                    print("Upload done")
                finally:
                    pass

            sleep(DELTA_UPDATE)
