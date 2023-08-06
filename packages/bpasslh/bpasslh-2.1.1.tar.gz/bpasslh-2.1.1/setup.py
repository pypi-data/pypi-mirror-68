# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bpasslh']

package_data = \
{'': ['*'],
 'bpasslh': ['data/*',
             'data/shapefiles/PSMA/*',
             'data/shapefiles/PSMA/act/*',
             'data/shapefiles/PSMA/nsw/*',
             'data/shapefiles/PSMA/nt/*',
             'data/shapefiles/PSMA/ot/*',
             'data/shapefiles/PSMA/qld/*',
             'data/shapefiles/PSMA/sa/*',
             'data/shapefiles/PSMA/tas/*',
             'data/shapefiles/PSMA/vic/*',
             'data/shapefiles/PSMA/wa/*']}

install_requires = \
['fiona>=1.8.13,<2.0.0', 'requests>=2.23.0,<3.0.0', 'shapely>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'bpasslh',
    'version': '2.1.1',
    'description': 'Location generalisation for sensitive species',
    'long_description': '# location-generalisation-utils\n\nHandling generalisation of location points based on rules for given species.\n',
    'author': 'Grahame Bowland',
    'author_email': 'grahame.bowland@qcif.edu.au',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
