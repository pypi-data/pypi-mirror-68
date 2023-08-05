# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.dashboardfeeds',
 'aleksis.apps.dashboardfeeds.migrations',
 'aleksis.apps.dashboardfeeds.util']

package_data = \
{'': ['*'],
 'aleksis.apps.dashboardfeeds': ['locale/*',
                                 'locale/ar/LC_MESSAGES/django.po',
                                 'locale/de_DE/LC_MESSAGES/django.po',
                                 'locale/fr/LC_MESSAGES/django.po',
                                 'locale/la/LC_MESSAGES/django.po',
                                 'locale/nb_NO/LC_MESSAGES/django.po',
                                 'locale/tr_TR/LC_MESSAGES/django.po',
                                 'static/*',
                                 'static/dashboardfeeds/*',
                                 'static/dashboardfeeds/css/*',
                                 'templates/dashboardfeeds/*']}

install_requires = \
['AlekSIS>=2.0a2,<3.0',
 'django-feed-reader>=0.2.1,<0.3.0',
 'feedparser>=5.2.1,<6.0.0',
 'ics>=0.7,<0.8']

setup_kwargs = {
    'name': 'aleksis-app-dashboardfeeds',
    'version': '2.0a2',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Dashboard Feeds (Include feeds from external resources as widgets on dashboard)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp Dashboard Feeds (Include feeds from external resources as widgets on dashboard)\n=========================================================================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\n* Add RSS widgets to dashboard\n* Add iCal widgets to dashboard\n\nLicence\n-------\n\n::\n\n  Copyright © 2020 Dominik George <dominik.george@teckids.org>\n  Copyright © 2020 Julian Leucker <leuckerj@gmail.com>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://aleksis.org/\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Julian Leucker',
    'author_email': 'leuckerj@gmail.com',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
