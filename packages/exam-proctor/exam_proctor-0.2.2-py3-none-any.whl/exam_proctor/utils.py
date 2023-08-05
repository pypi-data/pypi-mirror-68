from datetime import datetime, timedelta
import subprocess
import requests
import json
import sys
import os


def _jsondumps_converter(o):
     if isinstance(o, datetime):
          return o.strftime('%Y-%m-%d %H:%M:%S')


def _jsonloads_hook(json_dict):
     for (key, value) in json_dict.items():
          try:
               json_dict[key] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
          except:
               pass
     return json_dict


def json_datatime_loads(s):
     return json.loads(s, object_hook=_jsonloads_hook)


def json_datetime_dumps(d):
     return json.dumps(d, default=_jsondumps_converter)



class JsonRequestException(Exception):
    pass


def json_request(url, data=None):
    try:
        if data is None:
            data = {}
        try:
            res = requests.post(url, data=json_datetime_dumps(data))
        except Exception as e:
            raise JsonRequestException("Connection error: {}".format(e))
        if res.status_code != 200:
            raise JsonRequestException("Server error: {}".format(res.status_code))
        try:
            d = json_datatime_loads(res.text)
        except Exception as e:
            raise JsonRequestException("JSON decode error: {}".format(e))
        if 'status' not in d:
            raise JsonRequestException("Malformed JSON: {}".format(res.text))
        if d['status'] != 'OK':
            raise JsonRequestException("Remote error: {}".format(d['exception']))
        return d['response']

    except Exception as e:
        raise JsonRequestException("Error: {}".format(e))


def open_file_manager_on_dir(path):
    if os.path.isdir(path):
        if sys.platform == 'win32':
            os.startfile(path)

        elif sys.platform == 'darwin':
            subprocess.Popen(['open', path])

        else:
            try:
                subprocess.Popen(['xdg-open', path])
            except OSError:
                pass
