# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.ldap',
 'aleksis.apps.ldap.management.commands',
 'aleksis.apps.ldap.migrations',
 'aleksis.apps.ldap.util']

package_data = \
{'': ['*'],
 'aleksis.apps.ldap': ['locale/*',
                       'locale/ar/LC_MESSAGES/django.po',
                       'locale/de_DE/LC_MESSAGES/django.po',
                       'locale/fr/LC_MESSAGES/django.po',
                       'locale/la/LC_MESSAGES/django.po',
                       'locale/nb_NO/LC_MESSAGES/django.po',
                       'locale/tr_TR/LC_MESSAGES/django.po',
                       'static/*']}

install_requires = \
['AlekSIS>=2.0a2,<3.0', 'django-ldapdb>=1.4.0,<2.0.0', 'tqdm>=4.44.1,<5.0.0']

setup_kwargs = {
    'name': 'aleksis-app-ldap',
    'version': '2.0a2',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp LDAP (General LDAP import/export)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp LDAP (General LDAP import/export)\n==================================================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\n* Configurable sync strategies\n* Management commands for ldap import\n* Mass import of users and groups\n* Sync LDAP users and groups on login\n\nLicence\n-------\n\n::\n\n  Copyright © 2020 Tom Teichler <tom.teichler@teckids.org>\n  Copyright © 2020 Dominik George <dominik.george@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://aleksis.org/\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Tom Teichler',
    'author_email': 'tom.teichler@teckids.org',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
