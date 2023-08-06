# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dial_basic_nodes',
 'dial_basic_nodes.data_augmentation',
 'dial_basic_nodes.hyperparameters_config',
 'dial_basic_nodes.layers_editor',
 'dial_basic_nodes.layers_editor.layers_tree',
 'dial_basic_nodes.layers_editor.layers_tree.abstract_tree_model',
 'dial_basic_nodes.layers_editor.model_table',
 'dial_basic_nodes.model_checkpoint',
 'dial_basic_nodes.predefined_models',
 'dial_basic_nodes.predefined_models.predefined_models_window',
 'dial_basic_nodes.predefined_ttv',
 'dial_basic_nodes.predefined_ttv.ttv_sets_list',
 'dial_basic_nodes.test_model',
 'dial_basic_nodes.test_model.test_dataset_table',
 'dial_basic_nodes.training_console',
 'dial_basic_nodes.ttv_editor',
 'dial_basic_nodes.ttv_editor.ttv_sets_tabs',
 'dial_basic_nodes.ttv_exporter',
 'dial_basic_nodes.ttv_importer',
 'dial_basic_nodes.ttv_importer.datatype_selector',
 'dial_basic_nodes.ttv_importer.formats_widgets',
 'dial_basic_nodes.ttv_merger',
 'dial_basic_nodes.ttv_splitter',
 'dial_basic_nodes.utils',
 'dial_basic_nodes.utils.dataset_table']

package_data = \
{'': ['*']}

install_requires = \
['dial-core>=0.20a0', 'dial-gui>=0.9a0']

setup_kwargs = {
    'name': 'dial-basic-nodes',
    'version': '0.7a0',
    'description': 'Basic nodes for the Dial app.',
    'long_description': "# dial-basic-nodes\nBasic nodes for DL tasks, used by the Dial app.\n\n## Documentation\n\nThis project's documentation lives at [readthedocs.io](https://dial-basic-nodes.readthedocs.io)\n\n## License\n\nAll code is provided under the __GPL-3.0__ license. See [LICENSE](LICENSE) for more details.\n\n## Authors\n\n* **David Afonso (davafons)**: [Github](https://github.com/davafons) [Twitter](https://twitter.com/davafons)\n",
    'author': 'David Afonso',
    'author_email': 'davafons@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dial-app/dial-basic-nodes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<=3.8.2',
}


setup(**setup_kwargs)
