# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.chronos',
 'aleksis.apps.chronos.migrations',
 'aleksis.apps.chronos.templatetags',
 'aleksis.apps.chronos.util']

package_data = \
{'': ['*'],
 'aleksis.apps.chronos': ['locale/ar/LC_MESSAGES/django.po',
                          'locale/de_DE/LC_MESSAGES/django.po',
                          'locale/fr/LC_MESSAGES/django.po',
                          'locale/la/LC_MESSAGES/django.po',
                          'locale/nb_NO/LC_MESSAGES/django.po',
                          'locale/tr_TR/LC_MESSAGES/django.po',
                          'static/css/chronos/*',
                          'static/js/chronos/*',
                          'templates/chronos/*',
                          'templates/chronos/partials/*',
                          'templates/chronos/partials/subs/*']}

install_requires = \
['AlekSIS>=2.0a2,<3.0', 'calendarweek>=0.4.4,<0.5.0']

setup_kwargs = {
    'name': 'aleksis-app-chronos',
    'version': '2.0a2',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp Χρόνος (digital timetables)',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp Χρόνος (digital timetables)\n=====================================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\n* Show absent groups in timetable\n* Show absent teachers in timetable\n* Show affected groups in timetable\n* Show affected teachers in timetable\n* Timetables per day\n* Timetables per group\n* Timetables per person\n* Timetables per room\n* Timetables per week\n\nLicence\n-------\n\n::\n\n  Copyright © 2018, 2019, 2020 Jonathan Weth <wethjo@katharineum.de>\n  Copyright © 2018, 2019 Frank Poetzsch-Heffter <p-h@katharineum.de>\n  Copyright © 2019, 2020 Dominik George <dominik.george@teckids.org>\n  Copyright © 2019 Julian Leucker <leuckeju@katharineum.de>\n  Copyright © 2019 Tom Teichler <tom.teichler@teckids.org>\n  Copyright © 2019 Hangzhi Yu <yuha@katharineum.de>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://aleksis.org/\n.. _European Union Public Licence: https://eupl.eu/\n',
    'author': 'Dominik George',
    'author_email': 'dominik.george@teckids.org',
    'maintainer': 'Jonathan Weth',
    'maintainer_email': 'wethjo@katharineum.de',
    'url': 'https://aleksis.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
