import os

PATH = os.path.expanduser('~/skeed_exam_proctor')
VERSION = "1.0"


if not os.path.exists(PATH):
    os.mkdir(PATH)


def get_path(p):
    return os.path.join(PATH, p)
