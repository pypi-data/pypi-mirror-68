# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_require']
install_requires = \
['cmdy', 'pyppl>=3.0.0,<4.0.0', 'pyppl_annotate']

entry_points = \
{'pyppl': ['pyppl_require = pyppl_require']}

setup_kwargs = {
    'name': 'pyppl-require',
    'version': '0.0.4',
    'description': 'Requirement manager for processes of PyPPL',
    'long_description': '# pyppl_require\n\nRequirement manager for [PyPPL](https://github.com/pwwang/PyPPL).\n\n## Installation\nIt requires [pyppl_annotate](https://github.com/pwwang/pyppl_annotate).\n```shell\npip install pyppl_require\n```\n\n## Usage\n```shell\n> pyppl require\nDescription:\n  Process requirement manager\n\nUsage:\n  pyppl require <--pipe AUTO> [OPTIONS]\n\nRequired options:\n  -p, --pipe <AUTO>     - The pipeline script.\n\nOptional options:\n  --install <AUTO>      - Install the requirements.\n                          You can specify a directory (default: $HOME/bin) to install the \\\n                          requirements.\n                          Default: None\n  -h, -H, --help        - Show help message and exit.\n```\n\nTo allow your processes to be analyzed, you have to put a section in annotate using `toml` format:\n```python\npXXX.config.annotate = """\n@requires:\n  [bedtools]\n  validate: "bedtools --version"\n  install: "conda install -c bioconda bedtools"\n  # other annotations\n"""\n```\n\nIf you want define those commands using process properties and aggrs:\n```python\npXXX.config.annotate = """\n@requires:\n  [bedtools]\n  validate: "{{args.bedtools}} --version"\n  install: "conda install -c bioconda bedtools"\n  # other annotations\n"""\n```\n\nInstall to a specify directory:\n\n```python\npXXX.config.annotate = """\n@requires:\n  [bedtools]\n  validate: "{{args.bedtools}} --version"\n  install: "conda install -c bioconda bedtools; ln -s $(which bedtools) {{bindir}}/bedtools"\n  # other annotations\n"""\n```\n\n`{{bindir}}` will be the directory passed to the command line.\n```shell\npyppl require --pipe <your pipeline> --install </path/to/bin>\n```\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pyppl_require',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
