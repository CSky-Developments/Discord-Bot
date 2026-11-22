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
from bot.ticket.modals import CommissionOrderModal, StaffApplicationModal
from bot.embeds import ticket_embeds, help_embeds

DATA_FILE = os.path.join("data", "ticket_data.json")
_CREATOR_TOPIC_RE = re.compile(r"Ticket Creator:\s*(\d{17,20})")


def is_staff(member: discord.abc.User) -> bool:
    if not isinstance(member, discord.Member):
        return False
    if member.guild_permissions.administrator:
        return True
    return any(r.id == Config.STAFF_ROLE_ID for r in getattr(member, "roles", []))

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
        self._action_locks: Dict[int, asyncio.Lock] = {}
        self._processed_messages: set[int] = set()
        self.load_ticket_data()

    def _get_message_lock(self, message_id: int) -> asyncio.Lock:
        lock = self._action_locks.get(message_id)
        if lock is None:
            lock = asyncio.Lock()
            self._action_locks[message_id] = lock
        return lock

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

    def _peek_ticket_id(self, ticket_type: TicketType) -> str:
        if ticket_type == TicketType.NORMAL:
            tid = self.ticket_data.normal_ticket_id
        elif ticket_type == TicketType.ORDER:
            tid = self.ticket_data.order_ticket_id
        elif ticket_type == TicketType.STAFF_APP:
            tid = self.ticket_data.staff_app_ticket_id
        else:
            tid = 1
        return f"{tid:04d}"

    def _commit_ticket_id(self, ticket_type: TicketType):
        if ticket_type == TicketType.NORMAL:
            tid = self.ticket_data.normal_ticket_id
            self.ticket_data.normal_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.ORDER:
            tid = self.ticket_data.order_ticket_id
            self.ticket_data.order_ticket_id = 0 if tid >= 9999 else tid + 1
        elif ticket_type == TicketType.STAFF_APP:
            tid = self.ticket_data.staff_app_ticket_id
            self.ticket_data.staff_app_ticket_id = 0 if tid >= 9999 else tid + 1
        self.save_ticket_data()

    def get_ticket_id(self, ticket_type: TicketType) -> str:
        formatted = self._peek_ticket_id(ticket_type)
        self._commit_ticket_id(ticket_type)
        return formatted

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
            await interaction.response.send_modal(CommissionOrderModal(self))
        elif custom_id == "Order_Cancel_Button":
            await interaction.response.send_message(
                embed=ticket_embeds.make_order_close_embed(),
                view=buttons.create_order_close_confirm_view(),
                ephemeral=True
            )
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

        elif custom_id == "Commission_Accept_Button":
            await self.handle_commission_accept(interaction, member)
        elif custom_id == "Commission_Decline_Button":
            await self.handle_commission_decline(interaction, member)
        elif custom_id == "Purchase_Ticket_Button":
            await self.handle_purchase_ticket(interaction, member)

        elif custom_id in ("Developer_Button", "Moderator_Button", "Supporter_Button", "Marketing_Button", "Creator_Button"):
            role_name = custom_id.replace("_Button", "")
            await interaction.response.send_modal(StaffApplicationModal(self, role_name))
        elif custom_id in ("Developer_Close_Button", "Moderator_Close_Button", "Supporter_Close_Button", "Marketing_Close_Button", "Creator_Close_Button"):
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
            TicketType.NORMAL: "ticket-",
            TicketType.ORDER: "order-",
            TicketType.STAFF_APP: "app-"
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

        ticket_emoji = emoji_map.get(ticket_type, "🎫・")
        cat_id = category_map.get(ticket_type, 0)
        ticket_name = name_map.get(ticket_type, "ticket")

        category = self.guild.get_channel(cat_id)
        if not category or not isinstance(category, discord.CategoryChannel):
            BotLogger.error(f"Category {cat_id} not found for {ticket_type}", True)
            await interaction.response.send_message("❌ Failed to find ticket category. Please notify staff.", ephemeral=True)
            return

        await interaction.response.defer(ephemeral=True)

        ticket_id = self._peek_ticket_id(ticket_type)
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
                overwrites=overwrites,
                topic=f"Ticket Creator: {member.id}",
            )
        except Exception as e:
            BotLogger.error(f"An error occurred while creating a `{ticket_name}` for `{member.name}`: {e}", False)
            await interaction.followup.send("❌ Failed to create channel. Check permissions.", ephemeral=True)
            return

        self._commit_ticket_id(ticket_type)
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

        await interaction.followup.send(embed=reply_embed, ephemeral=True)

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

    def _resolve_ticket_creator(self, channel: discord.TextChannel) -> Optional[discord.Member]:
        topic = getattr(channel, "topic", None) or ""
        match = _CREATOR_TOPIC_RE.search(topic)
        if match:
            creator = self.guild.get_member(int(match.group(1)))
            if creator:
                return creator
        return None

    async def handle_close_confirm(self, interaction: discord.Interaction, member: discord.Member, channel: discord.TextChannel, ticket_type: TicketType):
        expected_cat = {
            TicketType.NORMAL: Config.TICKET_NORMAL,
            TicketType.ORDER: Config.TICKET_ORDER,
            TicketType.STAFF_APP: Config.TICKET_STAFF_APP,
        }.get(ticket_type)
        if not channel or getattr(channel, "category_id", None) != expected_cat:
            await interaction.response.send_message(
                "> **🚫 You can't use this here!**",
                ephemeral=True,
                delete_after=10,
            )
            return

        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites: Dict[Any, discord.PermissionOverwrite] = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        creator = self._resolve_ticket_creator(channel)
        if creator and not self._is_staff_member(creator):
            overwrites[creator] = discord.PermissionOverwrite(view_channel=False)

        # Also revoke view_channel for any non-staff member with explicit view_channel=True overwrite
        for target, overwrite in getattr(channel, "overwrites", {}).items():
            if isinstance(target, discord.Member) and overwrite.view_channel is True:
                if not self._is_staff_member(target):
                    overwrites[target] = discord.PermissionOverwrite(view_channel=False)

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
        if not self._is_staff_member(member):
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

    def _is_staff_member(self, member: discord.abc.User) -> bool:
        return is_staff(member)

    def _resolve_member_from_contact(self, contact_raw: str) -> Optional[discord.Member]:
        cleaned = contact_raw.strip().strip("`").lstrip("@").strip()
        if not cleaned or "@" in cleaned:
            return None

        # Numeric Discord user ID or <@id>
        id_match = re.fullmatch(r"(?:<@!?)?(\d{17,20})>?", cleaned)
        if id_match:
            return self.guild.get_member(int(id_match.group(1)))

        base = cleaned.split("#")[0].strip().lower()
        for m in self.guild.members:
            if m.bot:
                continue
            if str(m).lower() == cleaned.lower():
                return m
            if m.name.lower() == base:
                return m
            if m.global_name and m.global_name.lower() == base:
                return m
            if m.display_name.lower() == base:
                return m
        return None

    async def handle_commission_accept(self, interaction: discord.Interaction, member: discord.abc.User):
        if not self._is_staff_member(member):
            await interaction.response.send_message(
                "Only staff members can accept commission requests.",
                ephemeral=True,
                delete_after=10,
            )
            return

        if not interaction.message or not interaction.message.embeds:
            await interaction.response.send_message("Commission details not found on this message.", ephemeral=True)
            return

        async with self._get_message_lock(interaction.message.id):
            src_embed = interaction.message.embeds[0]
            if interaction.message.id in self._processed_messages or any(f.name == "Status" for f in src_embed.fields):
                await interaction.response.send_message("This commission request has already been processed.", ephemeral=True)
                return

            category = self.guild.get_channel(Config.TICKET_ORDER)
            if not category or not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message(
                    "Order ticket category is not configured.",
                    ephemeral=True,
                )
                return

            field_map = {f.name: f.value for f in src_embed.fields}
            client_name = field_map.get("Client", "Client")
            contact_raw = field_map.get("Contact", "Not provided")

            matched_member = self._resolve_member_from_contact(contact_raw)
            ticket_id = self._peek_ticket_id(TicketType.ORDER)
            channel_name = f"order-{ticket_id}"

            staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            }
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)
            if isinstance(member, discord.Member):
                overwrites[member] = discord.PermissionOverwrite(view_channel=True)
            if matched_member:
                overwrites[matched_member] = discord.PermissionOverwrite(view_channel=True)

            await interaction.response.defer(ephemeral=True)

            try:
                order_channel = await self.guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    overwrites=overwrites,
                    topic=f"Ticket Creator: {matched_member.id}" if matched_member else "",
                )
            except Exception as e:
                BotLogger.error(f"Failed to create commission order ticket: {e}", True)
                await interaction.followup.send("Failed to create order ticket channel.", ephemeral=True)
                return

            self._commit_ticket_id(TicketType.ORDER)
            self._processed_messages.add(interaction.message.id)

        summary_embed = discord.Embed(
            title=src_embed.title or "Accepted Commission Request",
            url=src_embed.url,
            color=0x1A73E8,
        )
        for f in src_embed.fields:
            if f.name != "Status":
                summary_embed.add_field(name=f.name, value=f.value, inline=f.inline)
        summary_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)

        await order_channel.send(embeds=[summary_embed, ticket_embeds.make_order_create_embed()], view=buttons.create_order_close_view())

        updated_embed = discord.Embed(
            title=src_embed.title,
            url=src_embed.url,
            description=src_embed.description,
            color=0x16A34A,
            timestamp=src_embed.timestamp,
        )
        for f in src_embed.fields:
            if f.name != "Status":
                updated_embed.add_field(name=f.name, value=f.value, inline=f.inline)
        updated_embed.add_field(
            name="Status",
            value=f"Accepted by {member.mention} — {order_channel.mention}",
            inline=False,
        )
        if src_embed.footer:
            updated_embed.set_footer(text=src_embed.footer.text, icon_url=src_embed.footer.icon_url)

        await interaction.message.edit(embed=updated_embed, view=buttons.create_commission_request_view(disabled=True))
        await interaction.followup.send(
            f"Order ticket created: {order_channel.mention}"
            + ("" if matched_member else " (client not matched in server automatically; use `/ticket add` if needed)."),
            ephemeral=True,
        )

    async def handle_commission_decline(self, interaction: discord.Interaction, member: discord.abc.User):
        if not self._is_staff_member(member):
            await interaction.response.send_message(
                "Only staff members can decline commission requests.",
                ephemeral=True,
                delete_after=10,
            )
            return

        if not interaction.message or not interaction.message.embeds:
            await interaction.response.send_message("Commission details not found on this message.", ephemeral=True)
            return

        src_embed = interaction.message.embeds[0]
        updated_embed = discord.Embed(
            title=src_embed.title,
            url=src_embed.url,
            description=src_embed.description,
            color=0xDC2626,
            timestamp=src_embed.timestamp,
        )
        for f in src_embed.fields:
            if f.name != "Status":
                updated_embed.add_field(name=f.name, value=f.value, inline=f.inline)
        updated_embed.add_field(
            name="Status",
            value=f"Declined by {member.mention}",
            inline=False,
        )
        if src_embed.footer:
            updated_embed.set_footer(text=src_embed.footer.text, icon_url=src_embed.footer.icon_url)

        await interaction.message.edit(embed=updated_embed, view=buttons.create_commission_request_view(disabled=True))
        await interaction.response.send_message("Commission request declined.", ephemeral=True, delete_after=10)

    async def handle_purchase_ticket(self, interaction: discord.Interaction, member: discord.abc.User):
        if not self._is_staff_member(member):
            await interaction.response.send_message(
                "Only staff members can open support tickets from purchase logs.",
                ephemeral=True,
                delete_after=10,
            )
            return

        if not interaction.message or not interaction.message.embeds:
            await interaction.response.send_message("Purchase details not found on this message.", ephemeral=True)
            return

        async with self._get_message_lock(interaction.message.id):
            src_embed = interaction.message.embeds[0]
            if interaction.message.id in self._processed_messages or any(f.name == "Ticket" for f in src_embed.fields):
                await interaction.response.send_message("A support ticket has already been opened for this purchase.", ephemeral=True)
                return

            category = self.guild.get_channel(Config.TICKET_NORMAL)
            if not category or not isinstance(category, discord.CategoryChannel):
                await interaction.response.send_message("Support ticket category is not configured.", ephemeral=True)
                return

            field_map = {f.name: f.value for f in src_embed.fields}
            buyer_raw = field_map.get("Buyer", "Customer")

            matched_member = None
            mention_match = re.search(r"<@!?(\d{17,20})>", buyer_raw)
            if mention_match:
                matched_member = self.guild.get_member(int(mention_match.group(1)))
            if not matched_member:
                matched_member = self._resolve_member_from_contact(buyer_raw.split("(")[0].strip())

            ticket_id = self._peek_ticket_id(TicketType.NORMAL)
            channel_name = f"ticket-{ticket_id}"

            staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
            overwrites = {
                self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            }
            if staff_role:
                overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)
            if isinstance(member, discord.Member):
                overwrites[member] = discord.PermissionOverwrite(view_channel=True)
            if matched_member:
                overwrites[matched_member] = discord.PermissionOverwrite(view_channel=True)

            await interaction.response.defer(ephemeral=True)

            try:
                ticket_channel = await self.guild.create_text_channel(
                    name=channel_name,
                    category=category,
                    overwrites=overwrites,
                    topic=f"Ticket Creator: {matched_member.id}" if matched_member else "",
                )
            except Exception as e:
                BotLogger.error(f"Failed to create purchase support ticket: {e}", True)
                await interaction.followup.send("Failed to create support ticket channel.", ephemeral=True)
                return

            self._commit_ticket_id(TicketType.NORMAL)
            self._processed_messages.add(interaction.message.id)

        summary_embed = discord.Embed(
            title=src_embed.title or "Store Purchase Support",
            url=src_embed.url,
            color=0x16A34A,
        )
        for f in src_embed.fields:
            if f.name != "Ticket":
                summary_embed.add_field(name=f.name, value=f.value, inline=f.inline)
        summary_embed.set_footer(text="CSky Store • store.csky.dev", icon_url=help_embeds.FOOTER_ICON)

        await ticket_channel.send(
            embeds=[summary_embed, ticket_embeds.make_ticket_create_embed()],
            view=buttons.create_ticket_close_view(),
        )

        updated_embed = discord.Embed(
            title=src_embed.title,
            url=src_embed.url,
            description=src_embed.description,
            color=src_embed.color or 0x16A34A,
            timestamp=src_embed.timestamp,
        )
        if src_embed.author:
            updated_embed.set_author(
                name=src_embed.author.name,
                url=src_embed.author.url,
                icon_url=src_embed.author.icon_url,
            )
        for f in src_embed.fields:
            if f.name != "Ticket":
                updated_embed.add_field(name=f.name, value=f.value, inline=f.inline)
        updated_embed.add_field(
            name="Ticket",
            value=f"{ticket_channel.mention} (opened by {member.mention})",
            inline=False,
        )
        if src_embed.image and src_embed.image.url:
            updated_embed.set_image(url=src_embed.image.url)
        if src_embed.footer:
            updated_embed.set_footer(text=src_embed.footer.text, icon_url=src_embed.footer.icon_url)

        product_url = src_embed.url or "https://store.csky.dev"
        await interaction.message.edit(embed=updated_embed, view=buttons.create_purchase_view(product_url, disabled=True))
        await interaction.followup.send(
            f"Support ticket created: {ticket_channel.mention}"
            + ("" if matched_member else " (buyer not matched in server automatically; use `/ticket add` if needed)."),
            ephemeral=True,
        )

    async def create_order_ticket_from_modal(
        self,
        interaction: discord.Interaction,
        member: discord.abc.User,
        service: str,
        track: str,
        budget: str,
        specs: str,
    ):
        category = self.guild.get_channel(Config.TICKET_ORDER)
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "Order ticket category is not configured. Please notify staff.",
                ephemeral=True,
            )
            return

        ticket_id = self._peek_ticket_id(TicketType.ORDER)
        channel_name = f"order-{ticket_id}"
        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        await interaction.response.defer(ephemeral=True)

        try:
            channel = await self.guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                topic=f"Ticket Creator: {member.id}",
            )
        except Exception as e:
            BotLogger.error(f"Failed to create modal order ticket for `{member.name}`: {e}", False)
            await interaction.followup.send("Failed to create order channel. Check permissions.", ephemeral=True)
            return

        self._commit_ticket_id(TicketType.ORDER)

        is_public = "public" in track.lower()
        brief_embed = discord.Embed(
            title=f"Commission Request — {service}",
            url="https://csky.dev/contact",
            color=0x137333 if is_public else 0x1A73E8,
        )
        brief_embed.set_author(name=f"Client: {member.display_name}", icon_url=member.display_avatar.url)
        brief_embed.add_field(name="Client", value=member.mention, inline=True)
        brief_embed.add_field(name="Service", value=service, inline=True)
        brief_embed.add_field(name="Estimated Budget", value=f"`{budget}`", inline=True)
        brief_embed.add_field(name="Commission Track", value=track, inline=False)
        brief_embed.add_field(name="Project Specifications & Stack", value=specs, inline=False)
        brief_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
        brief_embed.timestamp = discord.utils.utcnow()

        await channel.send(
            embeds=[brief_embed, ticket_embeds.make_order_create_embed()],
            view=buttons.create_order_close_view(),
        )

        reply_embed = discord.Embed(
            description=f"Your order ticket has been created in {channel.mention}.",
            color=0x1A73E8,
        )
        reply_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
        await interaction.followup.send(embed=reply_embed, ephemeral=True)

    async def create_staff_app_ticket_from_modal(
        self,
        interaction: discord.Interaction,
        member: discord.abc.User,
        role_name: str,
        age_tz: str,
        experience: str,
        role_details: str,
        availability: str,
        motivation: str,
    ):
        category = self.guild.get_channel(Config.TICKET_STAFF_APP)
        if not category or not isinstance(category, discord.CategoryChannel):
            await interaction.response.send_message(
                "Staff application category is not configured. Please notify staff.",
                ephemeral=True,
            )
            return

        ticket_id = self._peek_ticket_id(TicketType.STAFF_APP)
        channel_name = f"app-{ticket_id}"
        staff_role = self.guild.get_role(Config.STAFF_ROLE_ID)
        overwrites = {
            self.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            member: discord.PermissionOverwrite(view_channel=True),
        }
        if staff_role:
            overwrites[staff_role] = discord.PermissionOverwrite(view_channel=True)

        await interaction.response.defer(ephemeral=True)

        try:
            channel = await self.guild.create_text_channel(
                name=channel_name,
                category=category,
                overwrites=overwrites,
                topic=f"Ticket Creator: {member.id}",
            )
        except Exception as e:
            BotLogger.error(f"Failed to create modal staff app for `{member.name}`: {e}", False)
            await interaction.followup.send("Failed to create application channel. Check permissions.", ephemeral=True)
            return

        self._commit_ticket_id(TicketType.STAFF_APP)

        app_embed = discord.Embed(
            title=f"Staff Application — {role_name}",
            url="https://csky.dev/about",
            color=0x1A73E8,
        )
        app_embed.set_author(name=f"Applicant: {member.display_name}", icon_url=member.display_avatar.url)
        app_embed.add_field(name="Applicant", value=member.mention, inline=True)
        app_embed.add_field(name="Age & Timezone", value=f"`{age_tz}`", inline=True)
        app_embed.add_field(name="Availability", value=f"`{availability}`", inline=True)
        app_embed.add_field(name="Previous Experience", value=experience, inline=False)
        app_embed.add_field(name="Role-Specific Details", value=role_details, inline=False)
        app_embed.add_field(name="Why CSky Developments?", value=motivation, inline=False)
        app_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
        app_embed.timestamp = discord.utils.utcnow()

        close_view_map = {
            "Developer": buttons.create_developer_close_view,
            "Moderator": buttons.create_moderator_close_view,
            "Supporter": buttons.create_supporter_close_view,
            "Marketing": buttons.create_marketing_close_view,
            "Creator": buttons.create_creator_close_view,
        }
        close_view = close_view_map.get(role_name, buttons.create_ticket_close_view)()

        await channel.send(
            embeds=[app_embed, ticket_embeds.make_staff_app_create_embed()],
            view=close_view,
        )

        reply_embed = discord.Embed(
            description=f"Your **{role_name}** application has been opened in {channel.mention}.",
            color=0x1A73E8,
        )
        reply_embed.set_footer(text=help_embeds.FOOTER_TEXT, icon_url=help_embeds.FOOTER_ICON)
        await interaction.followup.send(embed=reply_embed, ephemeral=True)
