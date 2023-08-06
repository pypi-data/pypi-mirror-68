# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colour_sort']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'pillow>=6.2,<7.0']

extras_require = \
{'cli': ['importlib_resources>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['colour = colour_sort:cli.run']}

setup_kwargs = {
    'name': 'colour-sort',
    'version': '0.1.2',
    'description': 'A tool to generate images using all rgb colours with no duplicates.',
    'long_description': '## Colour Sort \n\nGenerating Images using all 256<sup>3</sup> RGB colours, inspired by https://allrgb.com/\n\n### Technique\n\nTo generate a re-coloured image, the source image\'s pixel data is sorted (using one of several different sorting modes) using numpy\'s `argsort` function, giving us a mapping from the original to the sorted version. This mapping is then used to "unsort" an array of all 256<sup>3</sup> colours that in sorted order. The result of this operation is then written out as our result.\n\n### Installing\n\nGo get [poetry](https://poetry.eustace.io/).\n```\n$ poetry install\n```\n\n### Running\n\nOnce the tool has been installed, it can be ran with the following command\n```\n$ colour generate --help\nusage: colour generate [-h] [--sort {brightness,avg,rgb,rbg,brg,bgr,grb,gbr}]\n                       infile outfile\n\npositional arguments:\n  infile\n  outfile\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --sort {brightness,avg,rgb,rbg,brg,bgr,grb,gbr}\n\n$ colour verify --help\nusage: colour verify [-h] infile\n\npositional arguments:\n  infile\n\noptional arguments:\n  -h, --help  show this help message and exit\n```\n',
    'author': 'David Buckley',
    'author_email': 'buckley.w.david@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/buckley-w-david/colour_sort',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.7',
}


setup(**setup_kwargs)
