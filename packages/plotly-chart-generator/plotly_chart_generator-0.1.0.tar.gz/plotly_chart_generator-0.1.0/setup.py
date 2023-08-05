# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['plotly_chart_generator']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.0.3,<2.0.0', 'plotly>=4.6.0,<5.0.0', 'seaborn>=0.10.0,<0.11.0']

setup_kwargs = {
    'name': 'plotly-chart-generator',
    'version': '0.1.0',
    'description': 'Quickly display basic Plotly charts based on data inside a Pandas dataframe.',
    'long_description': '======================\nPlotly Chart Generator\n======================\n\nDescription\n-----------\nThis package allows the user to quickly generate plotly charts from\nPandas dataframes and other data structures with as little as one line of code.\n\nThe following chart types can be created:\n\n* Bar charts (from dataframe)\n* Line charts (from dataframe)\n* Scatter charts (from dictionary)\n* Pie charts (from lists, numpy arrays, Pandas series)\n* Histograms (from lists, numpy arrays, Pandas series)\n* Dot charts (from dataframe)\n* Box charts (from lists, numpy arrays, Pandas series)\n* Sunburst charts (from lists, numpy arrays, Pandas series)\n* Scatter charts subplots (from dictionary)\n* Pie chats subplots (from dictionary)\n\n\n\nInstallation\n------------\n\n.. code:: python\n\n    pip install plotly_chart_generator\n\nUsage\n-----\n\n',
    'author': 'Preben Hesvik',
    'author_email': 'Prebenhesvik@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/PrebenHesvik/plotly_chart_builder',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
