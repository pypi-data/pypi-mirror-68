#  Copyright 2018 Ocean Protocol Foundation
#  SPDX-License-Identifier: Apache-2.0

import uuid

import pytest
from ocean_keeper.contract_handler import ContractHandler
from ocean_keeper.web3_provider import Web3Provider
from ocean_utils.aquarius import AquariusProvider

from examples import ExampleConfig
from squid_py import ConfigProvider
from squid_py.ocean.keeper import SquidKeeper as Keeper
from tests.resources.helper_functions import (get_consumer_ocean_instance,
                                              get_metadata, get_publisher_account,
                                              get_publisher_ocean_instance, get_registered_ddo,
                                              setup_logging)
from tests.resources.mocks.secret_store_mock import SecretStoreMock
from tests.resources.tiers import should_run_test

setup_logging()

if should_run_test('e2e'):
    ConfigProvider.set_config(ExampleConfig.get_config())


@pytest.fixture
def setup_all():
    config = ExampleConfig.get_config()
    Web3Provider.init_web3(config.keeper_url)
    ContractHandler.set_artifacts_path(config.keeper_path)
    Keeper.get_instance()


@pytest.fixture
def secret_store():
    return SecretStoreMock


@pytest.fixture
def publisher_ocean_instance():
    return get_publisher_ocean_instance()


@pytest.fixture
def consumer_ocean_instance():
    return get_consumer_ocean_instance()


@pytest.fixture
def registered_ddo():
    ocn = get_publisher_ocean_instance()
    aqua = AquariusProvider.get_aquarius(ocn.config.aquarius_url)
    for did in aqua.list_assets():
        aqua.retire_asset_ddo(did)

    return get_registered_ddo(ocn, get_publisher_account())


@pytest.fixture
def web3_instance():
    config = ExampleConfig.get_config()
    return Web3Provider.get_web3(config.keeper_url)


@pytest.fixture
def metadata():
    metadata = get_metadata()
    metadata['main']['files'][0]['checksum'] = str(uuid.uuid4())
    return metadata
