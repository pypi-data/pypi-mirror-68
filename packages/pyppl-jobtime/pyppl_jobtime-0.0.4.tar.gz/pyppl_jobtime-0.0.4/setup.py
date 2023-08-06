# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_jobtime']
install_requires = \
['cmdy', 'pyppl']

entry_points = \
{'pyppl': ['pyppl_jobtime = pyppl_jobtime']}

setup_kwargs = {
    'name': 'pyppl-jobtime',
    'version': '0.0.4',
    'description': 'Job running time statistics for PyPPL',
    'long_description': '# pyppl_jobtime\n\nJob running time statistics for [PyPPL](https://github.com/pwwang/PyPPL).\n\n## Installation\nRequire `R` and `ggplot2`.\n```shell\npip install pyppl_jobtime\n```\n\nAfter this plugin is installed, a file named `job.time` will be created in each job directory with running time in seconds saved in it.\n\n## Plotting the running time profile\n```shell\npyppl jobtime --proc pVcfFix --outfile profile.png\n```\n\n![profile.png](./images/profile.png)\n\n- Using violin plot:\n    ```shell\n    pyppl jobtime --proc pVcfFix --outfile violin.png --plottype violin\n    ```\n    ![violin.png](./images/violin.png)\n\n- Changing process names:\n    ```shell\n    pyppl jobtime --outfile procnames.png \\\n        --proc pVcfFix --ggs.scale_x_discrete:dict \\\n        --ggs.scale_x_discrete.labels:list A B C\n    ```\n\n    ![procnames.png](./images/procnames.png)\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pyppl_jobtime',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
