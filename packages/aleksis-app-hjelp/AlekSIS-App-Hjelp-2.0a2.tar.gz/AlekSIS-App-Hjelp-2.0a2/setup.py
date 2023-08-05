# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis', 'aleksis.apps.hjelp', 'aleksis.apps.hjelp.migrations']

package_data = \
{'': ['*'],
 'aleksis.apps.hjelp': ['locale/ar/LC_MESSAGES/django.po',
                        'locale/de_DE/LC_MESSAGES/django.po',
                        'locale/fr/LC_MESSAGES/django.po',
                        'locale/la/LC_MESSAGES/django.po',
                        'locale/nb_NO/LC_MESSAGES/django.po',
                        'locale/tr_TR/LC_MESSAGES/django.po',
                        'static/css/hjelp/*',
                        'templates/hjelp/*',
                        'templates/templated_email/*']}

install_requires = \
['AlekSIS>=2.0a2,<3.0']

setup_kwargs = {
    'name': 'aleksis-app-hjelp',
    'version': '2.0a2',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Hjelp (FAQ, issue reporting and support)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp Hjelp (FAQ and support)\n=================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\n* Report issues\n* Frequently asked questions\n* Ask questions\n* Feedback\n\nLicence\n-------\n\n::\n\n  Copyright © 2019, 2020 Julian Leucker <leuckeju@katharineum.de>\n  Copyright © 2019, 2020 Hangzhi Yu <yuha@katharineum.de>\n  Copyright © 2019 Frank Poetzsch-Heffter <p-h@katharineum.de>\n  Copyright © 2019 Jonathan Weth <wethjo@katharineum.de>\n  Copyright © 2020 Tom Teichler <tom.teichler@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://aleksis.org/\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Julian Leucker',
    'author_email': 'leuckeju@katharineum.de',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
