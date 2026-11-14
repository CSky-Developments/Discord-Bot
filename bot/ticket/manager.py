import os
import json
import time
import asyncio
import re
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import discord

from bot.config import Config
from bot.logger import BotLogger
from bot.ticket.types import TicketType
from bot.ticket import buttons
from bot.embeds import ticket_embeds, help_embeds

DATA_FILE = os.path.join("data", "ticket_data.json")

class TicketData:
    def __init__(self):
        self.normal_ticket_id = 1
        self.order_ticket_id = 1
        self.staff_app_ticket_id = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            "normalTicketID": self.normal_ticket_id,
            "orderTicketID": self.order_ticket_id,
            "staffAppTicketID": self.staff_app_ticket_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TicketData":
        td = cls()
        td.normal_ticket_id = data.get("normalTicketID", 1)
        td.order_ticket_id = data.get("orderTicketID", 1)
        td.staff_app_ticket_id = data.get("staffAppTicketID", 1)
        return td

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
        emoji_map = {
            TicketType.NORMAL: "ðŸŽ«ãƒ»",
            TicketType.ORDER: "ðŸ›’ãƒ»",
            TicketType.STAFF_APP: "ðŸŽ“ãƒ»"
        }
        category_map = {
            TicketType.NORMAL: Config.TICKET_NORMAL,
            TicketType.ORDER: Config.TICKET_ORDER,
            TicketType.STAFF_APP: Config.TICKET_STAFF_APP
        }
        name_map = {
            TicketType.NORMAL: "ticket",
            TicketType.ORDER: "order",
            TicketType.STAFF_APP: "staff application"
        }

        ticket_emoji = emoji_map.get(ticket_type, "ðŸŽ«ãƒ»")
        cat_id = category_map.get(ticket_type, 0)
        ticket_name = name_map.get(ticket_type, "ticket")

        category = self.guild.get_channel(cat_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            BotLogger.error(f"Category {cat_id} not found for {ticket_type}", True)
            await interaction.response.send_message("âŒ Failed to find ticket category. Please notify staff.", ephemeral=True)
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
            await interaction.response.send_message("âŒ Failed to create channel. Check permissions.", ephemeral=True)
            return

        BotLogger.info(f"Successfully created a new `{ticket_name}`: `{channel.name}`", True)

        desc_map = {
            TicketType.NORMAL: f"Your ticket has been successfully created in {channel.mention}. We appreciate your patience while we address your request.",
            TicketType.ORDER: f"Your order has been successfully placed in {channel.mention}. We appreciate your patience while our team reviews your request.",
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
            TicketType.STAFF_APP: f"The application has been closed by {interaction.user.mention}! Please click on the **Delete** button below to delete the application permanently."
        }
        view_map = {
            TicketType.NORMAL: buttons.create_ticket_delete_view(),
            TicketType.ORDER: buttons.create_order_delete_view(),
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
