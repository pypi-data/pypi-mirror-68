# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dssdata',
 'dssdata.decorators',
 'dssdata.pfmodes',
 'dssdata.reductions',
 'dssdata.reductions.regs',
 'dssdata.tools',
 'dssdata.tools.lines',
 'dssdata.tools.losses',
 'dssdata.tools.regs',
 'dssdata.tools.voltages']

package_data = \
{'': ['*']}

install_requires = \
['OpenDSSDirect.py[extras]>=0.3.7,<0.4.0']

setup_kwargs = {
    'name': 'dssdata',
    'version': '0.1.2',
    'description': 'Organizing OpenDSS data',
    'long_description': '# DSSData\n\n\nA python micro-framework for simulation and data analysis of electrical distribution systems modeled on [OpenDSS](https://www.epri.com/#/pages/sa/opendss?lang=en).\n\nMode support: Static and Time-series\n\n\n## Documentation\n\nSee [DSSData Documentation](https://felipemarkson.github.io/power-flow-analysis/).\n\n## Installation\n\nWe strongly recommend the use of virtual environments manager.\n\n\n### Using pip\n\n```console\npip install dssdata\n```\n\n### Using poetry\n\n```console\npoetry add dssdata\n```\n\nContributors: \n\n- [JonasVil](https://github.com/felipemarkson/power-flow-analysis/commits?author=JonasVil)\n\n<!--\n### ```powerflow.losses_tools.get_total_pd_elements_losses(powerflow.systemclass.SystemClass)```\n\nRetorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados do somatório das perdas de todos os elementos do tipo PD (Power Delivery). Apresenta as perdas ativas(kW) e reativas(kVAr). Ex:\n\n|         name       |  kw_losses_total  | kvar_losses_total |\n|--------------------|-------------------|-------------------|\n|   all_pd_elements  |       112.398     |      327.926      |\n\nObs: Apesar dos capacitores serem tratados como um elemento do tipo PD, eles não são considerados.\n\n\n### ```powerflow.losses_tools.get_transformer_losses(powerflow.systemclass.SystemClass)```\nRetorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados referentes as perdas um a um dos transformadores conectaods à rede. Além disso, é apresentado o valor referente as perdas totais relacionadas aos transformadores. Apresenta as perdas ativas(kW) e reativas(kVAr).\n\n### ```powerflow.losses_tools.get_all_pd_elements_losses(powerflow.systemclass.SystemClass)```\nRetorna um [pandas.Dataframe](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) com os dados referentes as perdas um a um dos elementos do tipo PD conectaods à rede. Apresenta as perdas ativas(kW) e reativas(kVAr).\n\nObs: Apesar dos capacitores serem tratados como um elemento do tipo PD, eles não são considerados.\n\n\n## Como contribuir\n\nEsteja livre para criar outras classes além do PowerFlow.\n\nTodos atributos das classes devem ser privados, ou seja, iniciar com __ (dois underlines). Com exceção dos atributos que dão acesso ao [OpenDSSDirect.py](https://github.com/dss-extensions/OpenDSSDirect.py)\n\nO acesso ou mudança de um atributo deve ser feita por um método público.\n\nDeve-se definir quais métodos devem ser públicos e quais devem ser privados.\n\nOs métodos privados devem iniciar com __ (dois underlines).\n\nDê preferência por criar funções (métodos) pequenas que possuem apenas uma única responsabilidade.\n\nOs nomes dos atributos e dos métodos devem ser claros e legíveis, não precisa economizar no tamanho do nome ;).\n\nEnvie commits pequenos com poucas alterações por vez.\n\n\n## Requisitos para Desenvolvimento\n\n[Poetry](https://python-poetry.org/)\n\n-->\n',
    'author': 'Felipe M. S. Monteiro',
    'author_email': 'fmarkson@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/felipemarkson/dssdata',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.8',
}


setup(**setup_kwargs)
