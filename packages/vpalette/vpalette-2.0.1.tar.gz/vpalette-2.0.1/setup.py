# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['vpalette']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'vpalette',
    'version': '2.0.1',
    'description': 'Utility to easily use material design colors',
    'long_description': '# Palettes\n[![Build Status](https://travis-ci.com/villoro/v-palette.svg?branch=master)](https://travis-ci.com/villoro/v-palette)\n\nUtility to easily use palettes\n\n## Colors\n\nThere are two palettes **material** and **flat**.\n\n### Material Colors\n<img src="https://raw.githubusercontent.com/villoro/v-palette/master/assets/material_grid.svg?sanitize=true">\n\nYou can view them in a [svg file](https://github.com/villoro/v-palette/blob/master/assets/material_grid.svg). More info at [material.io](https://material.io/design/color/the-color-system.html#color-usage-palettes).\n\n### Flat Colors\n<img src="https://raw.githubusercontent.com/villoro/v-palette/master/assets/flat_grid.svg?sanitize=true">\n\nYou can view them in a [svg file](https://github.com/villoro/v-palette/blob/master/assets/flat_grid.svg). More info at [html color codes](https://htmlcolorcodes.com/color-chart/flat-design-color-chart/).\n\n## Installation\n\nYou can install it with pip by running:\n\n    pip install v-palette\n\n\n## Usage\n\nYou can retrive one color or a list of colors using `get_colors` function:\n\n```python\nfrom v_palette import get_colors\n\n# 1. Retrive one color\nget_colors(("red", 100)) # out: \'#FFCDD2\'\n\n# 2. Retrive some colors\nget_colors([("red", 100), ("blue", 100)]) # out: [\'#FFCDD2\', \'#BBDEFB\']\n\n# 3. Retrive colors from others palettes\nget_colors([("emerald", 100), ("silver", 100)]) # out: [\'#D5F5E3\', \'#F2F3F4\']\nget_colors([("emerald", 100), ("silver", 100)], palette="flat") # out: [\'#D5F5E3\', \'#F2F3F4\']\n```\n\n> The parameter `palette` is not necessary if the color you want is not present in the material palette. Since if the color is not found in the default palette it will look at the others palettes.\n\n## Development\n\nThis package relies on [poetry](https://villoro.com/post/poetry) and `pre-commit`. In order to develop you need to install both libraries with:\n\n```sh\npip install poetry pre-commit\npoetry install\npre-commit install\n```\n\nThen you need to add `poetry run` before any python shell command. For example:\n\n```sh\n# DO\npoetry run python master.py\n\n# don\'t do\npython master.py\n```\n\n## Authors\n* [Arnau Villoro](https://villoro.com)\n\n## License\nThe content of this repository is licensed under a [MIT](https://opensource.org/licenses/MIT).\n\n## Nomenclature\nBranches and commits use some prefixes to keep everything better organized.\n\n### Branches\n* **f/:** features\n* **r/:** releases\n* **h/:** hotfixs\n\n### Commits\n* **[NEW]** new features\n* **[FIX]** fixes\n* **[REF]** refactors\n* **[PYL]** [pylint](https://www.pylint.org/) improvements\n* **[TST]** tests\n',
    'author': 'Arnau Villoro',
    'author_email': 'arnau@villoro.com',
    'maintainer': 'Arnau Villoro',
    'maintainer_email': 'arnau@villoro.com',
    'url': 'https://github.com/villoro/vpalette',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
