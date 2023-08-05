# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['curious_slido']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.23.0,<3.0.0']

setup_kwargs = {
    'name': 'curious-slido',
    'version': '0.1.0',
    'description': 'Sends question to a sli.do event',
    'long_description': "# curious-slido\n\nSends your questions to a [sli.do](https://sli.do) event\n\n## How to install\n\n```\npip install curious-slido \n```\n\n## How to use\n\n```python\nfrom curious_slido import SlidoClient\n\n# You can grab it from URL with event, for example\n# https://app.sli.do/event/abcd1234/live/questions -> event_hash = 'abcd1234'\nevent_hash = 'abcd1234'\n\n# You can grab it from cookie Slido.EventAuthTokens (part after comma) or from \n# any api request: \n# Developer Tools -> Network -> (request to api.sli.do) -> Headers -> Request headers -> authorization (part after `Bearer`)\nauth_token = 'longlonglongstring'\n\nslido_client = SlidoClient(event_hash=event_hash, auth_token=auth_token)\nslido_client.send_question('Your question')\n```",
    'author': 'Dima Boger',
    'author_email': 'kotvberloge@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/b0g3r/curious-slido',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
