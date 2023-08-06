# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphene_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['graphene>=2.1.8,<3.0.0', 'prometheus_client>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'graphene-prometheus',
    'version': '0.1.0',
    'description': 'Prometheus exporter middleware for the Graphene GraphQL framework.',
    'long_description': '# graphene-prometheus\n\n📊 Prometheus exporter middleware for the Graphene GraphQL framework.\n\n_This is still under development. Use at your own risk._\n\n## Usage\n\nInstall using `pip install graphene-prometheus` or `poetry add graphene-prometheus`.\n\n### Graphene\n\n```python\nimport graphene_prometheus\n\nschema.execute("THE QUERY", middleware=[graphene_prometheus.PrometheusMiddleware()])\n```\n\nSee https://docs.graphene-python.org/en/latest/execution/middleware/#middleware for more information.\n\n### Django\n\nIn `settings.py`:\n\n```python\nGRAPHENE = {\n    "MIDDLEWARE": ["graphene_prometheus.PrometheusMiddleware"],\n}\n```\n\nSee https://docs.graphene-python.org/projects/django/en/latest/settings/#middleware for more information.\n\n### FastAPI / Starlette\n\nComing soon.\n',
    'author': 'Courtsite',
    'author_email': 'tech+os@courtsite.dev',
    'maintainer': 'Ian L.',
    'maintainer_email': 'ian+os@courtsite.dev',
    'url': 'https://github.com/courtsite/graphene-prometheus',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
