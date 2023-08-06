# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lion', 'lion.contrib']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'pytz>=2020.1,<2021.0']

setup_kwargs = {
    'name': 'lion',
    'version': '0.4.1',
    'description': 'Fast and flexible object mapping (serialization, marshalling)',
    'long_description': "# Lion\n\nLion is a very flexible yet fast library for mapping objects to\ndictionaries. It uses a declarative API and supports a query language\nsimilar to GraphQL. Unlike other serialization libraries it also\nallows to skip entire fields instead of having a ``null`` value\nin the dictionary.\n\nIt is inspired by libraries like [serpy][serpy], [marshmallow][marshmallow],\n[Django REST Framework][drf] and [Kim][kim].\n\n## Example\n\n```python\nimport lion\n\nclass GroupMapper(lion.Mapper):\n    id = lion.UUIDField()\n    name = lion.StrField()\n\nclass UserMapper(lion.Mapper):\n    id = lion.UUIDField()\n    email = lion.StrField(condition=lion.skip_empty)\n    first_name = lion.StrField()\n    last_name = lion.StrField()\n    groups = lion.ListField(GroupMapper)\n\nuser = User(\n    id=UUID('ad94d0e8-2526-4d9b-ad76-0fbffcf41033'),\n    email='john.doe@example.com',\n    first_name='John',\n    last_name='Doe',\n    groups=[\n        Group(\n            id=UUID('95a326fc-32e5-4d9b-a385-1ea1257d98da'),\n            name='Awesome people'\n        )\n    ]\n)\n\n# Dump all fields to a dictionary\nassert UserMapper().dump(user) == {\n    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',\n    'email': 'john.doe@example.com',\n    'first_name': 'John',\n    'last_name': 'Doe',\n    'groups': [\n        {\n            'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da',\n            'name': 'Awesome people'\n        }\n    ]\n}\n\n# Load user object from a dictionary\nassert user == UserMapper().load({\n    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',\n    'email': 'john.doe@example.com',\n    'first_name': 'John',\n    'last_name': 'Doe',\n    'groups': [\n        {\n            'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da',\n            'name': 'Awesome people'\n        }\n    ]\n})\n```\n\n## Query language\n\nBy using the GraphQL-like query language it is possible\nto dump and load only parts of a given structure:\n\n```python\n# Dump a subset of fields\nassert UserMapper('{id,email}').dump(user) == {\n    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',\n    'email': 'john.doe@example.com'\n}\n\n# Dump subset of a nested mapper\nassert UserMapper('{id,email,groups{id}}').dump(user) == {\n    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',\n    'email': 'john.doe@example.com',\n    'groups': [\n        'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da'\n    ]\n}\n```\n\n## Performance\n\nThe performance is somewhat slower than [serpy][serpy] but still far ahead of [marshmallow][marshmallow] and [Django REST Framework][drf].\n\n![Simple Benchmark](https://raw.githubusercontent.com/bikeshedder/lion/master/docs/benchmark-chart-simple.svg)\n\n![Complex Benchmark](https://raw.githubusercontent.com/bikeshedder/lion/master/docs/benchmark-chart-complex.svg)\n\n## Caveats\n\nLion also supports loading (serialization/marshalling) of data but currently does not perform any kind of validation. This is not a big deal if using Lion as part of a project which uses something like [connexion][connexion] which already performs validation using the provided OpenAPI specification file. Just be warned that loading an unvalidated data structure using Lion might result in somewhat weird looking data.\n\n\n[serpy]: https://pypi.python.org/pypi/serpy\n[marshmallow]: https://pypi.python.org/pypi/marshmallow/\n[kim]: https://pypi.python.org/pypi/py-kim\n[drf]: https://pypi.python.org/pypi/djangorestframework\n[connexion]: https://pypi.org/project/connexion/\n",
    'author': 'Michael P. Jung',
    'author_email': 'michael.jung@terreon.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bikeshedder/lion',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
