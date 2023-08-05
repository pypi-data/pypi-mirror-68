from bottle import route, get, post, run, template, HTTPResponse, request, redirect
import bottle
import requests
from time import sleep
import uuid
from .webcam import Webcam
from .utils import json_request, JsonRequestException, open_file_manager_on_dir
from datetime import datetime, timedelta
from playhouse.kv import KeyValue
from threading import Thread
from .video import Screencast, cleanup_videos
from .processes import Processes
from .video_uploader import VideoUploader
from .updater import Updater
from . import models
from . import glb
import webbrowser
import pystray
from PIL import Image
import random
import sys
import os
from pprint import pprint


PORT = 6520


def rel_path(fn):
    return os.path.join(os.path.dirname(__file__), fn)


bottle.TEMPLATE_PATH = [rel_path('templates')]


class App:
    def __init__(self):
        self.data = KeyValue(database=models.db, table_name='config')
        sleep(0.2)
        if 'client_id' not in self.data:
            self.data['client_id'] = str(uuid.uuid4())
        self.webcam = Webcam()
        ss = models.Session.select().where(models.Session.ts_expire > datetime.now())
        self.session = None
        self.recording = False
        self.cast = None
        self.processes = None
        self.video_uploader = VideoUploader()
        self.video_uploader.start()
        self.updater = Updater(self)
        self.updater.start()
        self.confirmation_id = -1
        self.confirmation_back = None
        self.icon = None
        if len(ss) > 0:
            self.start_session(ss[0])

    def start_session(self, s):
        print("Starting session")
        self.webcam.close()
        self.session = s
        self.recording = True
        self.cast = Screencast(s)
        self.cast.start()
        self.processes = Processes(s)
        self.processes.start()

    def stop_session(self):
        print("Ending session")
        self.recording = False
        if self.cast is not None:
            self.cast.close()
        if self.processes is not None:
            self.processes.close()

    def _exit(self):
        self.stop_session()
        if self.video_uploader is not None:
            self.video_uploader.close()
        if self.updater is not None:
            self.updater.close()
        sleep(5)
        self.icon.stop()
        os.kill(os.getpid(), 9)

    def exit(self):
        Thread(target=self._exit, args=(), kwargs={}).start()


app = App()


@route('/cam.jpg')
def webcam():

    return HTTPResponse(app.webcam.shot().tobytes(), content_type='image/jpeg')


@get('/')
def index():
    if app.session is not None:
        redirect(app.session.redirect_url)
    redirect('/privacy')


@get('/privacy')
def privacy():
    return template('privacy.html', error='')


@get('/start')
def start():
    return template('start.html', error='')


@post('/start')
def start_post():
    if 'expire' in app.data and app.data['expire'] < datetime.now():
        redirect(app.session.redirect_url)
    url = request.forms.get('url')
    try:
        res = json_request(url, data={'action': 'login', 'client_id': app.data['client_id']})
    except JsonRequestException as e:
        return template('start.html', error=str(e))
    s = models.Session(
        ts_create=res['start'],
        ts_expire=res['expire'],
        session_id=res['session_id'],
        service_url=url,
        redirect_url=res['redirect_url'],
    )
    s.save()
    app.start_session(s)
    redirect(s.redirect_url)


@get('/status')
def status():
    Video = models.Video
    vs = Video.select().where(Video.ts_update_upload.is_null() & ~Video.upload_url.is_null())

    ctx = {
        'status': 'recording' if app.recording else 'not recording',
        'video_upload': len(vs),
        'data_path': glb.PATH,
    }

    return template('status.html', **ctx)


@get('/open_data_path')
def open_data_path():
    open_file_manager_on_dir(glb.PATH)
    redirect('/status')


@get('/cleanup_data_path')
def cleanup_data_path():
    confirmation_id = request.params.get('yes')
    confirmation_back = request.params.get('back')
    if confirmation_id == app.confirmation_id:
        app.confirmation_id = -1
        cleanup_videos()
        redirect('/status')
    else:
        cid = str(random.randint(0, 100000))
        app.confirmation_id = cid
        msg = """
            Do you really want to delete all video files from data folder? This action cannot be undone!
        """
        return template('confirm.html', confirm=cid, message=msg, back=confirmation_back)


@get('/exit')
def exit_app():
    confirmation_id = request.params.get('yes')
    confirmation_back = request.params.get('back')
    if confirmation_id == app.confirmation_id:
        app.confirmation_id = -1
        app.exit()
        return template('message.html', message="Application is closing. Good bye!")
    else:
        cid = str(random.randint(0, 100000))
        app.confirmation_id = cid
        msg = """
            Do you really want to exit?
        """
        return template('confirm.html', confirm=cid, message=msg, back=confirmation_back)



def open_browser():
    sleep(1)
    webbrowser.open_new_tab('http://127.0.0.1:{}/'.format(PORT))


def create_icon_image():
    # Generate an image and draw a pattern
    image = Image.open(rel_path('user-graduate.png'))
    return image


def main_web(*args):
    Thread(target=open_browser, args=(), kwargs={}).start()
    run(host='localhost', server='waitress', port=PORT)
    # run(host='localhost', port=PORT)


def details():
    webbrowser.open_new_tab('http://127.0.0.1:{}/status'.format(PORT))


def main_tray():
    Thread(target=main_web, args=(), kwargs={}).start()
    menu = pystray.Menu(
        pystray.MenuItem("Show details", details, default=True)
    )
    icon = pystray.Icon('Skeed Esami Proctor', create_icon_image(), "Skeed", menu=menu)
    app.icon = icon
    icon.run()
