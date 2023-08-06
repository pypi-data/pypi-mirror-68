# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['golosscripts']

package_data = \
{'': ['*']}

install_requires = \
['bitshares>=0.5.1,<0.6.0',
 'bitsharesscripts>=2,<3',
 'ccxt>=1.26.96,<2.0.0',
 'click>=7.1.1,<8.0.0',
 'defusedxml>=0.6.0,<0.7.0',
 'graphenelib>=1.3.2,<2.0.0',
 'python-golos>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'golosscripts',
    'version': '0.3.2',
    'description': 'Scripts for Golos blockchain',
    'long_description': "golos-scripts\n=============\n\n![test](https://github.com/bitfag/golos-scripts/workflows/test/badge.svg)\n[![Documentation\nStatus](https://readthedocs.org/projects/golos-scripts/badge/?version=latest)](https://golos-scripts.readthedocs.io/en/latest/?badge=latest)\n\nThis is a python scripts collection for golos blockchain network.\n\nFor documentation on reusable parts, pleasee see [documentation on\nreathedocs](https://golos-scripts.readthedocs.io/en/latest/).\n\n* `donation.py` - make a donation for post\n* `change_password.py` - change all account keys using random generated password or user-provided\n* `calc_vesting_reward.py` - calculate profit from vesting holdings\n* `inflation.py` - calculate current inflation or model long-term inflation\n* `generate_keypair.py` - just generate private and public keypair\n* `transfer.py` - transfer some money to another account\n* `transfer_to_vesting.py` - transfer GOLOS to vesting balance (Golos Power)\n* `get_balance.py` - display account balances\n* `get_balance_multi.py` - display balances of multiple accounts\n* `estimate_median_price.py` - look up current witnesses price feeds and calculate new expected median price\n* `estimate_gbg_debt.py` - script to estimate system debt in GBG, see [ESTIMATE\\_GBG\\_DEBT](ESTIMATE_GBG_DEBT.md)\n* `get_post.py` - get and print post/comment\n* `get_props.py` - script to display global properties\n* `get_median_props.py` - script to display current votable parameters\n* `get_voting_power.py` - calculate current voting power of specified account\n* `get_bandwidth.py` - calculate used bandwidth of the account. Can be used in scripting as monitoring tool (`-w 75 -q`)\n* `get_vesting_withdraws.py` - find all vesting withdrawals with rates and dates\n* `get_conversion_requests.py` - find all GBG conversion requests\n* `get_feed_history.py` - script to obtain GBG price feed history\n* `get_miner_queue.py` - script to display miner queue\n* `get_median_voting.py` - get witnesses voting for a particular chain param\n* `get_inflation_voting.py` - show voting for inflation targets properties\n* `get_witness.py` - script to obtain current info for specified witness\n* `get_witnesses.py` - script to display known witnesses, sorted by votes\n* `post.py` - publish post to the blockchain\n* `sea_biom.py` - print Golos Power for each sea habitant level\n* `create_account.py` - create child account\n* `find_transfers.py` - scan account history to find transfers\n* `upvote.py` - upvote/downvote post or comment\n* `withdraw_vesting.py` - withdraw from vesting balance of one account to specified account\n* `withdraw_vesting_multi.py` - withdraw from vesting balance of multiple accounts to specified account\n* `delegate_vesting_shares.py` - script to delegate vesting shares\n* `witness_approve.py` - vote for witness\n* `witness_disapprove.py` - remove vote from witness\n* `update_witness.py` - script to manipulate witness data in the blockchain, see [UPDATE\\_WITNESS](UPDATE_WITNESS.md)\n\nRequirements\n------------\n\n* golos node 0.18+\n\nInstallation via poetry\n-----------------------\n\n1. Install [poetry](https://python-poetry.org/docs/)\n2. Run `poetry install` to install the dependencies\n3. Copy `common.yml.example` to `common.yml` and change variables according to your needs\n4. Now you're ready to run scripts:\n\n\n```\npoetry shell\n./script.py\n```\n\nInstallation via pip\n--------------------\n\nWith pip you can install *golosscripts* package, which provides various functions and helpers:\n\n```\npip install golosscripts\n```\n\nHow to use\n----------\n\n1. Prepare working environment using virtualenv (see above)\n2. Copy `common.yml.example` to `common.yml` and change variables according to your needs\n",
    'author': 'Vladimir Kamarzin',
    'author_email': 'vvk@vvk.pp.ru',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bitfag/golos-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
