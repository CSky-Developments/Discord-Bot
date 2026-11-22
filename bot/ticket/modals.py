from typing import TYPE_CHECKING
import discord
from discord.ui import Modal, TextInput

if TYPE_CHECKING:
    from bot.ticket.manager import TicketManager


class CommissionOrderModal(Modal, title="Commission Order Request"):
    service = TextInput(
        label="Service Required",
        placeholder="Custom Plugin, Resource Pack, Optimization, or Setup",
        max_length=100,
        required=True,
    )
    track = TextInput(
        label="Commission Track",
        placeholder="Public (40-60% Off) or Private (100% Exclusive)",
        max_length=80,
        required=True,
    )
    budget = TextInput(
        label="Estimated Budget",
        placeholder="e.g. Under $50, $50 - $150, $150 - $350, $350+",
        max_length=60,
        required=True,
    )
    specs = TextInput(
        label="Project Specifications & Stack",
        style=discord.TextStyle.paragraph,
        placeholder="Minecraft version (e.g. Paper 26.3), key mechanics, commands, or deadlines...",
        max_length=1000,
        required=True,
    )

    def __init__(self, ticket_manager: "TicketManager"):
        super().__init__()
        self.ticket_manager = ticket_manager

    async def on_submit(self, interaction: discord.Interaction):
        await self.ticket_manager.create_order_ticket_from_modal(
            interaction=interaction,
            member=interaction.user,
            service=self.service.value.strip(),
            track=self.track.value.strip(),
            budget=self.budget.value.strip(),
            specs=self.specs.value.strip(),
        )


class StaffApplicationModal(Modal):
    def __init__(self, ticket_manager: "TicketManager", role_name: str):
        super().__init__(title=f"Staff Application — {role_name}")
        self.ticket_manager = ticket_manager
        self.role_name = role_name

        role_prompts = {
            "Developer": (
                "Portfolio & Java / Paper Stack",
                "GitHub links, Paper/Purpur/Folia/Velocity projects, or 16x resource packs...",
            ),
            "Moderator": (
                "Conflict & Rule Enforcement Approach",
                "How do you handle heated disputes, rule violations, and stay impartial?",
            ),
            "Supporter": (
                "Technical Support & Troubleshooting",
                "How do you handle multiple player tickets, bug reports, and onboarding?",
            ),
            "Marketing": (
                "Marketing Ideas & Community Knowledge",
                "Which Minecraft trends/communities do you follow? Share your best idea to promote CSky, plus any big servers, YouTube channels or SMP communities you're part of or connected to...",
            ),
            "Creator": (
                "Content & Channels / Connections",
                "Links to your YouTube/TikTok/social channels, audience size, content examples, and any creators or communities you could collab with...",
            ),
        }
        prompt_label, prompt_placeholder = role_prompts.get(
            role_name,
            ("Role-Specific Experience", "Describe your relevant skills and past work..."),
        )

        self.age_tz = TextInput(
            label="Age & Timezone",
            placeholder="e.g. 19 / UTC+0",
            max_length=60,
            required=True,
        )
        self.experience = TextInput(
            label="Previous Experience",
            style=discord.TextStyle.paragraph,
            placeholder="Summarize previous servers, teams, or projects you have worked with...",
            max_length=800,
            required=True,
        )
        self.role_details = TextInput(
            label=prompt_label,
            style=discord.TextStyle.paragraph,
            placeholder=prompt_placeholder,
            max_length=800,
            required=True,
        )
        self.availability = TextInput(
            label="Weekly Availability",
            placeholder="e.g. 15–20 hours per week",
            max_length=80,
            required=True,
        )
        self.motivation = TextInput(
            label="Why CSky Developments?",
            style=discord.TextStyle.paragraph,
            placeholder="What interests you about joining CSky Developments?",
            max_length=600,
            required=True,
        )

        self.add_item(self.age_tz)
        self.add_item(self.experience)
        self.add_item(self.role_details)
        self.add_item(self.availability)
        self.add_item(self.motivation)

    async def on_submit(self, interaction: discord.Interaction):
        await self.ticket_manager.create_staff_app_ticket_from_modal(
            interaction=interaction,
            member=interaction.user,
            role_name=self.role_name,
            age_tz=self.age_tz.value.strip(),
            experience=self.experience.value.strip(),
            role_details=self.role_details.value.strip(),
            availability=self.availability.value.strip(),
            motivation=self.motivation.value.strip(),
        )
