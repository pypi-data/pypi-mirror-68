# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['exam_proctor']

package_data = \
{'': ['*'], 'exam_proctor': ['templates/*']}

install_requires = \
['bottle>=0.12.18,<0.13.0',
 'ffsend>=0.1.3,<0.2.0',
 'ipython>=7.13.0,<8.0.0',
 'mss>=5.0.0,<6.0.0',
 'opencv-python>=4.2.0,<5.0.0',
 'peewee>=3.13.2,<4.0.0',
 'psutil>=5.7.0,<6.0.0',
 'pystray>=0.15.0,<0.16.0',
 'python-ffmpeg>=1.0.11,<2.0.0',
 'requests>=2.23.0,<3.0.0',
 'waitress>=1.4.3,<2.0.0']

entry_points = \
{'console_scripts': ['exam_proctor = exam_proctor.bootstrap:main']}

setup_kwargs = {
    'name': 'exam-proctor',
    'version': '0.3.0',
    'description': '',
    'long_description': None,
    'author': 'Luca Allulli',
    'author_email': 'luca@skeed.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
