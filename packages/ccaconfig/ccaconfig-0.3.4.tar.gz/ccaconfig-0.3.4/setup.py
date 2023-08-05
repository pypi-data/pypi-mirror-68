# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ccaconfig']

package_data = \
{'': ['*']}

install_requires = \
['ccalogging>=0.3.3,<0.4.0', 'pytest>=5.3.2,<6.0.0', 'pyyaml>=5.2,<6.0']

setup_kwargs = {
    'name': 'ccaconfig',
    'version': '0.3.4',
    'description': 'Easily find and read application configuration files.',
    'long_description': '# ccaConfig\n\na config file utility. Will read yaml formatted config files from various\nlocations in the following order, so that the \'nearer\' files override the\nfurther ones.  Finally, it checks the environment for variables and\noverrides any set in the config file.\n\nThe order of files to read is\n```\n/etc/appname.yaml\n/etc/appname/appname.yaml\n$HOME/.config/appname.yaml\n$HOME/.appname.yaml\n$(pwd)/appname.yaml\n```\n\nAny environment variables of the form\n\n```\nAPPNAME_VARIABLENAME\n```\n\nwill be found, chopped at the underscore, lower cased and set into the\nfinal configuration i.e: `config[variablename]` will exist if there is an\nenvironment variable `APPNAME_VARIABLENAME`.\n\n\n## Usage\n```\nfrom ccaconfig import ccaConfig\n\ncf = ccaConfig(appname="appname")\nconfig = cf.envOverride()\n```\n\nor, to not take environment variables into account:\n```\nfrom ccaconfig import ccaConfig\n\ncf = ccaConfig(appname="appname")\nconfig = cf.findConfig()\n```\n\nTwo additional dictionaries can be supplied, the first `defaultd` can be\nused to set a default config, and the 2nd, `overrided` can be used for\nconfig variables that you do not want overridden by any config file found\nor from the environment.\n\n```\nfrom ccaconfig import ccaConfig\n\ndefd = {"environment": "dev"}\noverd = {"product": "myapp"}\ncf = ccaConfig(appname="appname", defaultd=defd, overrided=overd)\nconfig = cf.envOverride()\n# config["environment"] == "dev" if it is not overridden by a subsequent\n# config file or from an environment variable\n#\n# config["product"] == "myapp" and will not be overridden, at all\n```\n\n',
    'author': 'Chris Allison',
    'author_email': 'chris.charles.allison@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ccdale/ccaconfig',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
