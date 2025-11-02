import os

from dotenv import load_dotenv

from src.maestro import Maestro
from src.proxmox import ProxmoxClient

load_dotenv()


def main():
    _proxmox = ProxmoxClient()
    maestro = Maestro()

    if token := os.getenv("DISCORD_TOKEN"):
        maestro.run(token)


if __name__ == "__main__":
    main()
