# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['quoted',
 'quoted.scrapy',
 'quoted.scrapy.extensions',
 'quoted.scrapy.spiders']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'importlib-metadata>=1.6.0,<2.0.0',
 'rich>=1.0.3,<2.0.0',
 'scrapy>=2.1.0,<3.0.0']

entry_points = \
{'console_scripts': ['quoted = quoted.quoted:main']}

setup_kwargs = {
    'name': 'quoted',
    'version': '0.3.0',
    'description': 'Feed your brain with the best random quotes from multiple web portals.',
    'long_description': "# quoted\n\nFeed your brain with the best random quotes from multiple web portals.\n\n## Features\n\n* Multiple WEB sources\n* Rich Text\n* Argument options\n* Logs\n\n## Requirements\n\n```\ngit\npython 3x\npoetry\n```\n\n## Installation\n\n### Linux/MacOS\n\n```\n$ pip install quoted\n```\n\n### Windows\n\n\n## Usage\n\n```\n$ quoted\n\n\xe2\x80\x9cInsanity is doing the same thing, over and over again, but expecting different results.\xe2\x80\x9d\n\xe2\x80\x95\xe2\x80\x95 Narcotics Anonymous\n\ntags: humor, insanity, life, misattributed-ben-franklin, misattributed-mark-twain, misattributed-to-einstein\nlink: https://www.goodreads.com/quotes/5543-insanity-is-doing-the-same-thing-over-and-over-again\n\n\xc2\xa9 goodreads\n\nPowered by quoted\n```\n## Development\n\n### Run\n\n```\n$ poetry install\n$ poetry run quoted\n```\n\n### Build\n\n```\n$ poetry build\n```\n\nThe distribution packages are located in `dist` directory.\n\n### Publish\n\n```\n$ poetry publish\n```\n\n### Spiders\n\nSpider output is a list of dicts with the structure:\n```\n[\n    {\n        'author': 'Author Name',\n        'text': 'Text of Quote',\n        'tags': ['tag1','tag2'],\n        'url': 'https://www.quotesource.com/linktoquote'\n    }\n]\n```\n\n## Todo\n\n* Cache\n* Supports `bash` and `zsh`\n* Output formats\n\n## Contribution\n\n* File bugs, feature requests in [GitHub Issues](https://github.com/rcares/quoted/issues).\n",
    'author': 'Rodrigo Cares',
    'author_email': 'rcares@gmail.com',
    'maintainer': 'Rodrigo Cares',
    'maintainer_email': 'rcares@gmail.com',
    'url': 'https://github.com/rcares/quoted/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
