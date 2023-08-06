# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['spado']
install_requires = \
['boto3>=1.13.8,<2.0.0']

setup_kwargs = {
    'name': 'spado',
    'version': '0.1.3',
    'description': 'Client simplifying and abstracting common operations for digital ocean spaces.',
    'long_description': '# Spado (Digital Ocean spaces client)\n\nSpado is a simple client to interact with Digital Ocean\'s spaces. It\'s built on top of the AWS python 3 framwork boto3 and aims to simplify and streamline common storage operations.\n\n\n## Usage\n\nInitialization\n```py\nfrom spado import Spado\n\n# Required params\nparams: dict = {\n    space_name: "space_name",\n    region_name: "region_name",\n    endpoint: "endpoint",\n    spaces_key: "spaces_key",\n    spaces_secret: "space_token"\n}\n\n_client: Spado = Spado(**params)\n```\n\n\nMethod usage\n```py\n_client.upload(\n    filepath="Samples/sample.jpg",  # Folder/filename.extension\n    file=open(\'/tmp/sample.jpg\', \'rb\'),  # File as <bytes>\n    acl="private"\n)\n\n_client.download(\n    spaces_fpath=\'Samples/sample.jpg\',\n    local_fpath=\'/tmp/sample2.jpg\'\n)\n```\n\n### CRUD methods:\n- upload: Adds a new file to spaces\n- download_url: Returns a download link for a file in spaces\n- download: Downloads the file directly  to given filepath\n- replace: Replaces a file in spaces with a new one\n- delete: Deletes a file in spaces\n\n### Helper methods:\n- list_files: Returns a list of files in default space\n- list_spaces: Returns a list of available spaces',
    'author': 'Alex Pedersen',
    'author_email': 'me@alexpdr.dev',
    'maintainer': 'Alex Pedersen',
    'maintainer_email': 'me@alexpdr.dev',
    'url': 'https://github.com/alexpdr/spado',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
