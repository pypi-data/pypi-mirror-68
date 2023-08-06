# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ssrm_test']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.16,<2.0',
 'scipy>=1.3,<2.0',
 'toolz>=0.10.0,<0.11.0',
 'typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'ssrm-test',
    'version': '0.1.1',
    'description': 'A library for Bayesian Sequential Sample Ratio Mismatch (SRM) test.',
    'long_description': '![Build](https://github.com/optimizely/ssrm/workflows/Build/badge.svg)\n\n# Sequential Sample Ratio Mismatch (SRM) test.\nA package for sequential testing of Sample Ratio Mismatch (SRM).\n\nContributors:\n- Michael Lindon (michael.lindon@optimizely.com )\n\n## Installation\nWe recommend that you use an isolated virtual environment to install and run the code in this repo (See: [virtualenv](https://pypi.org/project/virtualenv/) and [pyenv](https://github.com/pyenv/pyenv))\n\n1. Install dependencies: Run `make install`.\n    - If you wish to develop in the repo, run `make\n    install-dev`.  Also, see the contributing doc [here](/CONTRIBUTING.md)\n    > **Tip:** have a look in the [`Makefile`](/Makefile) to learn more about what this, and other make recipes do!\n1. Run tests:\n    -   `make check` to run all checks.\n    -   `make test` to run unit tests.\n\n\n## Tutorials\nWe provide a tutorial notebook that walks through an example of running a Sequential SRM test here.\n\n## Documentation\nThe latest reference documentation is here.\n\n## Contributing\nSee the contributing doc [here](/CONTRIBUTING.md).\n',
    'author': 'Michael Lindon',
    'author_email': 'michael.lindon@optimizely.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/optimizely/ssrm',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
