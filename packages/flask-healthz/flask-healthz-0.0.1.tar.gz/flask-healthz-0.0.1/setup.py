# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flask_healthz']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=1.1.1,<2.0.0']

setup_kwargs = {
    'name': 'flask-healthz',
    'version': '0.0.1',
    'description': 'A simple module to allow you to easily add health endpoints to your Flask application',
    'long_description': '# Flask-Healthz\n\nDefine endpoints in your Flask application that Kubernetes can use as\n[liveness and readiness probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/).\n\n## Setting it up\n\nRegister the blueprint on your Flask application:\n\n```python\nfrom flask import Flask\nfrom flask_healthz import healthz\n\napp = Flask(__name__)\napp.register_blueprint(healthz, url_prefix="/healthz")\n```\n\nDefine the functions you want to use to check health. To signal an error, raise `flask_healthz.HealthError`.\n\n```python\nfrom flask_healthz import HealthError\n\ndef liveness():\n    pass\n\ndef readiness():\n    try:\n        connect_database()\n    except Exception:\n        raise HealthError("Can\'t connect to the database")\n```\n\nNow point to those functions in the Flask configuration:\n\n```python\nHEALTHZ = {\n    "live": "yourapp.checks.liveness",\n    "ready": "yourapp.checks.readiness",\n}\n```\n\nIt is possible to directly set callables in the configuration, so you could write something like:\n\n```python\nHEALTHZ = {\n    "live": lambda: None,\n}\n```\n\nCheck that the endpoints actually work:\n\n```\n$ curl http://localhost/yourapp/healthz/live\nOK\n$ curl http://localhost/yourapp/healthz/ready\nOK\n```\n\nNow your can configure Kubernetes to check for those endpoints.\n\n## License\n\nCopyright 2020 Red Hat\n\nFlask-Healthz is licensed under the same license as Flask itself: BSD 3-clause.\n',
    'author': 'Fedora Infrastructure',
    'author_email': 'admin@fedoraproject.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/fedora-infra/flask-healthz',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
