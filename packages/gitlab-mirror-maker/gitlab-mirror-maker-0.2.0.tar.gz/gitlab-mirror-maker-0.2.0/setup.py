# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mirrormaker']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.1,<8.0.0', 'requests>=2.23.0,<3.0.0']

entry_points = \
{'console_scripts': ['gitlab-mirror-maker = '
                     'mirrormaker.mirrormaker:mirrormaker']}

setup_kwargs = {
    'name': 'gitlab-mirror-maker',
    'version': '0.2.0',
    'description': 'Automatically mirror your repositories from GitLab to GitHub',
    'long_description': '# GitLab Mirror Maker\n\nAutomatically mirror your repositories from GitLab to GitHub.',
    'author': 'Grzegorz Dlugoszewski',
    'author_email': 'pypi@grdl.dev',
    'maintainer': 'Grzegorz Dlugoszewski',
    'maintainer_email': 'pypi@grdl.dev',
    'url': 'https://gitlab.com/grdl/gitlab-mirror-maker',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
