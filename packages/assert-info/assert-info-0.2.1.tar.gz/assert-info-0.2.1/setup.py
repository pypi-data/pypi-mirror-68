# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['assert_info']

package_data = \
{'': ['*']}

install_requires = \
['asttokens>=2.0.4,<3.0.0', 'docopt>=0.6.2,<0.7.0', 'six>=1.14.0,<2.0.0']

entry_points = \
{'console_scripts': ['assert-info = assert_info:main']}

setup_kwargs = {
    'name': 'assert-info',
    'version': '0.2.1',
    'description': 'A tool for fixing bare assert statements',
    'long_description': "***********\nAssert Info\n***********\n\nAssert Info fixes up bare assert statements in your code so they include diagnostics when\nthey they're hit.\n\nA problem that crops up when working in legacy code bases is the use of ``assert X == Y``,\nwhen this fails you get minimal diagnostics.\n\nWhilst `Pytest <https://docs.pytest.org/en/latest/>`_ solves this by playing with AST at run\ntime, inserting diagnostics on the fly, you can't just run all your code with `Pytest`.\n\nThe standard libraries `unittest <https://docs.python.org/3/library/unittest.html>`_ solves\nthis problem with helper functions that include extra diagnostics by default, for instance\n``assertEqual``.\n\nThis package will inspect any file and replace assert statement which aren't accompanied\nby a message with a `unittest` style assertion so that when it fails you get diagnostics!\n\nTo run the script:\n\n.. code-block:: shell\n\n    pip install assert-info\n    assert-info -h\n",
    'author': 'Samuel Broster',
    'author_email': 's.h.broster+gitlab@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/broster/assert-info',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, !=3.5.*',
}


setup(**setup_kwargs)
