import os
import json
import time
import asyncio
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import discord
from discord.ui import Modal, TextInput

from bot.config import Config
from bot.logger import BotLogger
from bot.ticket.types import TicketType
from bot.ticket import buttons
from bot.embeds import ticket_embeds, help_embeds
from bot.plugingen.models import Project
from bot.plugingen.builder import Builder
from bot.plugingen.services.gemini_service import GeminiService

DATA_FILE = os.path.join("data", "ticket_data.json")

class TicketData:
    def __init__(self):
        self.normal_ticket_id = 1
        self.order_ticket_id = 1
        self.plugin_gen_ticket_id = 1
        self.reward_ticket_id = 1
        self.staff_app_ticket_id = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalTicketID": self.normal_ticket_id,
            "orderTicketID": self.order_ticket_id,
            "pluginGenTicketID": self.plugin_gen_ticket_id,
            "rewardTicketID": self.reward_ticket_id,
            "staffAppTicketID": self.staff_app_ticket_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TicketData":
        td = cls()
        td.normal_ticket_id = data.get("normalTicketID", 1)
        td.order_ticket_id = data.get("orderTicketID", 1)
        td.plugin_gen_ticket_id = data.get("pluginGenTicketID", 1)
        td.reward_ticket_id = data.get("rewardTicketID", 1)
        td.staff_app_ticket_id = data.get("staffAppTicketID", 1)
        return td

class PluginGenModal(Modal, title="Generate Plugin"):
    def __init__(self, ticket_manager: "TicketManager"):
        super().__init__(custom_id="plugin_gen_modal")
        self.ticket_manager = ticket_manager

        self.api_key_input = TextInput(
            label="Gemini API Key",
            placeholder="Your Gemini API Key",
            style=discord.TextStyle.short,
            required=True
        )
        self.name_input = TextInput(
            label="Plugin Name",
            placeholder="Name",
            style=discord.TextStyle.short,
            required=True
        )
        self.version_input = TextInput(
            label="Minecraft Version",
            placeholder="Plugin Version (e.g. 1.21.4)",
            style=discord.TextStyle.short,
            required=True
        )
        self.desc_input = TextInput(
            label="Description",
            placeholder="Describe your plugin features...",
            style=discord.TextStyle.paragraph,
            required=True
        )

        self.add_item(self.api_key_input)
        self.add_item(self.name_input)
        self.add_item(self.version_input)
        self.add_item(self.desc_input)

    async def on_submit(self, interaction: discord.Interaction):
        api_key = self.api_key_input.value.strip()
        name = self.name_input.value.strip()
        version = self.version_input.value.strip()
        description = self.desc_input.value.strip()

        member = interaction.user
        project = Project(name, version, description)

        response_embed = discord.Embed(
            title="Plugin Generation",
            description="Creating your Work Space, Please wait while we process your generation.\n",
            color=0x4482FF
        )
        response_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)

        await interaction.response.send_message(embed=response_embed, ephemeral=True, delete_after=15)
        BotLogger.info(f"Plugin generation requested by `{member.name}` for plugin: `{name}` Creating workspace for it...", True)

        await self.ticket_manager.create_workspace(member, project, api_key)

