# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gigabloat', 'gigabloat.coverter', 'gigabloat.gatherer']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'humanize>=2.4.0,<3.0.0', 'tabulate>=0.8.7,<0.9.0']

setup_kwargs = {
    'name': 'gigabloat',
    'version': '0.1.1',
    'description': 'Tool to get general file and directory stats',
    'long_description': '# Gigabloat File Manager\n\nNote: this project is in it\'s baby stage, do not use it, like at all. Come back later to see how it goes.\n\n## Development\n\nFor now Gigabloat was developed mostly on MacOS (Catalina), therefore I can only provide clear instructions for development related to MacOS, although I suppose it would be very similar on Linux and on Windows.\n\n### MacOS\n\nThis project relies on the follwoing packages during development.  \n\n- [PyEnv](https://github.com/pyenv/pyenv) - used to switch to the specific python version this package requires\n- [Poetry](https://python-poetry.org/) - used as a dependency management solution.\n- [Black](https://github.com/psf/black) - code formatter.\n\n0. Clone/Fork this repo\n1. Install PyEnv and Poetry (see their repos on instructions, Gigabloat needs just basic installation)\n2. You need to add this line to zhrc, otherwise you\'ll see some errors while using Poetry   \n`eval "$(pyenv init -)"`\n3. In the root folder of this repo specify python version to use with PyEnv (this will update .python-version file)  \n```shell\npyenv install 3.8.2\npyenv local 3.8.2\n```\n4. Run `poetry install`\n5. Configure VScode workspace settings to use black and pylint  \n    5.1. Get poetry virtual env path `poetry env info --path`  \n    5.2. Create `.vscode` folder with `settings.json` file in it (in root of this project) and add the following lines  \n    ```json\n    {\n        "python.formatting.blackPath": "<poetry_env_path>/bin/black",\n        "python.formatting.provider": "black",\n        "python.linting.pylintPath": "<poetry_env_path>/bin/pylint"\n    }\n    ```\n\n## General algorithm\n_This section is just for me to keep track of stuff, experimental/unfinished/uncertain_\n\n`scanDirectory` is called with directory to scan.\nfor it we:\n- create dummy `Directory` with just path name for now (and parent if provided)\n1. get list of files (in dir, no subdirs)\n    - create `File` objects for each\n    - increment total files in scan with number of these files\n2. get list of subdirs\n    - recursively apply `scanDirectory` again\n3. update dummy `Directory` with `File`s and sub`Directories`\n4. add directory to `self.directories` list\n5. if we end up at this point and figure out that we\'re in root\n    - assing `self.root_directory` for easy access\n6. return the `Directory` to be used in step 2\n\n## Proposed CLI interface\n\nCommand `gigabloat scan`  \nGet general stats  \nOptions:  \n`--dir <directory>` @required  \ndirectory to scan  \n`--json`  \n_Not implemented yet_  \nprovide json output  \n`--table`  \n_Not implemented yet_  \nprovide tabulat output  \n`--pyobj`  \n_Not implemented yet_  \nprovide pyobj output  \n`--nofile`  \n_Not implemented yet_  \ndo not save report file after scan is finished  \n\nCommand `gigabloat filter`  \n_Not implemented yet_  \nFilter some specific stat  \n`--f <file>` @required  \nspecify report file  \n`--ext <ext>`  \ngive stats for files with .<ext> extension  \n`--bd`  \nshow biggest directory (by size)  \n`--bf`  \nshow biggest file (by size)  \n`--photos`  \nshow amount and size of photos  \n`--videos`  \nshow amount and size of videos  \n`--audio`  \nshow amount and size of audio  \n`--media`  \nshow amount and size of media files (phtos, images, audio)  \n',
    'author': 'Artem Kolichenkov',
    'author_email': 'artem@kolichenkov.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ArtemKolichenkov/gigabloat_scanner',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.2,<4.0.0',
}


setup(**setup_kwargs)
