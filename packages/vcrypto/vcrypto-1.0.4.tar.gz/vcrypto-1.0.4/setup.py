# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vcrypto']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=2.9.2,<3.0.0']

setup_kwargs = {
    'name': 'vcrypto',
    'version': '1.0.4',
    'description': 'Utility to easily store password/secrets',
    'long_description': '# Palette Material Design\n[![Build Status](https://travis-ci.com/villoro/v-crypt.svg?branch=master)](https://travis-ci.com/villoro/v-crypt)\n[![codecov](https://codecov.io/gh/villoro/v-crypt/branch/master/graph/badge.svg)](https://codecov.io/gh/villoro/v-crypt)\n\nUtility to easily store password/secrets. It uses `Fernet` from the [cryptography](https://cryptography.io/en/latest/) module instead of reinventing the wheel.\n\nFernet is a symmetric encryption that uses 128-bit AES in CBC mode and PKCS7 padding with HMAC using SHA256 for authentication. You can read more about it [here](https://medium.com/coinmonks/if-youre-struggling-picking-a-crypto-suite-fernet-may-be-the-answer-95196c0fec4b).\n\n## Why v-crypt?\nIt is always annoying to deal with secrets and passwords in python especially if you work with other people. What we found that worked best for us was:\n\n* Create one master private password (ignored from git)\n* Have dict-like file with the rest of passwords encrypted\n\nThis module provides the class `Cipher` to handle that easily.\n\nThe idea behind this module is to be able to **create a `json` or `yaml` with encrypted secrets**. The keys will be public but the values won\'t. This way you can **store the dictionary of secrets in git** and easily share them with other people working in the same project. You will only need to **share the `master.password` once**. And all the other passwords/secrets will be tracked with git.\n\n## Installation\n\nYou can install it with pip by running:\n\n    pip install v-crypt\n\n## Usage\n\n```python\nfrom v_crypt import Cipher\n\n# Create a cipher instance\ncipher = Cipher()\n\n# Create a new master password\ncipher.create_password()\n\n# Store a secret\ncipher.save_secret("secret", "I like python")\n\n# Retrive a secret\ncipher.get_secret("secret")\n```\n\n### Customization\n\nThere are three paramaters to customize the cipher:\n\n1. **secrets_file:** path of the file with secrets. Can be a `json` or `yaml`.\n2. **filename_master_password:** path of the file with the master password\n3. **environ_var_name:** if passed it allows to read the master password from an environ var.\n\n> For `yaml` you need to install `pyyaml`\n\nFor example you could do:\n\n```python\ncipher = Cipher(secrets_file="data/secrets.yaml", filename_master_password="data/master.secret")\n```\n\nThis will allow you to store both the `master.password` and `secrets.yaml` in the folder `data`.\n\nThere is not much more customization since the idea is to keep it simple.\n\n### Integrating it in other projects\nWe usually have one or more python files with utilities, for example `utilities.py`.\n\nTo use v_crypt we initiallize the `cipher` there and then create a `get_secret` dummy function that will call the cipher.\n\n```python\nfrom v_crypt import Cipher\n\ncipher = Cipher(secrets_file="data/secrets.yaml", filename_master_password="data/master.secret")\n\ndef get_secret(key):\n    return cipher.get_secret(key)\n```\n\nThen you can use it elsewhere with:\n\n```python\nimport utilities as u\n\nu.get_secret("secret")\n```\n\n## Development\n\nThis package relies on [poetry](https://villoro.com/post/poetry) and `pre-commit`. In order to develop you need to install both libraries with:\n\n```sh\npip install poetry pre-commit\npoetry install\npre-commit install\n```\n\nThen you need to add `poetry run` before any python shell command. For example:\n\n```sh\n# DO\npoetry run python master.py\n\n# don\'t do\npython master.py\n```\n\n## Authors\n* [Arnau Villoro](https://villoro.com)\n\n## License\nThe content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).\n\n## Nomenclature\nBranches and commits use some prefixes to keep everything better organized.\n\n### Branches\n* **f/:** features\n* **r/:** releases\n* **h/:** hotfixs\n\n### Commits\n* **[NEW]** new features\n* **[FIX]** fixes\n* **[REF]** refactors\n* **[PYL]** [pylint](https://www.pylint.org/) improvements\n* **[TST]** tests\n',
    'author': 'Arnau Villoro',
    'author_email': 'arnau@villoro.com',
    'maintainer': 'Arnau Villoro',
    'maintainer_email': 'arnau@villoro.com',
    'url': 'https://github.com/villoro/vcrypto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
