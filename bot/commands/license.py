import os
import asyncio
import discord
from discord import app_commands
from bot.config import Config
from bot.logger import BotLogger
from bot.license.models import LicenseType
from bot.license.generator import LicenseGenerator

def setup_license_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(name="license", description="Generate a plugin license key", guild=guild)
    @app_commands.default_permissions(administrator=True)
    @app_commands.choices(plugin=[
        app_commands.Choice(name=l.name, value=l.name) for l in LicenseType
    ])
    @app_commands.describe(
        plugin="Select the plugin",
        uuid="Server UUID",
        ip="Server IP Address",
        port="Server port"
    )
    async def license_cmd(
        interaction: discord.Interaction,
        plugin: app_commands.Choice[str],
        uuid: str,
        ip: str,
        port: int
    ):
        await interaction.response.defer(ephemeral=False)
        user_id = str(interaction.user.id)
        plugin_name = plugin.value

        if user_id not in Config.LICENSE_GEN_ACCESS_ID_LIST:
            guild_obj = interaction.guild
            mentions = []
            for uid in Config.LICENSE_GEN_ACCESS_ID_LIST:
                m = guild_obj.get_member(int(uid)) if guild_obj else None
                mentions.append(m.mention if m else "`Unknown Member`")

            if not mentions:
                message = f"No one is authorized to generate the license for {plugin_name}!"
            elif len(mentions) == 1:
                message = f"Only {mentions[0]} can generate the license for {plugin_name}!"
            else:
                all_except_last = ", ".join(mentions[:-1])
                message = f"Only {all_except_last} and {mentions[-1]} can generate the license for {plugin_name}!"

            await interaction.followup.send(message, ephemeral=True)
            return

        BotLogger.info("License generation request received.", True)
        details = (
            "───────── License Request Details ─────────\n"
            f"Plugin: {plugin_name}\n"
            f"UUID: {uuid}\n"
            f"IP: {ip}\n"
            f"Port: {port}\n"
            f"Requested By: {interaction.user}\n"
            "───────────────────────────────────────────\n"
        )
        BotLogger.info(details, True)

        try:
            license_type = LicenseType[plugin_name]
        except KeyError:
            BotLogger.warn(f"Invalid plugin name: {plugin_name}", True)
            await interaction.followup.send("❌ Invalid plugin name.", ephemeral=True)
            return

        BotLogger.info("Starting license file generation...", True)
        file_path = await asyncio.to_thread(LicenseGenerator.get_license_file, license_type, ip, port, uuid)

        if file_path and os.path.exists(file_path):
            try:
                BotLogger.info(f"License generated successfully for {plugin_name} ({uuid})", True)
                filename = os.path.basename(file_path)
                await interaction.followup.send(
                    f"✅ License successfully generated for **{plugin_name}**!",
                    file=discord.File(file_path, filename=filename),
                    ephemeral=False
                )
            finally:
                try:
                    os.remove(file_path)
                except Exception:
                    pass
        else:
            BotLogger.error("License file not found after generation process.", True)
            await interaction.followup.send(
                "❌ Something went wrong while generating the license file. Please check the console.",
                ephemeral=True
            )
