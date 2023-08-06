from vault_client.client import VaultClient


env_file = 'data/test.env'


def test_good_init_client():
    client = VaultClient(environ="LOCAL", env_file=env_file)
    assert client.is_authenticated
    assert client.is_authenticated
    assert not client.is_sealed


# def test_bad_init_client():
#     client = VaultClient(environ="LOCAL", env_file=env_file)
#     assert not client.is_authenticated
#     assert not client.is_authenticated
#     assert client.is_sealed


def test_param_in_vault():
    client = VaultClient(environ="LOCAL", env_file=env_file)
    result = client.get("storage", "host")
    assert result == "127.0.0.1"


def test_bad_param1_in_vault():
    client = VaultClient(environ="LOCAL", env_file=env_file)
    result = client.get("storage1", "host")
    assert result is None


def test_bad_param2_in_vault():
    client = VaultClient(environ="LOCAL", env_file=env_file)
    result = client.get("storage", "host1")
    assert result is None
