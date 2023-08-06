# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mroll', 'mroll.templates']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0', 'pymonetdb>=1.3.1,<2.0.0']

entry_points = \
{'console_scripts': ['mroll = mroll.commands:cli']}

setup_kwargs = {
    'name': 'mroll',
    'version': '0.1.0',
    'description': 'monetdb migration tool',
    'long_description': '# Mroll migration tool\nDatabase migration tool around MonetDB and pymonetdb.\n\n![mroll ci](https://github.com/MonetDBSolutions/mroll/workflows/ci_workflow/badge.svg)\n\n## Install\n\nInstall mroll from PyPi\n\n```\n$ pip install mroll\n```\n\n## Usage\n\nWith MonetDB installed and running a project database, following commands can be used to set up migration \nprocess in your project.\n\n```\n$ mroll --help\nUsage: commands.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  all_revisions\n  config         Set up mroll configuration under $HOME/.config/mroll\n  downgrade      Downgrades to the previous revison or to the revision with...\n  history        Shows applied revisions.\n  init           Creates mroll_revisions tbl.\n  new_revisions  Shows revisions not applied yet\n  revision       Creates new revision file from a template.\n  rollback       Downgrades to the previous revision.\n  setup          Set up work directory.\n  show\n  upgrade        Applies all revisions not yet applied in work dir.\n  version\n\n```\nTo set working directory use setup command.\n```\nmroll setup --help\n```\n\n, use  -p/--path option to specify location. For an example lets use "/tmp/migration" location.\n\n```\n$ mroll setup -p "/tmp/migrations"\nok\n```\nIf no path specified defaults to setting "migrations" folder in current working directory.\nTo update/set mroll configuartion use \'config\' command. For example to update configuration setting for working directory path run.\n```\nmroll config -p <workdir_path>\n```\n\nIn the working directory modify mroll.ini with specific connection options\n\n```\n$ vi /tmp/migrations/mroll.ini \n```\n, then run "init" command to create revisions table \n\n```\n$ mroll init\n```\ncreate first revision with brief description \n\n```\n$ mroll revision -m "create table foo"\nok\n$ mroll show all_revisions\n<Revision id=fe00de6bfa19 description=create table foo>\n```\nA new revison file was added under "/tmp/migrations/versions". Open and fill under "-- migration:upgrade" and "-- migration:downgrade" sections. \n\n```\n-- identifiers used by mroll\n-- id=fe00de6bfa19\n-- description=create tbl foo\n-- ts=2020-05-08T14:19:46.839773\n-- migration:upgrade\n\tcreate table foo (a string, b string);\n\talter table foo add constraint foo_pk primary key (a);\n-- migration:downgrade\n\tdrop table foo;\n\n```\nThen run "upgrade" command.\n\n```\n$ mroll upgrade\nDone\n```\nInspect what has being applied with "history" command\n\n```\n$ mroll history\n<Revision id=fe00de6bfa19 description=create tbl foo>\n```\n\nTo revert last applied revision run "rollback" command. That will run the sql under "migration:downgrade"\nsection.\n```\n$ mroll rollback \nRolling back id=fe00de6bfa19 description=create tbl foo ...\nDone\n```\n\n## Development\n* Developer notes\n\n~mroll~ is developed using [[https://python-poetry.org/][Poetry]], for dependency management and\npackaging.\n\n** Installation for development\nIn order to install ~mroll~ do the following:\n\n```\n  pip3 install --user poetry\n  PYTHON_BIN_PATH="$(python3 -m site --user-base)/bin"\n  export PATH="$PATH:$PYTHON_BIN_PATH"\n\n  git clone git@github.com:MonetDBSolutions/mroll.git\n  cd mroll\n  poetry install\n  poetry run mroll/commands.py --help\n```\nOn 30/04/2020 [[https://github.com/gijzelaerr/pymonetdb/releases/tag/1.3.1][pymonetdb 1.3.1]] was released, which includes a feature needed to\nconnect transparently to the MonetDB server. If you have installed the\ndevelopment version of ~mroll~, before that date you need to update:\n```\n  cd monetdb-pystethoscope\n  git pull\n  poetry update\n```\n, install project dependencies with\n\n```\npoetry install\n```\n, this will create virtual environment and install dependencies from poetry.lock file. Any of the above \ncommands then can be run with poetry\n\n```\npoetry run mroll/commands.py <command>\n```\n## Testing\nRun all unit tests\n```\nmake test\n```\n',
    'author': 'svetlin',
    'author_email': 'svetlin.stalinov@monetdbsolutions.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/MonetDBSolutions/mroll',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
