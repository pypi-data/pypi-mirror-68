# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_runners']
install_requires = \
['cmdy', 'diot', 'psutil>=5.0.0,<6.0.0', 'pyppl']

entry_points = \
{'pyppl_runner': ['pyppl_runner_dry = pyppl_runners:DRY_RUNNER',
                  'pyppl_runner_sge = pyppl_runners:SGE_RUNNER',
                  'pyppl_runner_slurm = pyppl_runners:SLURM_RUNNER',
                  'pyppl_runner_ssh = pyppl_runners:SSH_RUNNER']}

setup_kwargs = {
    'name': 'pyppl-runners',
    'version': '0.0.5',
    'description': 'More strict check of job success for PyPPL',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
