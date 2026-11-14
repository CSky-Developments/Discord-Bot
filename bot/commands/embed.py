import discord
from discord import app_commands
from bot.ticket import buttons
from bot.embeds import (
    help_embeds,
    service_embeds,
    ticket_embeds,
)
from bot.commands.ticket import is_staff, make_no_permission_embed

CATEGORIES = [
    "Custom Work",
    "Order",
    "Ticket",
    "Staff Application",
    "Service Not Available",
]


def setup_embed_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(name="embed", description="Use to send embeds.", guild=guild)
    @app_commands.describe(category="Select a category")
    @app_commands.choices(
        category=[app_commands.Choice(name=c, value=c) for c in CATEGORIES]
    )
    async def embed_cmd(
        interaction: discord.Interaction,
        category: app_commands.Choice[str],
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(
                embed=make_no_permission_embed(), ephemeral=True, delete_after=10
            )
            return

        cat_val = category.value
        channel = interaction.channel

        if cat_val == "Service Not Available":
            await channel.send(embed=help_embeds.make_not_available_embed())
        elif cat_val == "Ticket":
            await channel.send(
                embed=ticket_embeds.make_ticket_embed(),
                view=buttons.create_ticket_create_view(),
            )
        elif cat_val == "Order":
            await channel.send(
                embed=ticket_embeds.make_order_embed(),
                view=buttons.create_order_create_view(),
            )
        elif cat_val == "Staff Application":
            await channel.send(
                embed=ticket_embeds.make_staff_app_embed(),
                view=buttons.create_app_create_view(),
            )
        elif cat_val == "Custom Work":
            await channel.send(
                embed=service_embeds.make_custom_work_embed(),
                view=buttons.create_order_create_view(),
            )
        else:
            await interaction.response.send_message("Unknown category.", ephemeral=True)
            return

        await interaction.response.send_message("Sent.", ephemeral=True, delete_after=10)
