# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azulejo']

package_data = \
{'': ['*'], 'azulejo': ['bin/*']}

install_requires = \
['biopython>=1.76,<2.0',
 'click>=7.1.2,<8.0.0',
 'click_loguru>=0.1.0,<0.2.0',
 'click_plugins>=1.1.1,<2.0.0',
 'coverage>=5.1,<6.0',
 'dask[bag]>=2.15.0,<3.0.0',
 'flynt>=0.46.1,<0.47.0',
 'gffpandas>=1.2.0,<2.0.0',
 'loguru>=0.4.1,<0.5.0',
 'matplotlib>=3.2.1,<4.0.0',
 'networkx>=2.4,<3.0',
 'numpy>=1.18.3,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'poetry_version>=0.1.5,<0.2.0',
 'pytest-datadir-mgr>=1.0.1,<2.0.0',
 'seaborn>=0.10.1,<0.11.0',
 'sh>=1.13.1,<2.0.0']

entry_points = \
{'console_scripts': ['azulejo = azulejo:cli']}

setup_kwargs = {
    'name': 'azulejo',
    'version': '0.6.5',
    'description': 'tile phylogenetic space with subtrees',
    'long_description': '.. epigraph:: azulejo\n              noun INFORMAL\n              a glazed tile, usually blue, found on the inside of churches and palaces in Spain and Portugal.\n\n\nazulejo tiles phylogenetic space with subtrees\n\n\n+-------------------+------------+------------+\n| Latest Release    | |pypi|     | |azulejo|  |\n+-------------------+------------+            +\n| GitHub            | |repo|     |            |\n+-------------------+------------+            +\n| License           | |license|  |            |\n+-------------------+------------+            +\n| Travis Build      | |travis|   |            |\n+-------------------+------------+            +\n| Coverage          | |coverage| |            |\n+-------------------+------------+            +\n| Code Grade        | |codacy|   |            |\n+-------------------+------------+            +\n| Dependencies      | |depend|   |            |\n+-------------------+------------+            +\n| Issues            | |issues|   |            |\n+-------------------+------------+------------+\n\n\n.. |azulejo| image:: docs/azulejo.jpg\n     :target: https://en.wikipedia.org/wiki/Azulejo\n     :alt: azulejo Definition\n\n.. |pypi| image:: https://img.shields.io/pypi/v/azulejo.svg\n    :target: https://pypi.python.org/pypi/azulejo\n    :alt: Python package\n\n.. |repo| image:: https://img.shields.io/github/commits-since/legumeinfo/azulejo/0.3.svg\n    :target: https://github.com/legumeinfo/azulejo\n    :alt: GitHub repository\n\n.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg\n    :target: https://github.com/legumeinfo/azulejo/blob/master/LICENSE\n    :alt: License terms\n\n.. |rtd| image:: https://readthedocs.org/projects/azulejo/badge/?version=latest\n    :target: http://azulejo.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Server\n\n.. |travis| image:: https://img.shields.io/travis/legumeinfo/azulejo.svg\n    :target:  https://travis-ci.org/legumeinfo/azulejo\n    :alt: Travis CI\n\n.. |codacy| image:: https://api.codacy.com/project/badge/Grade/99549f0ed4e6409e9f5e80a2c4bd806b\n    :target: https://www.codacy.com/app/joelb123/azulejo?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=legumeinfo/azulejo&amp;utm_campaign=Badge_Grade\n    :alt: Codacy.io grade\n\n.. |coverage| image:: https://codecov.io/gh/legumeinfo/azulejo/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/legumeinfo/azulejo\n    :alt: Codecov.io test coverage\n\n.. |issues| image:: https://img.shields.io/github/issues/LegumeFederation/lorax.svg\n    :target:  https://github.com/legumeinfo/azulejo/issues\n    :alt: Issues reported\n\n.. |requires| image:: https://requires.io/github/legumeinfo/azulejo/requirements.svg?branch=master\n     :target: https://requires.io/github/legumeinfo/azulejo/requirements/?branch=master\n     :alt: Requirements Status\n\n.. |depend| image:: https://api.dependabot.com/badges/status?host=github&repo=legumeinfo/azulejo\n     :target: https://app.dependabot.com/accounts/legumeinfo/repos/203668510\n     :alt: dependabot dependencies\n',
    'author': 'Joel Berendzen',
    'author_email': 'joelb@ncgr.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/legumeinfo/azulejo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