class TicketManager:
    def __init__(self, guild: discord.Guild, data_file: str = DATA_FILE):
        self.guild = guild
        self.data_file = data_file
        self.ticket_data = TicketData()
        self.load_ticket_data()

    def load_ticket_data(self):
        if not os.path.exists(self.data_file):
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            self.ticket_data = TicketData()
            self.save_ticket_data()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.ticket_data = TicketData.from_dict(data)
            BotLogger.info("Successfully Loaded ticket data!", False)
        except Exception as ex:
            BotLogger.error(f"An error occurred while loading ticket data. Error: {ex}", False)
            self.ticket_data = TicketData()

    def save_ticket_data(self):
        try:
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            temp_file = f"{self.data_file}.tmp"
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(self.ticket_data.to_dict(), f, indent=2)
            os.replace(temp_file, self.data_file)
        except Exception as ex:
            BotLogger.info(f"An error occurred while saving ticket data. Error: {ex}", False)

    def get_ticket_id(self, ticket_type: TicketType) -> str:
        if ticket_type == TicketType.NORMAL:
            tid = self.ticket_data.normal_ticket_id
            self.ticket_data.normal_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.ORDER:
            tid = self.ticket_data.order_ticket_id
            self.ticket_data.order_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.PLUGIN_GEN:
            tid = self.ticket_data.plugin_gen_ticket_id
            self.ticket_data.plugin_gen_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.REWARD:
            tid = self.ticket_data.reward_ticket_id
            self.ticket_data.reward_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.STAFF_APP:
            tid = self.ticket_data.staff_app_ticket_id
            self.ticket_data.staff_app_ticket_id = 0 if tid >= 9999 else tid + 1
        else:
            tid = 1

        self.save_ticket_data()
        return f"{tid:04d}"

    async def handle_button_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data.get("custom_id")
        member = interaction.user
        channel = interaction.channel

        if custom_id == "Ticket_Create_Button":
            await self.handle_create_ticket(interaction, member, TicketType.NORMAL)
        elif custom_id == "Ticket_Close_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_ticket_close_embed(),
                view=buttons.create_ticket_close_confirm_view(),
                ephemeral=True
            )
        elif custom_id == "Ticket_Close_Confirm_Button":
            await self.handle_close_confirm(interaction, member, channel, TicketType.NORMAL)
        elif custom_id == "Ticket_Close_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_ticket_close_cancel_embed(),
                ephemeral=True,
                delete_after=10
            )
        elif custom_id == "Ticket_Delete_Button":
            await self.handle_delete_ticket(interaction, member, channel, TicketType.NORMAL)

        elif custom_id == "Order_Create_Button":
            await self.handle_create_ticket(interaction, member, TicketType.ORDER)
        elif custom_id == "Order_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_order_close_embed(),
                view=buttons.create_order_close_confirm_view(),
                ephemeral=True
            )
        elif custom_id == "Server_Order_Create_Button":
            await interaction.response.send_message("Continue at https://discord.gg/Cftg5GT7vd", ephemeral=True)
            BotLogger.info(f"A server hosting order is requested by `{member.name}`.", True)
        elif custom_id == "Order_Cancel_Confirm_Button":
            await self.handle_close_confirm(interaction, member, channel, TicketType.ORDER)
        elif custom_id == "Order_Cancel_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_order_close_cancel_embed(),
                ephemeral=True,
                delete_after=10
            )
        elif custom_id == "Order_Delete_Button":
            await self.handle_delete_ticket(interaction, member, channel, TicketType.ORDER)

        elif custom_id == "Plugin_Generate_Button":
            await self.handle_create_ticket(interaction, member, TicketType.PLUGIN_GEN)
        elif custom_id == "Plugin_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_plugin_gen_close_embed(),
                view=buttons.create_plugin_cancel_confirm_view(),
                ephemeral=True
            )
        elif custom_id == "Plugin_Cancel_Confirm_Button":
            await self.handle_close_confirm(interaction, member, channel, TicketType.PLUGIN_GEN)
        elif custom_id == "Plugin_Cancel_Abort_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_plugin_gen_close_cancel_embed(),
                ephemeral=True,
                delete_after=10
            )
        elif custom_id == "Plugin_Delete_Button":
            await self.handle_delete_ticket(interaction, member, channel, TicketType.PLUGIN_GEN)

        elif custom_id == "Reward_Claim_Button":
            await self.handle_create_ticket(interaction, member, TicketType.REWARD)
        elif custom_id == "Reward_Close_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_reward_close_embed(),
                view=buttons.create_reward_close_confirm_view(),
                ephemeral=True
            )
        elif custom_id == "Reward_Close_Confirm_Button":
            await self.handle_close_confirm(interaction, member, channel, TicketType.REWARD)
        elif custom_id == "Reward_Close_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_reward_close_cancel_embed(),
                ephemeral=True,
                delete_after=10
            )
        elif custom_id == "Reward_Delete_Button":
            await self.handle_delete_ticket(interaction, member, channel, TicketType.REWARD)

        elif custom_id in ("Developer_Button", "Moderator_Button", "Supporter_Button"):
            await self.handle_create_ticket(interaction, member, TicketType.STAFF_APP, extra=custom_id)
        elif custom_id in ("Developer_Close_Button", "Moderator_Close_Button", "Supporter_Close_Button"):
            await interaction.response.send_message(
                embed=ticket_embeds.make_staff_app_close_embed(),
                view=buttons.create_app_close_confirm_view(),
                ephemeral=True
            )
        elif custom_id == "App_Close_Confirm_Button":
            await self.handle_close_confirm(interaction, member, channel, TicketType.STAFF_APP)
        elif custom_id == "App_Close_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_staff_app_close_cancel_embed(),
                ephemeral=True,
                delete_after=10
            )
        elif custom_id == "App_Delete_Button":
            await self.handle_delete_ticket(interaction, member, channel, TicketType.STAFF_APP)

    async def handle_create_ticket(self, interaction: discord.Interaction, member: discord.Member, ticket_type: TicketType, extra: Optional[str] = None):
        if ticket_type == TicketType.PLUGIN_GEN:
            has_role = any(r.id == Config.PLUGIN_GEN_ACCESS_ROLE_ID for r in member.roles) if isinstance(member, discord.Member) else False
            if not has_role:
                no_access = discord.Embed(
                    title="**Access Denied**",
                    description=(
                        "**You need the Plugin Generation subscription to use this service.**\n"
                        "This is a premium feature. Please create a ticket to subscribe."
                    ),
                    color=0xE74C3C
                )
                no_access.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
                await interaction.response.send_message(embed=no_access, ephemeral=True, delete_after=15)
                return

            modal = PluginGenModal(self)
            await interaction.response.send_modal(modal)
            return

        emoji_map = {
            TicketType.NORMAL: "🎫・",
            TicketType.ORDER: "🛒・",
            TicketType.PLUGIN_GEN: "✨️・",
            TicketType.REWARD: "🎁・",
            TicketType.STAFF_APP: "🎓・"
        }
        category_map = {
            TicketType.NORMAL: Config.TICKET_NORMAL,
            TicketType.ORDER: Config.TICKET_ORDER,
            TicketType.PLUGIN_GEN: Config.TICKET_PLUGIN_GEN,
            TicketType.REWARD: Config.TICKET_REWARD,
            TicketType.STAFF_APP: Config.TICKET_STAFF_APP
        }
        name_map = {
            TicketType.NORMAL: "ticket",
            TicketType.ORDER: "order",
            TicketType.PLUGIN_GEN: "plugin generation",
            TicketType.REWARD: "reward ticket",
            TicketType.STAFF_APP: "staff application"
        }

        ticket_emoji = emoji_map.get(ticket_type, "🎫・")
        cat_id = category_map.get(ticket_type, 0)
        ticket_name = name_map.get(ticket_type, "ticket")

        category = self.guild.get_channel(cat_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            BotLogger.error(f"Category {cat_id} not found for {ticket_type}", True)
            await interaction.response.send_message("❌ Failed to find ticket category. Please notify staff.", ephemeral=True)
            return

        ticket_id = self.get_ticket_id(ticket_type)
        channel_name = f"{ticket_emoji}{ticket_id}"

        BotLogger.info(f"Creating a new `{ticket_name}` for `{member.name}`...", True)

        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        try:
            channel = await self.guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites
            )
        except Exception as e:
            BotLogger.error(f"An error occurred while creating a `{ticket_name}` for `{member.name}`: {e}", False)
            await interaction.response.send_message("❌ Failed to create channel. Check permissions.", ephemeral=True)
            return

        BotLogger.info(f"Successfully created a new `{ticket_name}`: `{channel.name}`", True)

        desc_map = {
            TicketType.NORMAL: f"Your ticket has been successfully created in {channel.mention}. We appreciate your patience while we address your request.",
            TicketType.ORDER: f"Your order has been successfully placed in {channel.mention}. We appreciate your patience while our team reviews your request.",
            TicketType.PLUGIN_GEN: f"Your plugin generation request has been successfully created in {channel.mention}. Please wait while we process your generation.",
            TicketType.REWARD: f"Your reward claim ticket has been successfully created in {channel.mention}. Please wait for our team to process your request.",
            TicketType.STAFF_APP: f"Your application has been successfully created in {channel.mention}. We sincerely appreciate your interest in pursuing a position at CSky Developments."
        }

        reply_embed = discord.Embed(
            description=desc_map.get(ticket_type, ""),
            color=0x4482FF
        )
        reply_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)

        await interaction.response.send_message(embed=reply_embed, ephemeral=True, delete_after=10)

        # Send initial embed inside created channel
        if ticket_type == TicketType.NORMAL:
            await channel.send(embed=ticket_embeds.make_ticket_create_embed(), view=buttons.create_ticket_close_view())
        elif ticket_type == TicketType.ORDER:
            await channel.send(embed=ticket_embeds.make_order_create_embed(), view=buttons.create_order_close_view())
        elif ticket_type == TicketType.PLUGIN_GEN:
            await channel.send(embed=ticket_embeds.make_plugin_gen_embed(), view=buttons.create_plugin_cancel_view())
        elif ticket_type == TicketType.REWARD:
            await channel.send(embed=ticket_embeds.make_reward_create_embed(), view=buttons.create_reward_close_view())
        elif ticket_type == TicketType.STAFF_APP:
            if extra == "Moderator_Button":
                view = buttons.create_moderator_close_view()
                questions = ticket_embeds.make_moderator_questions_embed()
            elif extra == "Supporter_Button":
                view = buttons.create_supporter_close_view()
                questions = ticket_embeds.make_supporter_questions_embed()
            else:
                view = buttons.create_developer_close_view()
                questions = ticket_embeds.make_developer_questions_embed()

            await channel.send(embed=ticket_embeds.make_staff_app_create_embed(), view=view)
            await channel.send(embed=questions)

    async def create_workspace(self, member: discord.Member, project: Project, api_key: str):
        ticket_id = self.get_ticket_id(TicketType.PLUGIN_GEN)
        category = self.guild.get_channel(Config.TICKET_PLUGIN_GEN)

        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        channel = await self.guild.create_text_channel(
            name=f"✨️・{ticket_id}",
            category=category,
            overwrites=overwrites
        )

        response_embed = discord.Embed(
            title="Plugin・Generation",
            description=f"Your plugin generation Work Space has been successfully created in {channel.mention}. \nPlease wait while we process your generation.\n",
            color=0x4482FF
        )
        response_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)

        try:
            await member.send(embed=response_embed)
        except Exception:
            pass

        BotLogger.info(f"Successfully created a new `WorkSpace`:`{channel.name}`", True)

        desc = (
            "We're generating your plugin using CSky Development's advance AI build tool.\n"
            "> For safety and compatibility, we recommend testing generated builds on a **non-production server** before using them live.\n"
        )
        project_desc_trunc = (project.get_description()[:200] + "...") if len(project.get_description()) > 200 else project.get_description()

        gen_embed = discord.Embed(
            title="Plugin・Generation",
            description=desc,
            color=0xE67E22,
            timestamp=datetime.now(timezone.utc)
        )
        gen_embed.add_field(
            name="Project Info:",
            value=f"Name: {project.get_name()}\nVersion: `{project.get_version()}`\nDescription: `{project_desc_trunc}`\nStatus: `Initializing...`",
            inline=False
        )
        gen_embed.add_field(name="Console:", value="```\nInitializing...\n```", inline=False)
        gen_embed.set_footer(text=f"CSky Developments • Requested by {member.name}", icon_url=help_embeds.FOOTER_ICON)

        msg = await channel.send(embed=gen_embed, view=buttons.create_plugin_cancel_view())
        asyncio.create_task(self._run_generation(gen_embed, msg, channel, project, api_key, member))

    async def _run_generation(self, gen_embed: discord.Embed, message: discord.Message, channel: discord.TextChannel, project: Project, api_key: str, member: discord.Member):
        gemini = GeminiService(api_key)
        builder = Builder(gemini)

        log_channel = self.guild.get_channel(Config.LOG_CHANNEL_ID)
        log_buffer: List[str] = []
        full_log_buffer: List[str] = []

        current_phase = "Initializing"
        current_activity = "Starting system..."
        current_batch = 0
        total_batches = 0
        phase_num = 0
        last_edit_time = 0.0

        loop = asyncio.get_running_loop()

        def sync_log_callback(log_entry: str):
            nonlocal current_phase, current_activity, current_batch, total_batches, phase_num, last_edit_time

            log_buffer.append(log_entry)
            full_log_buffer.append(log_entry)
            if len(log_buffer) > 10:
                log_buffer.pop(0)

            if "Processing Batch" in log_entry:
                m = re.search(r"Batch (\d+)/(\d+)", log_entry)
                if m:
                    current_batch = int(m.group(1))
                    total_batches = int(m.group(2))

            if "[B] +" in log_entry:
                clean_path = re.sub(r"\[.*?\]", "", log_entry).replace("+", "").strip()
                file_name = clean_path.split("/")[-1] if "/" in clean_path else clean_path
                file_name = file_name.split()[0]
                current_activity = f"Generated: {file_name}"

            if "[PHASE" in log_entry:
                m = re.search(r"\[PHASE (\d+)\] (.*)", log_entry)
                if m:
                    phase_num = int(m.group(1))
                    current_phase = m.group(2).strip()

            if "Compilation attempt" in log_entry:
                current_activity = "Compiling source code..."
            elif "AI-assisted fix attempt" in log_entry:
                current_activity = "Fixing compilation errors..."
            elif "Generating documentation" in log_entry:
                current_activity = "Writing README.md..."

            percent = 0.0
            if phase_num == 1:
                percent = 10.0
            elif phase_num == 2:
                batch_base = 15.0
                batch_weight = 65.0
                if total_batches > 0:
                    percent = batch_base + ((current_batch - 1) / total_batches * batch_weight)
                else:
                    percent = 20.0
            elif phase_num == 3:
                percent = 85.0
            elif phase_num == 4:
                percent = 90.0

            if "successfully" in log_entry:
                percent = 100.0

            progress_bar = self._get_progress_bar(int(percent))
            logs_display = "".join((l[:77] + "..." if len(l) > 80 else l) + "\n" for l in log_buffer)

            gen_embed.color = 0x4482FF
            gen_embed.clear_fields()
            gen_embed.add_field(
                name="Project Info",
                value=f"**Name:** {project.get_name()}\n**Version:** `{project.get_version()}`\n**Phase:** `{current_phase}`",
                inline=True
            )
            gen_embed.add_field(
                name="Forge Progress",
                value=f"**Status:** {int(percent)}%\n{progress_bar}\n**Activity:** `{current_activity}`",
                inline=False
            )
            gen_embed.add_field(
                name="Console Output",
                value=f"```ml\n{logs_display}```",
                inline=False
            )

            now = time.time()
            if now - last_edit_time >= 1.5 or percent >= 100.0:
                last_edit_time = now
                asyncio.run_coroutine_threadsafe(message.edit(embed=gen_embed), loop)

        # Run Builder in thread
        await asyncio.to_thread(builder.build, project, sync_log_callback)

        releases_dir = project.get_path() / "releases"
        jar_files = list(releases_dir.glob("*.jar")) if releases_dir.exists() else []
        readme_file = project.get_path() / "sourcecode" / project.get_name() / "README.md"

        build_log_file = Path(os.environ.get("TEMP", "/tmp")) / "build.log"
        try:
            build_log_file.write_text("\n".join(full_log_buffer), encoding="utf-8")
        except Exception as ex:
            BotLogger.error(f"Failed to write build log file: {ex}", False)

        if jar_files:
            jar_file = jar_files[0]
            readme_text = "No documentation provided."
            if readme_file.exists():
                try:
                    raw_readme = readme_file.read_text(encoding="utf-8")
                    readme_text = re.sub(r"[#*_`~>\-]", "", raw_readme)
                    readme_text = re.sub(r"\[.*?\]\(.*?\)", "", readme_text).strip()
                    if len(readme_text) > 1000:
                        readme_text = readme_text[:1000] + "..."
                except Exception:
                    readme_text = "README details currently unavailable."

            gen_embed.color = 0x2ECC71
            gen_embed.description = (
                "Your plugin has been successfully generated!\n"
                "> **Reminder:** Please test generated builds on a **non-production server** before deploying them live.\n"
                "> **Security Note:** This ticket will be **automatically deleted in 6 hours**.\n"
            )
            gen_embed.clear_fields()
            gen_embed.add_field(name="Project Info", value=f"**Name:** {project.get_name()}\n**Version:** `{project.get_version()}`", inline=True)
            gen_embed.add_field(name="Forge Status", value=f"**Status:** `✔ COMPLETED`\n**Artifact:** `{jar_file.name}`", inline=True)
            doc_preview = (readme_text[:497] + "...") if len(readme_text) > 500 else readme_text
            gen_embed.add_field(name="Documentation", value=f"```ml\n{doc_preview}\n```", inline=False)
            gen_embed.timestamp = datetime.now(timezone.utc)

            await message.edit(embed=gen_embed, view=None)
            await channel.send(file=discord.File(str(jar_file), filename=jar_file.name))

            if log_channel and isinstance(log_channel, discord.TextChannel):
                BotLogger.info(f"Artifact Forge Completed for **{project.get_name()}**", True)
                if build_log_file.exists():
                    await log_channel.send(file=discord.File(str(build_log_file), filename="build.log"))
                if readme_file.exists():
                    await log_channel.send(file=discord.File(str(readme_file), filename="README.md"))
                await log_channel.send(file=discord.File(str(jar_file), filename=jar_file.name))

            # Auto-delete after 6 hours
            asyncio.create_task(self._delayed_delete(channel, 6 * 3600))
        else:
            gen_embed.title = "Generation Failed"
            gen_embed.color = 0xE74C3C
            gen_embed.description = (
                "The build process was unable to complete and no JAR file was generated.\n"
                "This may occur due to configuration issues or invalid source output. Please try generating again.\n"
            )
            gen_embed.clear_fields()
            gen_embed.add_field(name="Project Info", value=f"**Name:** {project.get_name()}\n**Version:** `{project.get_version()}`", inline=True)
            gen_embed.add_field(name="Forge Status", value="**Status:** `❌ FAILED`\n**Error:** `Critical systems failure during synthesis`", inline=True)
            gen_embed.timestamp = datetime.now(timezone.utc)
            await message.edit(embed=gen_embed)
            BotLogger.info(f"Generation failed for {project.get_name()}** — No JAR produced.", True)

    async def _delayed_delete(self, channel: discord.TextChannel, delay_seconds: int):
        await asyncio.sleep(delay_seconds)
        try:
            await channel.delete()
        except Exception:
            pass

    def _get_progress_bar(self, percent: int) -> str:
        length = 12
        filled = int(length * (percent / 100.0))
        sb = ["`["]
        for i in range(length):
            sb.append("█" if i < filled else "░")
        sb.append("]`")
        return "".join(sb)

    async def handle_close_confirm(self, interaction: discord.Interaction, member: discord.Member, channel: discord.TextChannel, ticket_type: TicketType):
        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=False),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        try:
            for target, overwrite in overwrites.items():
                await channel.set_permissions(target, overwrite=overwrite)
        except Exception as e:
            BotLogger.error(f"Failed to update channel permissions: {e}")

        desc_map = {
            TicketType.NORMAL: f"The ticket has been closed by {interaction.user.mention}! Please click on the **Delete** button below to delete the ticket permanently.",
            TicketType.ORDER: f"The order has been canceled by {interaction.user.mention}! Please click on the **Delete** button below to remove the order permanently.",
            TicketType.PLUGIN_GEN: f"The plugin generation ticket has been canceled by {interaction.user.mention}! Click the **Delete** button below to delete the generation permanently.",
            TicketType.REWARD: f"The reward claim ticket has been closed by {interaction.user.mention}! Click on the **Delete** button below to delete the ticket permanently.",
            TicketType.STAFF_APP: f"The application has been closed by {interaction.user.mention}! Please click on the **Delete** button below to delete the application permanently."
        }
        view_map = {
            TicketType.NORMAL: buttons.create_ticket_delete_view(),
            TicketType.ORDER: buttons.create_order_delete_view(),
            TicketType.PLUGIN_GEN: buttons.create_plugin_delete_view(),
            TicketType.REWARD: buttons.create_reward_delete_view(),
            TicketType.STAFF_APP: buttons.create_app_delete_view()
        }

        reply_embed = discord.Embed(
            description=desc_map.get(ticket_type, "Closed."),
            color=0x4482FF
        )
        reply_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)

        await interaction.response.send_message(
            embed=reply_embed,
            view=view_map.get(ticket_type, buttons.create_ticket_delete_view()),
            ephemeral=False
        )

    async def handle_delete_ticket(self, interaction: discord.Interaction, member: discord.Member, channel: discord.TextChannel, ticket_type: TicketType):
        has_staff_role = any(r.id == Config.STAFF_ROLE_ID for r in member.roles) if isinstance(member, discord.Member) else False
        if not has_staff_role:
            no_perms = discord.Embed(
                title="**NO PERMISSIONS**",
                description="**You must be a staff member to do that.**",
                color=0x0090FF
            )
            no_perms.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
            await interaction.response.send_message(embed=no_perms, ephemeral=True, delete_after=10)
            return

        channel_tag = getattr(channel, "name", str(channel.id))
        BotLogger.info(f"Deleting `{channel_tag}`...", True)

        deleting_embed = discord.Embed(title="Deleting...", color=0x0090FF)
        await interaction.response.send_message(embed=deleting_embed, ephemeral=True, delete_after=5)

        await self._save_ticket_transcript(ticket_type, channel)
        try:
            await channel.delete()
            BotLogger.info(f"Successfully deleted `{channel_tag}`!", True)
        except Exception as e:
            BotLogger.error(f"An error occurred while deleting the ticket {channel_tag}: {e}", False)

    async def _save_ticket_transcript(self, ticket_type: TicketType, channel: discord.TextChannel):
        name_map = {
            TicketType.NORMAL: "ticket",
            TicketType.ORDER: "order",
            TicketType.PLUGIN_GEN: "plugin generation",
            TicketType.REWARD: "reward ticket",
            TicketType.STAFF_APP: "staff application"
        }
        ticket_name = name_map.get(ticket_type, "ticket")

        lines = [
            "----------------------------------------",
            f"Channel ID: {channel.id}",
            f"Ticket Type: {ticket_name}",
            f"Channel Name: {getattr(channel, 'name', channel.id)}",
            f"Closed At: {datetime.now(timezone.utc).isoformat()}",
            "----------------------------------------\n",
            "Messages:\n"
        ]

        try:
            messages = [m async for m in channel.history(limit=1000)]
            messages.reverse()

            for msg in messages:
                att_str = "".join(f" [Attachment: {a.url}]" for a in msg.attachments)
                lines.append(f"{msg.created_at.isoformat()} {msg.author.name}: {msg.content}{att_str}")

            transcript_content = "\n".join(lines)
            timestamp_ms = int(time.time() * 1000)
            file_name = f"{ticket_name.replace(' ', '_')}_{channel.id}_{timestamp_ms}.txt"
            file_path = Path("data") / "tickets" / file_name
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(transcript_content, encoding="utf-8")

            BotLogger.info(f"Saved {channel.mention} messages to {file_path}", False)

            log_channel = self.guild.get_channel(Config.LOG_CHANNEL_ID)
            if log_channel and isinstance(log_channel, discord.TextChannel):
                await log_channel.send(file=discord.File(str(file_path), filename=file_name))
                BotLogger.info(f"Successfully sent ticket log to log channel: {file_name}", False)
            else:
                BotLogger.error(f"Ticket log channel not found or misconfigured (ID: {Config.LOG_CHANNEL_ID}). Skipping upload.", False)
        except Exception as ex:
            BotLogger.error(f"Failed to save {ticket_name} messages for `{channel.name}`: {ex}", False)

    async def handle_ticket_member_add(self, channel: discord.TextChannel, member: discord.Member):
        try:
            await channel.set_permissions(member, view_channel=True)
        except Exception as e:
            BotLogger.error(f"Failed to add member to ticket: {e}")

    async def handle_ticket_member_remove(self, channel: discord.TextChannel, member: discord.Member):
        try:
            await channel.set_permissions(member, overwrite=None)
        except Exception as e:
            BotLogger.error(f"Failed to remove member from ticket: {e}")
