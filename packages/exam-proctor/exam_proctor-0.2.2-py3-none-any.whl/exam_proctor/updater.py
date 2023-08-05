from .models import Session, Video, Process
from threading import Thread
from .utils import json_request, JsonRequestException
from datetime import datetime, timedelta
from playhouse.shortcuts import model_to_dict
from collections import defaultdict
from time import sleep
from pprint import pprint


DELTA_UPDATE = 30


class Updater(Thread):
    def __init__(self, app):
        super().__init__()
        self.end = False
        self.app = app

    def close(self):
        self.end = True

    def run(self):
        while not self.end:
            to_send = defaultdict(list)
            to_save = defaultdict(list)
            vs = Video.select().join(Session).where(
                (Video.ts_update.is_null() & ~Video.ts_end.is_null())
                |
                (Video.ts_update_upload.is_null() & ~Video.upload_url.is_null())
            )
            n = datetime.now()
            for v in vs:
                v.ts_update = n
                if v.ts_update is None:
                    v.ts_update = n
                if v.upload_url is not None:
                    v.ts_update_upload = n
                d = model_to_dict(v, max_depth=0)
                d['session'] = v.session.session_id
                url = v.session.service_url
                to_send[url].append(d)
                to_save[url].append(v)
            for url in to_send:
                try:
                    res = json_request(url, {
                        'action': 'update_video',
                        'data': to_send[url],
                    })
                    if 'end' in res and res['end']:
                        self.app.stop_session()
                    for v in to_save[url]:
                        v.save()
                except JsonRequestException as e:
                    print(e)

            to_send = defaultdict(list)
            to_save = defaultdict(list)
            ps = Process.select().join(Session).where(
                (Process.ts_update_create.is_null() & ~Process.ts_create.is_null())
                |
                (Process.ts_update_end.is_null() & ~Process.ts_end.is_null())
            )
            for p in ps:
                if p.ts_update_create is None:
                    p.ts_update_create = n
                if p.ts_end is not None:
                    p.ts_update_end = n
                d = model_to_dict(p, max_depth=0)
                d['session'] = p.session.session_id
                url = p.session.service_url
                pprint(d)
                to_send[url].append(d)
                to_save[url].append(p)
            for url in to_send:
                try:
                    json_request(url, {
                        'action': 'update_process',
                        'data': to_send[url],
                    })
                    for p in to_save[url]:
                        p.save()

                except JsonRequestException as e:
                    print(e)

            sleep(DELTA_UPDATE)
