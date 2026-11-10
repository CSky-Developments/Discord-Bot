import discord
from discord import app_commands

def setup_ping_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(name="ping", description="Replies with Pong!", guild=guild)
    async def ping_cmd(interaction: discord.Interaction):
        await interaction.response.send_message("🏓 **Pong!**")
