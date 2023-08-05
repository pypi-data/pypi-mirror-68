# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['calamus']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.5.1,<4.0.0', 'pyld>=2.0.2,<3.0.0']

setup_kwargs = {
    'name': 'calamus',
    'version': '0.1.2',
    'description': 'calamus is a library built on top of marshmallow to allow (de-)Serialization of Python classes to Json-LD.',
    'long_description': '..\n    Copyright 2017-2020 - Swiss Data Science Center (SDSC)\n    A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and\n    Eidgenössische Technische Hochschule Zürich (ETHZ).\n\n    Licensed under the Apache License, Version 2.0 (the "License");\n    you may not use this file except in compliance with the License.\n    You may obtain a copy of the License at\n\n        http://www.apache.org/licenses/LICENSE-2.0\n\n    Unless required by applicable law or agreed to in writing, software\n    distributed under the License is distributed on an "AS IS" BASIS,\n    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n    See the License for the specific language governing permissions and\n    limitations under the License.\n\n.. image:: https://github.com/SwissDataScienceCenter/calamus/blob/master/docs/reed.png?raw=true\n   :scale: 50\n   :align: center\n\n==================================================\n calamus: Json-LD Serialization Libary for Python\n==================================================\n\ncalamus is a library built on top of marshmallow to allow (de-)Serialization\nof Python classes to Json-LD\n\n\nInstallation\n============\n\ncalamus releases and development versions are available from `PyPI\n<https://pypi.org/project/calamus/>`_. You can install it using any tool that\nknows how to handle PyPI packages.\n\nWith pip:\n\n::\n\n    $ pip install calamus\n\n\nUsage\n=====\n\nAssuming you have a class like\n\n::\n\n    class Book:\n        def __init__(self, _id, name):\n            self._id = _id\n            self.name = name\n\nDeclare schemas\n---------------\nYou can declare a schema for serialization like\n::\n\n    schema = fields.Namespace("http://schema.org/")\n\n    class BookSchema(JsonLDSchema):\n        _id = fields.Id()\n        name = fields.String(schema.name)\n\n        class Meta:\n            rdf_type = schema.Book\n            model = Book\n\nThe ``fields.Namespace`` class represents an ontology namespace.\n\nMake sure to set ``rdf_type`` to the RDF triple type you want get and\n``model`` to the python class this schema applies to.\n\nSerializing objects ("Dumping")\n-------------------------------\n\nYou can now easily serialize python classes to Json-LD\n\n::\n\n    book = Book(_id="http://example.com/books/1", name="Ilias")\n    jsonld_dict = BookSchema().dump(book)\n    #{\n    #    "@id": "http://example.com/books/1",\n    #    "@type": "http://schema.org/Book",\n    #    "http://schema.org/name": "Ilias",\n    #}\n\n    jsonld_string = BookSchema().dumps(book)\n    #\'{"@id": "http://example.com/books/1", "http://schema.org/name": "Ilias", "@type": "http://schema.org/Book"}\')\n\nDeserializing objects ("Loading")\n---------------------------------\n\nYou can also easily deserialize Json-LD to python objects\n\n::\n\n    data = {\n        "@id": "http://example.com/books/1",\n        "@type": "http://schema.org/Book",\n        "http://schema.org/name": "Ilias",\n    }\n    book = BookSchema().load(data)\n    #<Book(_id="http://example.com/books/1", name="Ilias")>\n',
    'author': 'Swiss Data Science Center',
    'author_email': 'contact@datascience.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SwissDataScienceCenter/calamus/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
