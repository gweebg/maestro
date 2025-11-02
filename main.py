from dotenv import load_dotenv

from src.proxmox import ProxmoxClient

load_dotenv()


def main():
    proxmox = ProxmoxClient()

    for vm in proxmox.list_vms():
        print(vm["name"])


if __name__ == "__main__":
    main()
