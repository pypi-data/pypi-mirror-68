# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aleksis',
 'aleksis.apps.untis',
 'aleksis.apps.untis.management.commands',
 'aleksis.apps.untis.migrations',
 'aleksis.apps.untis.util.mysql',
 'aleksis.apps.untis.util.mysql.importers',
 'aleksis.apps.untis.util.xml']

package_data = \
{'': ['*'],
 'aleksis.apps.untis': ['locale/ar/LC_MESSAGES/django.po',
                        'locale/de_DE/LC_MESSAGES/django.po',
                        'locale/fr/LC_MESSAGES/django.po',
                        'locale/la/LC_MESSAGES/django.po',
                        'locale/nb_NO/LC_MESSAGES/django.po',
                        'locale/tr_TR/LC_MESSAGES/django.po',
                        'templates/untis/*']}

install_requires = \
['AlekSIS-App-Chronos>=2.0a2,<3.0',
 'AlekSIS>=2.0a2,<3.0',
 'defusedxml>=0.6.0,<0.7.0',
 'mysqlclient>=1.4.6,<2.0.0',
 'tqdm>=4.44.1,<5.0.0']

setup_kwargs = {
    'name': 'aleksis-app-untis',
    'version': '2.0a2',
    'description': 'AlekSIS (School Information System)\u200a—\u200aApp for Untis import',
    'long_description': 'AlekSIS (School Information System)\u200a—\u200aApp for Untis import\n==========================================================\n\nAlekSIS\n-------\n\nThis is an application for use with the `AlekSIS`_ platform.\n\nFeatures\n--------\n\n* Import absence reasons\n* Import absences\n* Import breaks\n* Import classes\n* Import events\n* Import exported Untis database via MySQL import\n* Import exported Untis XML files\n* Import holidays\n* Import lessons\n* Import rooms\n* Import subjects\n* Import substitutions\n* Import supervision areas\n* Import teachers\n* Import time periods\n\nLicence\n-------\n\n::\n\n  Copyright © 2018, 2019, 2020 Jonathan Weth <wethjo@katharineum.de>\n  Copyright © 2018, 2019 Frank Poetzsch-Heffter <p-h@katharineum.de>\n  Copyright © 2019, 2020 Dominik George <dominik.george@teckids.org>\n  Copyright © 2019 Julian Leucker <leuckeju@katharineum.de>\n  Copyright © 2019 mirabilos <thorsten.glaser@teckids.org>\n  Copyright © 2019 Tom Teichler <tom.teichler@teckids.org>\n\n  Licenced under the EUPL, version 1.2 or later\n\nPlease see the LICENCE.rst file accompanying this distribution for the\nfull licence text or on the `European Union Public Licence`_ website\nhttps://joinup.ec.europa.eu/collection/eupl/guidelines-users-and-developers\n(including all other official language versions).\n\n.. _AlekSIS: https://aleksis.org/\n.. _European Union Public Licence: https://eupl.eu/\n',
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
