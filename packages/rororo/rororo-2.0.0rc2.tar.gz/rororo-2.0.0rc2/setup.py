# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rororo', 'rororo.openapi']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.1,<6.0',
 'aiohttp-middlewares>=1.1.0,<2.0.0',
 'aiohttp>=3.5,<4.0',
 'attrs>=19.1,<20.0',
 'email-validator>=1.0.5,<2.0.0',
 'environ-config>=20.1.0,<21.0.0',
 'isodate>=0.6.0,<0.7.0',
 'openapi-core>=0.13.3,<0.14.0',
 'pyrsistent>=0.16.0,<0.17.0']

extras_require = \
{':python_version < "3.8"': ['typing-extensions>=3.7.4,<4.0.0']}

setup_kwargs = {
    'name': 'rororo',
    'version': '2.0.0rc2',
    'description': 'OpenAPI 3 schema support for aiohttp.web applications.',
    'long_description': '======\nrororo\n======\n\n.. image:: https://github.com/playpauseandstop/rororo/workflows/ci/badge.svg\n    :target: https://github.com/playpauseandstop/rororo/actions?query=workflow%3A%22ci%22\n    :alt: CI Workflow\n\n.. image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n    :target: https://github.com/pre-commit/pre-commit\n    :alt: pre-commit\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n    :alt: black\n\n.. image:: https://img.shields.io/pypi/v/rororo.svg\n    :target: https://pypi.org/project/rororo/\n    :alt: Latest Version\n\n.. image:: https://img.shields.io/pypi/pyversions/rororo.svg\n    :target: https://pypi.org/project/rororo/\n    :alt: Python versions\n\n.. image:: https://img.shields.io/pypi/l/rororo.svg\n    :target: https://github.com/playpauseandstop/rororo/blob/master/LICENSE\n    :alt: BSD License\n\n.. image:: https://coveralls.io/repos/playpauseandstop/rororo/badge.svg?branch=master&service=github\n    :target: https://coveralls.io/github/playpauseandstop/rororo\n    :alt: Coverage\n\n.. image:: https://readthedocs.org/projects/rororo/badge/?version=latest\n    :target: https://rororo.readthedocs.io/\n    :alt: Documentation\n\n`OpenAPI 3 <https://spec.openapis.org/oas/v3.0.2>`_ schema support\nfor `aiohttp.web <https://aiohttp.readthedocs.io/en/stable/web.html>`_\napplications.\n\nAs well as bunch other utilities to build effective web applications with\nPython 3 & ``aiohttp.web``.\n\n* Works on Python 3.6+\n* BSD licensed\n* Source, issues, and pull requests `on GitHub\n  <https://github.com/playpauseandstop/rororo>`_\n\nImportant\n=========\n\n**2.0.0** version still in development. To install it use,\n\n.. code-block:: bash\n\n    pip install rororo==2.0.0rc1\n\nor,\n\n.. code-block:: bash\n\n    poetry add rororo==2.0.0rc1\n\nQuick Start\n===========\n\n``rororo`` relies on valid OpenAPI schema file (both JSON or YAML formats\nsupported).\n\nExample below, illustrates on how to handle operation ``hello_world`` from\n`openapi.yaml <https://github.com/playpauseandstop/rororo/blob/master/tests/openapi.yaml>`_\nschema file.\n\n.. code-block:: python\n\n    from pathlib import Path\n    from typing import List\n\n    from aiohttp import web\n    from rororo import (\n        openapi_context,\n        OperationTableDef,\n        setup_openapi,\n    )\n\n\n    operations = OperationTableDef()\n\n\n    @operations.register\n    async def hello_world(request: web.Request) -> web.Response:\n        with openapi_context(request) as context:\n            name = context.parameters.query.get("name", "world")\n            return web.json_response({"message": f"Hello, {name}!"})\n\n\n    def create_app(argv: List[str] = None) -> web.Application:\n        app = web.Application()\n        setup_openapi(\n            app,\n            Path(__file__).parent / "openapi.yaml",\n            operations,\n            route_prefix="/api",\n        )\n        return app\n\nClass Based Views\n-----------------\n\n``rororo`` supports `class based views <https://docs.aiohttp.org/en/stable/web_quickstart.html#aiohttp-web-class-based-views>`_\nas well. `Todo-Backend <https://github.com/playpauseandstop/rororo/tree/master/examples/todobackend>`_\nexample illustrates how to use class based views for OpenAPI handlers.\n\nIn snippet below, ``rororo`` expects that OpenAPI schema contains operation ID\n``UserView.get``,\n\n.. code-block:: python\n\n    @operations.register\n    class UserView(web.View):\n        async def get(self) -> web.Response:\n            ...\n\nMore Examples\n-------------\n\nCheck\n`examples <https://github.com/playpauseandstop/rororo/tree/master/examples>`_\nfolder to see other examples on how to use OpenAPI 3 schemas with aiohttp.web\napplications.\n',
    'author': 'Igor Davydenko',
    'author_email': 'iam@igordavydenko.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://igordavydenko.com/projects.html#rororo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
