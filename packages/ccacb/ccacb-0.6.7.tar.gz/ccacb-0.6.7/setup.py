# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccacb']

package_data = \
{'': ['*']}

install_requires = \
['ccaconfig>=0.3.3,<0.4.0',
 'ccalogging>=0.3.3,<0.4.0',
 'pyperclip>=1.8.0,<2.0.0']

entry_points = \
{'console_scripts': ['ytcb = ccacb.watchclipboard:main']}

setup_kwargs = {
    'name': 'ccacb',
    'version': '0.6.7',
    'description': 'Watches the clipboard for youtube urls and downloads them',
    'long_description': '# ytcb\nWatches the clipboard for youtube urls and downloads them.\n\n## install\n\nfrom pypi:\n\n```\npython3 -m pip install ccacb --user --upgrade\n```\n\nfrom the repo (requires poetry):\n```\ngit clone https://github.com/ccdale/ccacb.git\ncd ccacb\npoetry install\npoetry build\npython3 -m pip install dist/ccacb-0.6.6-py3-none-any.whl --user --upgrade\n```\n\n## config\nedit `~/.config/ytcb.yaml`\n\n```\n---\nyoutubedl: /home/chris/bin/youtube-dl\nincoming: /home/chris/Videos\n```\n\n## example\n\n```\n$ ytcb\n08/05/2020 13:47:55 [INFO ]  ytcb - youtube-dl clipboard queue processor 0.6.3\n08/05/2020 13:47:55 [INFO ]  reading /home/chris/.config/ytcb.yaml\n08/05/2020 13:47:55 [INFO ]  Using /home/chris/bin/youtube-dl\n08/05/2020 13:47:55 [INFO ]  youtube-dl will store files in /home/chris/Videos/kmedia/incoming\n\n<CTRL>-c\n\n08/05/2020 13:48:11 [INFO ]  Interrupted: Will finish off the Q, then exit\n08/05/2020 13:48:12 [INFO ]  ytcb has finished\n```\n',
    'author': 'Chris Allison',
    'author_email': 'chris.charles.allison+ccacb@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/ccacb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
