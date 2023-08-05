# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['config_file', 'config_file.parsers']

package_data = \
{'': ['*']}

install_requires = \
['nested-lookup>=0.2.19,<0.3.0']

extras_require = \
{'toml': ['toml>=0.10.0,<0.11.0'], 'yaml': ['pyyaml>=5.3.1,<6.0.0']}

setup_kwargs = {
    'name': 'config-file',
    'version': '0.10.0',
    'description': 'Manage your configuration files.',
    'long_description': '# Config File\n\n> Manage and manipulate your configuration files\n\n![Python Version](https://img.shields.io/pypi/pyversions/config-file.svg)\n[![Version](https://img.shields.io/pypi/v/config-file)](https://pypi.org/project/config-file/)\n[![Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)\n[![Documentation Status](https://readthedocs.org/projects/config-file/badge/?version=latest)](https://config-file.readthedocs.io/en/latest/?badge=latest)\n[![Build Status](https://travis-ci.com/eugenetriguba/config-file.svg?branch=master)](https://travis-ci.com/eugenetriguba/config-file)\n[![Codecov](https://codecov.io/gh/eugenetriguba/config-file/graph/badge.svg)](https://codecov.io/gh/eugenetriguba/config-file)\n\n## About Config File\n\nThe Config File project is designed to allow you to easily manipulate your \nconfiguration files with the same simple API. for manipulating INI,\nJSON, YAML, and TOML configuration files. For the time being, it only\nsupports INI and JSON.\n\n## Installation\n\nConfig File is available to download through PyPI using pip.\n\n```bash\n$ pip install config-file\n```\n\nIf you want to manipulate YAML and TOML, you\'ll want to download the extras as well.\n\n```bash\n$ pip install config-file[yaml, toml]\n```\n\n## Usage\n\nSay you have an INI file you want to manipulate. It must have an .ini\nextension in order for the package to recognize it.\n\n```ini\n[section]\nfirst_key = 5\nsecond_key = blah\nthird_key = true\n```\n\nThen we can manipulate it as follows.\n\n```python\nfrom config_file import ConfigFile\n\nORIGINAL_CONFIG_PATH = Path("~/some-project/some-other-config-file.ini")\nCONFIG_PATH = Path("~/some-project/config.ini")\n\n# Our path can be a string or a Path object. \n# The "~" will be automatically expanded to the full path for us.\nconfig = ConfigFile(CONFIG_PATH)\n\n# All the types will be retrieved as strings unless specified otherwise.\nprint(config.get("section.first_key"))\n>>> "5"\nprint(config.get("section.first_key", return_type=int))\n>>> 5\n\n# This holds true when we retrieve entire sections as well. However, we can\n# also recursively parse the entire section is desired.\nprint(config.get("section"))\n>>> {\'first_key\': \'5\', \'second_key\': \'blah\', \'third_key\': \'true\'}\nprint(config.get("section", parse_types=True))\n>>> {\'first_key\': 5, \'second_key\': \'blah\', \'third_key\': True}\n\n# Sometimes we want to retrieve a key but don\'t know whether or not \n# it will be set. In that case, we can set a default.\nprint(config.get("section.unknown", default=False))\n>>> False\n\n# Setting, deleting, and checking if a key exists is just as easy.\nprint(config.set("section.first_key", 10))\n>>> True\n\nprint(config.delete("section.third_key"))\n>>> True\n\nprint(config.has("section.third_key"))\n>>> False\n\n# We can also convert the entire configuration file to a string.\nprint(config.stringify())\n>>> \'[section]\\nfirst_key = 5\\nsecond_key = blah\\nthird_key = true\\n\\n\'\n\n# Lastly, we need to make sure we save our changes. Nothing is written\n# out until we do so.\nprint(config.save())\n>>> True\n\n# If we have, say, a default config file and a user config file, we can easily\n# restore default one. We can specify the file path to it.\nprint(config.restore_original(original_file_path=ORIGINAL_CONFIG_PATH))\n>>> True\n\n# Otherwise, a config.original.ini file will automatically be looked for in the\n# current directory (because our configuration file we passed in was \n# named config.ini).\nprint(config.restore_original())\n>>> True\n```\n\n##  Documentation\n\nFull documentation and API reference is available at https://config-file.readthedocs.io\n\n## License\n\nThe [MIT](https://github.com/eugenetriguba/config-file/blob/master/LICENSE) License.',
    'author': 'Eugene Triguba',
    'author_email': 'eugenetriguba@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/eugenetriguba/config_file',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
