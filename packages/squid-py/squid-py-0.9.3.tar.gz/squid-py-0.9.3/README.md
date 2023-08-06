[![banner](https://raw.githubusercontent.com/oceanprotocol/art/master/github/repo-banner%402x.png)](https://oceanprotocol.com)

# squid-py

> 💧 Python wrapper, allowing to integrate the basic Ocean/web3.py capabilities
> [oceanprotocol.com](https://oceanprotocol.com)

[![PyPI](https://img.shields.io/pypi/v/squid-py.svg)](https://pypi.org/project/squid-py/)
[![Travis (.com)](https://img.shields.io/travis/com/oceanprotocol/squid-py.svg)](https://travis-ci.com/oceanprotocol/squid-py)
[![GitHub contributors](https://img.shields.io/github/contributors/oceanprotocol/squid-py.svg)](https://github.com/oceanprotocol/squid-py/graphs/contributors)
[![Codacy Badge](https://img.shields.io/codacy/grade/7084fbf528934327904a49d458bc46d1.svg)](https://app.codacy.com/project/ocean-protocol/squid-py/dashboard)
[![Codacy coverage](https://img.shields.io/codacy/coverage/7084fbf528934327904a49d458bc46d1.svg)](https://app.codacy.com/project/ocean-protocol/squid-py/dashboard)

---

## Table of Contents

  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Quick-start](#quick-start)
     - [Usage:](#usage)
  - [Configuration](#configuration)
  - [Development](#development)
        - [Code style](#code-style)
        - [Testing](#testing)
  - [License](#license)

---

## Features

Squid-py include the methods to make easy the connection with contracts deployed in different networks.
This repository include also the methods to encrypt and decrypt information using the Parity Secret Store.

## Prerequisites

Python 3.6

## Quick-start

Install Squid:

```
pip install squid-py
```

## Configuration

In order to effectively use `squid-py` in your local environment you need to run [_Barge_](https://github.com/oceanprotocol/barge) which runs a local Ocean Protocol network on your machine.  You can [configure it with environment variables and feature flags](https://github.com/oceanprotocol/barge#options), by default it will run all the latest stable versions of all [Ocean Protocol components](https://docs.oceanprotocol.com/concepts/components/).

You can generate your own private keys or use test keys that we provide. Please don't use it in production: 

Create key files:
```
touch key_file_1.json key_file_2.json
```
Copy the the following keys into the files that have been created

`key_file_1.json`:
```
{
  "id": "50aa801a-8d66-1402-1fa4-d8987868c2ce",
  "version": 3,
  "crypto": {
    "cipher": "aes-128-ctr",
    "cipherparams": {
      "iv": "a874e6fe50a5bb088826c45560dc1b7e"
    },
    "ciphertext": "2383c6aa50c744b6558e77b5dcec6137f647c81f10f71f22a87321fd1306056c",
    "kdf": "pbkdf2",
    "kdfparams": {
      "c": 10240,
      "dklen": 32,
      "prf": "hmac-sha256",
      "salt": "eca6ccc9fbb0bdc3a516c7576808ba5031669e6878f3bb95624ddb46449e119c"
    },
    "mac": "14e9a33a45ae32f88a0bd5aac14521c1fcf14f56fd55c1a1c080b2f81ddb8d44"
  },
  "address": "068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0",
  "name": "",
  "meta": "{}"
}

```

`key_file_2.json`:
```
{
  "id": "0902d04b-f26e-5c1f-e3ae-78d2c1cb16e7",
  "version": 3,
  "crypto": {
    "cipher": "aes-128-ctr",
    "cipherparams": {
      "iv": "6a829fe7bc656d85f6c2e9fd21784952"
    },
    "ciphertext": "1bfec0b054a648af8fdd0e85662206c65a4af0ed15fede4ad41ca9ab7b504ce2",
    "kdf": "pbkdf2",
    "kdfparams": {
      "c": 10240,
      "dklen": 32,
      "prf": "hmac-sha256",
      "salt": "95f96b5ee22dd537e06076eb8d7078eb7275d29af935782fe476696b11be50e5"
    },
    "mac": "4af2215c3cd9447a5b0512d7d1c3ea5a4435981e1c8f48bf71d7a49c0e5b4986"
  },
  "address": "00bd138abd70e2f00903268f3db08f2d25677c9e",
  "name": "Validator0",
  "meta": "{}"
}
```

Prepare environment account variables:
```
export PARITY_ADDRESS  = 0x00bd138abd70e2f00903268f3db08f2d25677c9e
export PARITY_PASSWORD = node0
export PARITY_ADDRESS1 = 0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0
export PARITY_PASSWORD1 = secret
export PARITY_KEYFILE1 = ./key_file_1.json
export PARITY_KEYFILE =  ./key_file_2.json

```


You may also use the following environment variables (override the corresponding configuration file values):

- KEEPER_PATH
- KEEPER_URL
- GAS_LIMIT
- AQUARIUS_URL

## Usage


```python
import os
import time
import uuid

from ocean_keeper.utils import get_account
from ocean_keeper.contract_handler import ContractHandler

from squid_py import Ocean, ConfigProvider, Config 
from ocean_utils.agreements.service_types import ServiceTypes
from ocean_utils.agreements.service_agreement import ServiceAgreement

# keeper.path should point to the artifact folder which is assumed here to be the default path created by barge
config_dict = {'keeper-contracts':{
                    # Point to an Ethereum RPC client. Note that Squid learns the name of the network to work with from this client.
                    'keeper.url':'http://localhost:8545',
                    # Specify the keeper contracts artifacts folder (has the smart contracts definitions json files). When you
                    # install the package, the artifacts are automatically picked up from the `keeper-contracts` Python
                    # dependency unless you are using a local ethereum network.
                    'keeper.path':'~/.ocean/keeper-contracts/artifacts',
                    'secret_store.url': 'http://localhost:12001',
                    'parity.url': 'http://localhost:8545',
                    'parity.address': '0x00bd138abd70e2f00903268f3db08f2d25677c9e',
                    'parity.password': 'node0',
                    'parity.address1': '0x068ed00cf0441e4829d9784fcbe7b9e26d4bd8d0',
                    'parity.password1': 'secret',
                },
                'resources': {
                    # aquarius is the metadata store. It stores the assets DDO/DID-document
                    'aquarius.url': 'http://172.15.0.15:5000',
                    # Brizo is the publisher's agent. It serves purchase and requests for both data access and compute services
                    'brizo.url': 'http://localhost:8030',
                    # points to the local database file used for storing temporary information (for instance, pending service agreements).
                    'storage.path': 'squid_py.db',
                    # Where to store downloaded asset files
                    'downloads.path': 'consume-downloads'
                }}

metadata = {
    "main": {
        "name": "Ocean protocol white paper",
        "dateCreated": "2012-02-01T10:55:11Z",
        "author": "Mario",
        "license": "CC0: Public Domain",
        "price": "0",
        "files": [
            {
                "index": 0,
                "contentType": "text/text",
                "checksum": str(uuid.uuid4()),
                "checksumType": "MD5",
                "contentLength": "12057507",
                "url": "https://raw.githubusercontent.com/oceanprotocol/barge/master/README.md"
            }
        ],
        "type": "dataset"
    }
}

ConfigProvider.set_config(Config('', config_dict))

ocean = Ocean()

print(ContractHandler.artifacts_path)

config = ocean.config

account = get_account(0) # use if env vars are declared
consumer_account = get_account(1) # PARITY_ADDRESS1 PARITY_KEYFILE1 & PARITY_PASSWORD1

#It is also possible to initialize account as follows bypassing the creation of environment variables
#account = Account(Web3.toChecksumAddress(address), pswrd, key_file, encr_key, key)

ddo = ocean.assets.create(metadata, account, providers=[])
assert ddo is not None, f'Registering asset on-chain failed.'
print("create asset success")

# Now we have an asset registered, we can verify it exists by resolving the did
_ddo = ocean.assets.resolve(ddo.did)
# ddo and _ddo should be identical
print(_ddo.did)

# CONSUMER
# search for assets
asset_ddo = ocean.assets.search("Ocean protocol")[0]
# Need some ocean tokens to be able to order assets
ocean.accounts.request_tokens(account, 10)
print("request tokens success")

service = ddo.get_service(service_type=ServiceTypes.ASSET_ACCESS)

service_agreement_id = ocean.assets.order(ddo.did, service.index, consumer_account, auto_consume=False)

event_wait_time = 10
event = ocean.keeper.agreement_manager.subscribe_agreement_created(
    service_agreement_id,
    event_wait_time,
    None,
    (),
    wait=True
)
assert event, 'no event for EscrowAccessSecretStoreTemplate.AgreementCreated'
print("agreement created")

#  check if the lock reward goes through
event = ocean.keeper.lock_reward_condition.subscribe_condition_fulfilled(
    service_agreement_id,
    120,
    None,
    (),
    wait=True
)
assert event, 'no event for LockRewardCondition.Fulfilled'
print("lockreward success")

assert ocean.assets.consume(service_agreement_id, ddo.did, service.index, consumer_account, config.downloads_path)
print("asset consumed")

# after a short wait (seconds to minutes) the asset data files should be available in the `downloads.path` defined in config
# wait a bit to let things happen
time.sleep(20)

# Asset files are saved in a folder named after the asset id
dataset_dir = os.path.join(
    ocean.config.downloads_path, f"datafile.{asset_ddo.asset_id}.0"
)
if os.path.exists(dataset_dir):
    print("asset files downloaded: {}".format(os.listdir(dataset_dir)))

```



## Development

1. Set up a virtual environment

    ```bash
    virtualenv venv -p python3.6
    source venv/bin/activate 
    ```

1. Install requirements

    ```
    pip install -r requirements_dev.txt
    ```

1. Set up test tier

   ```
   TEST_TIER=e2e
   ```

1. Export account info

    ```
    source accounts.sh
    ```

1. Create the local testing environment using [barge](https://github.com/oceanprotocol/barge). Once cloned that repository, you can start the cluster running:

    ```
    ./start_ocean.sh --no-commons --no-dashboard --no-agent --no-faucet --local-spree-node
    ```

    It runs an Aquarius node and an Ethereum RPC client. For details, read `docker-compose.yml`.

1. Create local configuration file

    ```
    cp config.ini config_local.ini
    ```

   `config_local.ini` is used by unit tests.

1. Copy keeper artifacts

    A bash script is available to copy keeper artifacts into this file directly from a running docker image. This script needs to run in the root of the project.
    The script waits until the keeper contracts are deployed, and then copies the artifacts.

    ```
    ./scripts/wait_for_migration_and_extract_keeper_artifacts.sh
    ```

    The artifacts contain the addresses of all the deployed contracts and their ABI definitions required to interact with them.

1. Run the automated tests

    ```
    python3 setup.py test 
    ```
    OR
    ```
    pytest
    ```

1. Run tests automatically as you change code while doing TDD

    ```
    TEST_TIER=<tier> ptw
    ```

#### Code style

The information about code style in python is documented in this two links [python-developer-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-developer-guide.md)
and [python-style-guide](https://github.com/oceanprotocol/dev-ocean/blob/master/doc/development/python-style-guide.md).

#### Testing

Automatic tests are setup via Travis, executing `tox`.
Our test use pytest framework.

#### New Version / New Release

See [RELEASE_PROCESS.md](RELEASE_PROCESS.md)

## License

```
Copyright 2018 Ocean Protocol Foundation Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
