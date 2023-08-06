import os
import typing
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

import hvac


@dataclass
class VaultClient:
    environ: str = field(init=True, default='')
    env_file: typing.Union[str, Path] = field(init=True, default='.deploy/.envs/local.env')
    host: str = field(init=False)
    port: str = field(init=False)
    mount_point: str = field(init=False)
    local: bool = field(init=False)
    param: dict = field(init=False)

    def __post_init__(self):
        self.environ = self.environ.upper()
        if self.environ == "LOCAL":
            self.local = True
            if not os.path.exists(self.env_file):
                self.is_authenticated = False
                self.is_initialized = False
                self.is_sealed = True
                return
            load_dotenv(dotenv_path=self.env_file)
            self.is_authenticated = True
            self.is_initialized = True
            self.is_sealed = False
            return
        self.local = False
        self.token = os.environ.get("VAULT_TOKEN")
        self.host = os.environ.get("VAULT_HOST")
        self.port = os.environ.get("VAULT_PORT")
        self.mount_point = os.environ.get("VAULT_MOUNT_POINT")
        self.environ = os.environ.get("VAULT_ENV")
        self.client = hvac.Client(url=f'http://{self.host}:{self.port}', token=self.token)
        self.client.secrets.kv.v2.configure(max_versions=20, mount_point=self.mount_point, )

        self.is_authenticated = self.client.is_authenticated()
        self.is_initialized = self.client.sys.is_initialized()
        self.is_sealed = self.client.sys.is_sealed()
        self.configuration = self.client.secrets.kv.v2.read_configuration(
            mount_point=self.mount_point,
        )
        self.param = dict()

    def get(self, service: str, param: str) -> typing.Union[str, None]:
        if self.local:
            param = f"{service.upper()}_{param.upper()}"
            value = os.environ.get(param)
        else:
            full_path = f"{service.upper()}/{self.environ}"
            if service not in self.param.keys():
                resp = self.client.secrets.kv.v2.read_secret_version(mount_point=self.mount_point, path=full_path)
                self.param[service.upper()] = resp['data']['data']
            if param.lower() in self.param[service.upper()].keys():
                value = self.param[service.upper()][param.lower()]
            else:
                value = None
        return value
