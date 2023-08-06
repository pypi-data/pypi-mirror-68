# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simulert', 'simulert.handlers', 'simulert.tests.unit']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.0,<2.0', 'slackclient>=2.5,<3.0']

setup_kwargs = {
    'name': 'simulert',
    'version': '0.2.0',
    'description': 'A package to provide useful functionality for sending alerts about running simulations.',
    'long_description': '# Simulert\n![Run Pytest and Lint](https://github.com/JJMinton/simulert/workflows/Run%20Pytest%20and%20Lint/badge.svg)\n\nHow often do your simulations fail moments after you close the terminal and head home\nfor the evening? Do you repeatedly check on your simulations to see how they\'re doing?\nHave you ever left a long simulations for days longer than it needed?\nThis package is for configuring alerts for your simulations so you get told what\'s\nhappened, when it\'s happened and in the format that best suits you.\n\n## Installation\nAn early release has been made available onn Pypi so install via pip:\n`pip install simulert`. Or for the latest, clone this repository and adding it as a\ndevelopment package with either `pip install -e /path/to/simulert` or\n`conda develop /path/to/simulert`.\n\n## Usage\nThis package is architected similarly to Python\'s built-in logging package.\nAn `Alerter` class is instantiated with `getAlerter()` and is triggered to send\nalerts to all the handlers registered with it.\n\nCurrent handlers include a logger (default), an emailer and a slack client.\n\nThe `Alerter` currently provides two ways to trigger alerts: most simply, calling the\n`alert` method with a message; and possibly more conveniently, with the\n`simulation_alert` context wrapping the simulation code.\n\n## Environment variable configuration\nThe handlers will take default arguments from environment variables so that this package\ncan be configured globally for the fewest lines to alerts.\n\n##### Email hander:\n`SIMULERT_EMAIL_HOST`: the host address of the email server to send from.\n`SIMULERT_EMAIL_PORT`: the connection port of the email server to send from.\n`SIMULERT_EMAIL_AUTHENTICATION`: comma-separated username and password to authenticate\n    to the email server.\n`SIMULERT_EMAIL_SENDER`: comma-separated sender name and email address\n`SIMULERT_EMAIL_RECIPIENT`: comma-separated receiver name and email address\n\n\n##### Slack handler:\n`SIMULERT_SLACK_TOKEN`: the token for the slack-bot used to send messages from.\n`SIMULERT_SLACK_USERNAME`: the username of the slack user to send messages to.\n\n\n## Example\nThe verbose and transparent example:\n```python\nfrom simulert import getAlerter\nfrom simulert.handlers import Emailer, Slacker\n\nemailer = Emailer(\n    "username",\n    "password",\n    ("Simulations", "noreply_simulations@company.com"),\n    ("Data scientist", "scientist@company.com"),\n    "smtp.mailserver.company.com",\n)\nslacker = Slacker("slack_app_token", "username")\nalerter = getAlerter().add_handler(emailer).add_handler(slacker)\nalerter.alert("Something special has happened in my code")\n```\nwhich will send "Something special has happened in my code" to the log files, to\n`scientist@company.com` and to `@username` on slack.\n\nThe convenient example, with environment variables configured:\n```python\nfrom simulert import getAlerter\nfrom simulert.handlers import Slacker\nalerter = getAlerter("BigSims").add_handler(Slacker())\nwith alerter.simulation_alert("super dooper sim"):\n    run_simulation()\n```\nwhich will send "BigSims: super dooper sim has completed without error." via slack once\n`run_simulation()` has completed.\n\n## TODO\n1. Test logs.py\n1. Tidy up pyproject.toml to include only necessary files\n1. Add a changelog\n1. Add a logging handler as an event source.\n',
    'author': 'Jeremy Minton',
    'author_email': 'jeremyminton@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jjminton/simulert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
