# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cocinero', 'cocinero.plugins']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'click>=7.1.2,<8.0.0', 'colorama>=0.4.3,<0.5.0']

entry_points = \
{'console_scripts': ['cocinero = cocinero:cli']}

setup_kwargs = {
    'name': 'cocinero',
    'version': '0.1.1',
    'description': 'Um utilitário em Python para criar projetos a partir de templates',
    'long_description': '# 🍳 cocinero\n\ncocinero é um utilitário escrito em Python para facilitar a geração de projetos novos a partir de boilerplates. Este projeto permite:\n\n- Criar novos projetos a partir de um repositório base\n- Verificar no ambiente do usuário se ele possui todos os requisitos para criar/executar um projeto\n- Executar tarefas pré-definidas em cima dos novos projetos \n\n## Instalação\n\nPara instalar o cocinero, você pode utilizar tanto o pip, quanto o pipx, executando:\n\n```bash\npip install cocinero\n```\n\nou ...\n\n```bash\npipx install cocinero\n```\n\nPara utilizar boilerplates oriundos do GitHub, você também precisa instalar o git.\n\n\n## Como usar \n\nApós instalado, para criar um novo projeto com o cocinero, execute:\n\n```bash\ncocinero cook github.com/des467/webservicepython meu_novo_projeto_incrivel\n```\n\nO comando acima irá:\n- Clonar o repositório template passado\n- Ler o arquivo `cocinero-recipe.yml` na raiz do repositório e a partir daí..\n- .. gerar o seu incrível projeto.\n\nPara ver mais informações sobre como criar `recipes`, [clique aqui](docs/RECIPE.md).\n\n## Como contribuir\n\nVeja como contribuir [clicando aqui](docs/CONTRIBUTING.md).\n\n## Licença\n\nEste projeto utiliza a licença GPL v3. Para ver mais sobre a licença, [clique aqui](LICENSE)',
    'author': 'Ricardo Gomes',
    'author_email': 'desk467@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/desk467/cocinero',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
