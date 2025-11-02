import os
from itertools import chain
from typing import Any, Optional

from proxmoxer import ProxmoxAPI


class ProxmoxClient:
    """Singleton class representing the Proxmox client."""

    # singleton instance of proxmox api
    _instance: Optional["ProxmoxClient"] = None
    _initialized: bool = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "ProxmoxClient":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if self._initialized:
            return

        config = self._load_proxmox_env()

        self.proxmox: ProxmoxAPI = ProxmoxAPI(
            host=config["PROXMOX_HOST"],
            user=config["PROXMOX_USER"],
            token_name=config["PROXMOX_TOKEN_NAME"],
            token_value=config["PROXMOX_TOKEN"],
            verify_ssl=config["PROXMOX_SSL"],
            port=config["PROXMOX_PORT"],
        )

        self._initialized = True

    @staticmethod
    def _load_proxmox_env():
        env_variables: list[str] = [
            "PROXMOX_HOST",
            "PROXMOX_USER",
            "PROXMOX_TOKEN_NAME",
            "PROXMOX_TOKEN",
            "PROXMOX_SSL",
            "PROXMOX_PORT",
        ]
        env: dict[str, Any] = {key: os.getenv(key) for key in env_variables}

        env["PROXMOX_SSL"] = (env["PROXMOX_SSL"] or False) in ["true", "yes"]
        env["PROXMOX_PORT"] = int(env["PROXMOX_PORT"]) or 8006

        missing: list[str] = [key for key, value in env.items() if value is None]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return env

    def list_nodes(self) -> list:
        return self.proxmox.nodes.get() or []

    def list_vms(self, node: Optional[str] = None) -> list:
        if node:
            return self.proxmox.nodes(node).qemu.get() or []

        # if node is not specified, return vms all from all nodes
        return list(
            chain.from_iterable(
                self.proxmox.nodes(n["node"]).qemu.get() or []
                for n in self.list_nodes() or []
            )
        )
