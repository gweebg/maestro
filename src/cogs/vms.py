import discord
from discord import app_commands
from discord.ext import commands

from src.proxmox import ProxmoxClient


class VirtualMachinesCog(commands.Cog):
    """_summary_

    Args:
        commands (_type_): _description_
    """

    def __init__(self, bot):
        self.bot = bot
        self.proxmox = ProxmoxClient()

    vms = app_commands.Group(name="vms", description="Virtual machine related commands")

    @vms.command(name="list", description="List all existing virtual machines")
    async def vms_list(self, interaction: discord.Interaction):
        vms = self.proxmox.list_vms()
        vm_list = "\n".join(
            [
                f"- {vm.get('name', 'Unknown')} (ID: {vm.get('vmid', 'N/A')})"
                for vm in vms
            ]
        )

        if not vm_list:
            vm_list = "No VMs found"

        await interaction.response.send_message(
            f"Virtual Machines:\n```\n{vm_list}\n```"
        )


async def setup(bot):
    await bot.add_cog(VirtualMachinesCog(bot))
