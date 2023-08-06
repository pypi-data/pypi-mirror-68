import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

from vault_client.client import VaultClient


env_file = Path.cwd().joinpath("data/vault.env")
load_dotenv(dotenv_path=env_file)
token = os.environ.get("VAULT_TOKEN")
port = os.environ.get("VAULT_PORT")
host = os.environ.get("VAULT_HOST")
mount_point = os.environ.get("VAULT_MOUNT_POINT")
env = os.environ.get("VAULT_ENV")


def test_bad_token_init_client():
    os.environ["VAULT_TOKEN"] = token+"123"
    with pytest.raises(Exception):
        VaultClient(env_file=env_file)
    os.environ["VAULT_TOKEN"] = token


def test_bad_port_init_client():
    os.environ["VAULT_PORT"] = port+"123"
    with pytest.raises(Exception):
        VaultClient(env_file=env_file)
    os.environ["VAULT_PORT"] = port


def test_bad_host_init_client():
    os.environ["VAULT_HOST"] = host+"123"
    with pytest.raises(Exception):
        VaultClient()
    os.environ["VAULT_HOST"] = host


def test_bad_mount_point_init_client():
    os.environ["VAULT_MOUNT_POINT"] = mount_point+"123"
    with pytest.raises(Exception):
        VaultClient(env_file=env_file)
    os.environ["VAULT_MOUNT_POINT"] = mount_point


def test_bad_env_init_client():
    os.environ["VAULT_ENV"] = env+"123"
    client = VaultClient(env_file=env_file)
    os.environ["VAULT_ENV"] = env
    assert client.is_authenticated
    assert client.is_authenticated
    assert not client.is_sealed
    service = "service"
    with pytest.raises(Exception):
        client.get(service, "key_stage1")


def test_init_client():
    client = VaultClient(env_file=env_file)
    assert client.is_authenticated
    assert client.is_authenticated
    assert not client.is_sealed


def test_param_in_vault():
    client = VaultClient(env_file=env_file)
    service = "service"
    result = client.get(service, "key_stage1")
    assert result == "val_stage1"


def test_bad_service_in_vault():
    client = VaultClient(env_file=env_file)
    service = "service1"
    with pytest.raises(Exception):
        client.get(service, "key_stage1")


def test_param_in_cashe_clientvault():
    client = VaultClient(env_file=env_file)
    service = "service"
    client.get(service, "key_stage1")
    result = client.get(service, "key_stage2")
    assert result == "val_stage2"


def test_no_param_in_vault():
    client = VaultClient(env_file=env_file)
    service = "service"
    param = "key_stage123"
    result = client.get(service, param)
    assert result is None

