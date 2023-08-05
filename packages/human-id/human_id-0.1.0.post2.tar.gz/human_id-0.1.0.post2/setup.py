# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['human_id']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0']

entry_points = \
{'console_scripts': ['humanid-gen = human_id.cli:main']}

setup_kwargs = {
    'name': 'human-id',
    'version': '0.1.0.post2',
    'description': 'Human readable IDs, in Python',
    'long_description': '# Human ID\n\nA simple library for generating human IDs like `look-dead-game-story` or `get-nice-office-side`. \n\nInstall with `pip install human-id`\n\nUsage:\n\n```python\nfrom human_id import generate_id\n\n# Simple: "appear-hard-idea-case"\ngenerate_id()\n\n# Custom separator: "do,past,job,number"\ngenerate_id(separator=",")\n\n# More words: "say-may-ask-traditional-power-week"\ngenerate_id(word_count=10)\n\n# Custom seed - the same UUID will produce the same ID.\nimport uuid\ngenerate_id(seed=uuid.uuid4())\n```\n\n## CLI\n\nThis module also comes with a small command line tool: `humanid-gen`\n\n```\n❯ humanid-gen --help\nUsage: humanid-gen [OPTIONS]\n\n  Generate human readable IDs\n\nOptions:\n  --words INTEGER  Number of words\n  --sep TEXT       Separator\n  --seed TEXT      Seed to use\n  --count INTEGER  Number of IDs to generate\n  --help           Show this message and exit.\n```\n\n## Implementation\n\nThis library contains 100 of the most common English nouns, adjectives and verbs, and will \ngenerate a phrase containing several of each type, in the order `verb, adjective, noun`.\n\nThe most common words where chosen because they are typically shorter and simpler to read or type, \nwhich is a key property of human readable IDs.\n\nBy default the ID will contain 4 words, which means there are `300^4` possible IDs (8,100,000,000). If your \nuse case requires more IDs then you can up the number of words at the expense of the readability factor. To \nhave the same number of possible IDs as UUIDs you require 15 words:\n\n`may-hold-come-foreign-low-white-cold-team-point-study-others-home-service-body-child`\n\n',
    'author': 'Tom Forbes',
    'author_email': 'tom@tomforb.es',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
