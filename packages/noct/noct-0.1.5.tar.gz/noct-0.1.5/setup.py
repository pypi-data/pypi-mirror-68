# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['noct', 'noct.schema', 'noct.schema.attachment', 'noct.schema.block']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['noct = noct.cli:cmd']}

setup_kwargs = {
    'name': 'noct',
    'version': '0.1.5',
    'description': 'Command Line Notification Tool',
    'long_description': '# NOCT\n  NOCTは、メッセンジャーへの通知を容易に実現するためのコマンドラインツールです。\nサポートしているメッセンジャー: SLACK\n\n# ドキュメント\n\u3000以下のページから利用方法について確認を行う事が可能です。\n- https://tuntunkun-org.github.io/noct/\n\n',
    'author': 'Naoya Sawada',
    'author_email': 'naoya@tuntunkun.com',
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
