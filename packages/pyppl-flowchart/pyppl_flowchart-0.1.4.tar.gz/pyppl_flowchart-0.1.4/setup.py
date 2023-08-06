# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pyppl_flowchart']
install_requires = \
['graphviz>=0.11,<0.12', 'pyppl']

entry_points = \
{'pyppl': ['pyppl_flowchart = pyppl_flowchart']}

setup_kwargs = {
    'name': 'pyppl-flowchart',
    'version': '0.1.4',
    'description': 'Generating flowchart for PyPPL',
    'long_description': '# pyppl_flowchart\n\n[![Pypi][3]][4] [![Github][5]][6] [![PyPPL][7]][1] [![PythonVers][8]][4] [![Travis building][10]][11] [![Codacy][12]][13] [![Codacy coverage][14]][13]\n\nFlowchart generator for [PyPPL](https://github.com/pwwang/PyPPL).\n\n## Installation\n```shell\npip install pyppl_flowchart\n```\n\n## Usage\n\n### Generating flowchart for your pipeline\n```python\n# process definition\n\nPyPPL().start(...).flowchart(fcfile = \'/path/to/your/flowchart.svg\').run()\n```\n\n### Hiding some processes from flowchart\n```python\n# Turn\n# p1 -> p2 -> p3 -> p4 -> p5\np3.config.flowchart_hide = True\n# into:\n# p1 -> p2 -> p4 -> p5\n```\n\n### Theming\n\nIn your configuration:\n```toml\n[default.flowchart]\ntheme = "dark"\n\n# other configuration\n```\n\nWe have two builtin themes: `default` and `dark`:\n\n![default](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl.png)\n\n![dark](https://pyppl.readthedocs.io/en/latest/drawFlowchart_pyppl_dark.png)\n\nYou can also default your own theme in the configuration:\n```toml\n[default.flowchart.theme]\nbase = {\n    shape = "box",\n    style = "rounded,filled",\n    fillcolor = "#ffffff",\n    color = "#000000",\n    fontcolor = "#000000"\n}\nstart = { style = "filled", color = "#259229" }\nend = { style = "filled", color = "#d63125" }\nprocset = { style = "filled", color: "#eeeeee" }\nedge = {}\nedge_hidden = { style = "dashed" } # for links with hidden processes\n```\n\n[1]: https://github.com/pwwang/PyPPL\n[2]: https://pyppl_flowchart.readthedocs.io/en/latest/\n[3]: https://img.shields.io/pypi/v/pyppl_flowchart?style=flat-square\n[4]: https://pypi.org/project/pyppl_flowchart/\n[5]: https://img.shields.io/github/tag/pwwang/pyppl_flowchart?style=flat-square\n[6]: https://github.com/pwwang/pyppl_flowchart\n[7]: https://img.shields.io/github/tag/pwwang/pyppl?label=PyPPL&style=flat-square\n[8]: https://img.shields.io/pypi/pyversions/pyppl_flowchart?style=flat-square\n[10]: https://img.shields.io/travis/pwwang/pyppl_flowchart?style=flat-square\n[11]: https://travis-ci.org/pwwang/pyppl_flowchart\n[12]: https://img.shields.io/codeclimate/maintainability-percentage/pwwang/pyppl_flowchart?style=flat-square\n[13]: https://app.codacy.com/project/pwwang/pyppl_flowchart/dashboard\n[14]: https://img.shields.io/codeclimate/coverage/pwwang/pyppl_flowchart?style=flat-square\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pwwang/pyppl_flowchart',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
