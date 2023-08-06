# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tailwind',
 'tailwind.app_template',
 'tailwind.management',
 'tailwind.management.commands']

package_data = \
{'': ['*'],
 'tailwind.app_template': ['static_src/*', 'static_src/src/*', 'templates/*']}

install_requires = \
['django>=2.2,<3.1']

setup_kwargs = {
    'name': 'django-tailwind',
    'version': '0.9.0',
    'description': 'Tailwind CSS Framework for Django projects',
    'long_description': '# The integration of Tailwind CSS framework with Django a.k.a. Django + Tailwind = ❤\n\n## Quick start\n\n1. Install the python package django-tailwind from pip\n\n   `pip install django-tailwind`\n\n   Alternatively, you can download or clone this repo and run `pip install -e .`.\n\n2. Add `tailwind` to INSTALLED_APPS in **settings.py**\n\n3. Create a tailwind-compatible Django-app, I like to call it `theme`:\n\n   `python manage.py tailwind init theme`\n\n4. Add your newly created `theme` app to INSTALLED_APPS in **settings.py**\n\n5. In settings.py, register tailwind app by adding the following string:\n\n   `TAILWIND_APP_NAME = \'theme\'`\n\n6. Run a command to install all necessary dependencies for tailwind css:\n\n   `python manage.py tailwind install`\n\n7. Now, go and start tailwind in dev mode:\n\n   `python manage.py tailwind start`\n\n8. Django Tailwind comes with a simple `base.html` template that can be found under\n   `yourtailwindappname/templates/base.html`. You can always extend it or delete it if you\n   have own layout.\n\n9. If you\'re not using `base.html` template provided with Django Tailwind, add `styles.min.css` to your own `base.html` template file:\n\n   ```html\n   <link\n     rel="stylesheet"\n     href="{% static \'css/styles.css\' %}"\n     type="text/css"\n   />\n   ```\n\n10) You should now be able to use Tailwind CSS classes in your html.\n\n11) To build a production version of CSS run:\n\n    `python manage.py tailwind build`.\n\n## NPM executable path configuration\n\nSometimes (especially on Windows), Python executable can\'t find `NPM` installed in the system.\nIn this case, you need to set `NPM` executable path in settings.py file manually (Linux/Mac):\n\n```python\nNPM_BIN_PATH = \'/usr/local/bin/npm\'\n```\n\nOn windows it might look like:\n\n```python\nNPM_BIN_PATH = r"C:\\Program Files\\nodejs\\npm.cmd"\n```\n\nPlease note that `NPM` path of your system may be different. Try to run `which npm` in your\ncommand line to get the path.\n\n## Bugs and suggestions\n\nIf you have found a bug, please use the issue tracker on GitHub.\n\n[https://github.com/timonweb/django-tailwind/issues](https://github.com/timonweb/django-tailwind/issues)\n\n2020 (c) [Tim Kamanin - A Full Stack Django Developer](https://timonweb.com)\n',
    'author': 'Tim Kamanin',
    'author_email': 'tim@timonweb.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/timonweb/django-tailwind',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<3.9',
}


setup(**setup_kwargs)
