from discord.ext import commands
import discord
import os


class Maestro(commands.Bot):
    def __init__(self):
        self.loadable_cogs: list[str] = ["src.cogs.vms"]

        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(command_prefix=">", intents=intents)

    async def setup_hook(self):
        for cog in self.loadable_cogs:
            await self.load_extension(cog)

        guild_id = os.getenv("DISCORD_GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            self.tree.copy_global_to(guild=guild)
            await self.tree.sync(guild=guild)
        else:
            await self.tree.sync()

        print("Registered commands:")
        for command in self.tree.get_commands():
            print(f"  - {command.name}")

    async def on_ready(self):
        print(f"{self.user} is ready")
        print(f"serving {len(self.guilds)} guilds")
