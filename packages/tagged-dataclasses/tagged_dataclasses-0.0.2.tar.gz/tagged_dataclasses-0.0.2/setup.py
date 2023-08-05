# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tagged_dataclasses']

package_data = \
{'': ['*']}

install_requires = \
['typing_inspect>=0.6,<0.7']

extras_require = \
{':python_version < "3.7"': ['dataclasses>0.1']}

setup_kwargs = {
    'name': 'tagged-dataclasses',
    'version': '0.0.2',
    'description': '',
    'long_description': 'tagged_dataclasses\n==================\n\nSupport for tagged unions based on dataclasses via a lightweight mixin that is supported\nby mypy\n\n```python\nfrom typing import Optional\n\nfrom dataclasses import dataclass\n\nfrom tagged_dataclasses import TaggedUnion\n\nclass A:\n    pass\n\n@dataclass\nclass AB(A):\n    pass\n\n@dataclass\nclass AC(A):\n    pass\n\n@dataclass\nclass MyUnion(TaggedUnion[A]):\n    # Optional is not optional here (this is for better support in PyCharm)\n    first: Optional[AB] = None\n    second: Optional[AC] = None\n\nx = MyUnion.from_value(AB())\n\n# support for many variations\n\nif x.first is not None:\n    pass\nelif x.second is not None:\n    pass\n\n# other\n\nif x.kind == AB:\n    x.value()\nelif x.kind == AC:\n    x.value()\n\n\n\n```\n',
    'author': 'Andrey Cizov',
    'author_email': 'acizov@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/andreycizov/python-tagged_dataclasses',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
