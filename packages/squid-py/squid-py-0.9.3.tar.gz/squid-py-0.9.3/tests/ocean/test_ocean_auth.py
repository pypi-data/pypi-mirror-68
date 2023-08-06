from squid_py.ocean.keeper import SquidKeeper as Keeper
from squid_py.ocean.ocean_auth import OceanAuth
from tests.resources.helper_functions import get_publisher_account


def test_get_token():
    ocn_auth = OceanAuth(Keeper.get_instance(), ':memory:')
    acc = get_publisher_account()
    token = ocn_auth.get(acc)
    assert isinstance(token, str), 'Invalid auth token type.'
    assert token.startswith('0x'), 'Invalid auth token.'
    parts = token.split('-')
    assert len(parts) == 2, 'Invalid token, timestamp separator is not found.'

    address = ocn_auth.check(token)
    assert address != '0x0', 'Verifying token failed.'


def test_check_token(web3_instance):
    ocn_auth = OceanAuth(Keeper.get_instance(), ':memory:')
    acc = get_publisher_account()

    token = ocn_auth.get(acc)
    address = ocn_auth.check(token)
    assert address != '0x0', 'Verifying token failed.'

    sig = token.split('-')[0]
    assert ocn_auth.check(sig) == '0x0'

    # Test token expiration


def test_store_token():
    ocn_auth = OceanAuth(Keeper.get_instance(), ':memory:')
    acc = get_publisher_account()
    token = ocn_auth.store(acc)
    assert ocn_auth.check(token) == acc.address, 'invalid token, check failed.'
    # verify it is saved
    assert ocn_auth.restore(acc) == token, 'Restoring token failed.'


def test_restore_token(publisher_ocean_instance):
    ocn_auth = OceanAuth(Keeper.get_instance(), ':memory:')
    acc = get_publisher_account()
    assert ocn_auth.restore(acc) is None, 'Expecting None when restoring non-existing token.'

    token = ocn_auth.store(acc)
    assert ocn_auth.check(token) == acc.address, 'invalid token, check failed.'
    # verify it is saved
    assert ocn_auth.restore(acc) == token, 'Restoring token failed.'


def test_known_token():
    token = "0x1d2741dee30e64989ef0203957c01b14f250f5d2f6ccb0c" \
            "88c9518816e4fcec16f84e545094eb3f377b7e214ded22676" \
            "fbde8ca2e41b4eb1b3565047ecd9acf300-1568372035"
    pub_address = "0xe2DD09d719Da89e5a3D0F2549c7E24566e947260"

    ocn_auth = OceanAuth(Keeper.get_instance(), ':memory:')
    assert ocn_auth.is_token_valid(token), f'Invalid token!! has the token specs changed?'

    def _get_timestamp():
        return int('1568372035') + 10000

    ocn_auth._get_timestamp = _get_timestamp
    address = ocn_auth.check(token)
    assert address.lower() == pub_address.lower(), f'Recovered address {address} does not match ' \
                                                   f'known signer address {pub_address}, if the ' \
                                                   f'token generation method is changed please update ' \
                                                   f'the token in this test with the new format.'
