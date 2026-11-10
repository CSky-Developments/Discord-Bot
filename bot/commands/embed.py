from typing import Optional
import discord
from discord import app_commands
from bot.ticket import buttons
from bot.embeds import (
    help_embeds,
    reward_embeds,
    service_embeds,
    ticket_embeds,
)
from bot.commands.ticket import is_staff, make_no_permission_embed

CATEGORIES = [
    "Service Not Available",
    "Building",
    "Texture Pack",
    "Server Setup",
    "Hosting Services",
    "Server Optimization",
    "Plugin Development",
    "Ticket",
    "Order",
    "Plugin Generation",
    "Reward",
    "Staff Application",
]

EMBED_TYPES = [
    "Invite",
    "Booster",
    "Dirt Plan",
    "Wood Plan",
    "Coal Plan",
    "Stone Plan",
    "Iron Plan",
    "Gold Plan",
    "Diamond Plan",
    "Netherite Plan",
    "Payments",
]

def setup_embed_command(tree: app_commands.CommandTree, guild: discord.Object):
    @tree.command(name="embed", description="Use to send embeds.", guild=guild)
    @app_commands.describe(
        category="Select a category",
        embed="Select an embed within the category",
        send_all="Send all embeds from the category"
    )
    @app_commands.choices(category=[
        app_commands.Choice(name=c, value=c) for c in CATEGORIES
    ])
    @app_commands.choices(embed=[
        app_commands.Choice(name=e, value=e) for e in EMBED_TYPES
    ])
    async def embed_cmd(
        interaction: discord.Interaction,
        category: app_commands.Choice[str],
        embed: Optional[app_commands.Choice[str]] = None,
        send_all: Optional[bool] = False
    ):
        if not is_staff(interaction.user):
            await interaction.response.send_message(embed=make_no_permission_embed(), ephemeral=True, delete_after=10)
            return

        cat_val = category.value
        embed_val = embed.value if embed else None
        channel = interaction.channel

        if send_all and embed_val and cat_val != "Reward":
            await interaction.response.send_message(
                "❌ Cannot specify an embed and also use 'send_all' for this category. Please choose one.",
                ephemeral=True
            )
            return

        async def send_confirmation():
            await interaction.response.send_message("✅ Sent!", ephemeral=True, delete_after=10)

        async def send_with_order(emb: discord.Embed):
            await channel.send(embed=emb)
            await channel.send(embed=ticket_embeds.make_order_embed(), view=buttons.create_order_create_view())
            await send_confirmation()

        if send_all:
            if cat_val == "Service Not Available":
                await channel.send(embed=help_embeds.make_not_available_embed())
            elif cat_val == "Building":
                await channel.send(embed=service_embeds.make_building_embed())
                await channel.send(embed=service_embeds.make_service_order_embed(color=0xF35A46), view=buttons.create_order_create_view())
            elif cat_val == "Texture Pack":
                await channel.send(embed=service_embeds.make_texture_pack_embed())
                await channel.send(embed=service_embeds.make_service_order_embed(color=0x6AAFB8), view=buttons.create_order_create_view())
            elif cat_val == "Server Setup":
                await channel.send(embed=service_embeds.make_server_setup_embed())
                await channel.send(embed=service_embeds.make_service_order_embed(color=0x4DAEE1), view=buttons.create_order_create_view())
            elif cat_val == "Server Optimization":
                await channel.send(embed=service_embeds.make_server_optimization_embed())
                await channel.send(embed=service_embeds.make_service_order_embed(color=0xE5B432), view=buttons.create_order_create_view())
            elif cat_val == "Plugin Development":
                await channel.send(embed=service_embeds.make_plugin_development_embed())
                await channel.send(embed=service_embeds.make_service_order_embed(color=0x938FF1), view=buttons.create_order_create_view())
            elif cat_val == "Plugin Generation":
                await channel.send(embed=ticket_embeds.make_plugin_gen_embed(), view=buttons.create_plugin_generate_view())
            elif cat_val == "Reward":
                if embed_val:
                    if embed_val == "Invite":
                        await channel.send(embed=reward_embeds.make_invite_reward_embed())
                    elif embed_val == "Booster":
                        await channel.send(embed=reward_embeds.make_booster_reward_embed())
                    else:
                        await interaction.response.send_message("❌ Invalid reward embed type. Please select either `Invite` or `Booster`.", ephemeral=True)
                        return
                else:
                    await channel.send(embed=reward_embeds.make_invite_reward_embed())
                    await channel.send(embed=reward_embeds.make_booster_reward_embed())
            elif cat_val == "Hosting Services":
                hosting_embeds = [
                    service_embeds.make_dirt_plan_embed(),
                    service_embeds.make_wood_plan_embed(),
                    service_embeds.make_coal_plan_embed(),
                    service_embeds.make_stone_plan_embed(),
                    service_embeds.make_iron_plan_embed(),
                    service_embeds.make_gold_plan_embed(),
                    service_embeds.make_diamond_plan_embed(),
                    service_embeds.make_netherite_plan_embed(),
                ]
                for he in hosting_embeds:
                    await channel.send(embed=he)
                await channel.send(embed=service_embeds.make_locations_payments_embed(), view=buttons.create_server_order_create_view())
            else:
                await interaction.response.send_message("❌ Cannot send all embeds for unknown category.", ephemeral=True)
                return

            await send_confirmation()
            return

        # Single embed sending
        if cat_val == "Service Not Available":
            await channel.send(embed=help_embeds.make_not_available_embed())
            await send_confirmation()
        elif cat_val == "Ticket":
            await channel.send(embed=ticket_embeds.make_ticket_embed(), view=buttons.create_ticket_create_view())
            await send_confirmation()
        elif cat_val == "Plugin Generation":
            await channel.send(embed=ticket_embeds.make_plugin_gen_embed(), view=buttons.create_plugin_generate_view())
            await send_confirmation()
        elif cat_val == "Order":
            await channel.send(embed=ticket_embeds.make_order_embed(), view=buttons.create_order_create_view())
            await send_confirmation()
        elif cat_val == "Staff Application":
            await channel.send(embed=ticket_embeds.make_staff_app_embed(), view=buttons.create_app_create_view())
            await send_confirmation()
        elif cat_val == "Building":
            await send_with_order(service_embeds.make_building_embed())
        elif cat_val == "Texture Pack":
            await send_with_order(service_embeds.make_texture_pack_embed())
        elif cat_val == "Server Setup":
            await send_with_order(service_embeds.make_server_setup_embed())
        elif cat_val == "Server Optimization":
            await send_with_order(service_embeds.make_server_optimization_embed())
        elif cat_val == "Plugin Development":
            await send_with_order(service_embeds.make_plugin_development_embed())
        elif cat_val == "Reward":
            if not embed_val:
                await interaction.response.send_message("❌ Please select either `Invite` or `Booster` reward embed.", ephemeral=True)
                return
            if embed_val == "Invite":
                await channel.send(embed=reward_embeds.make_invite_reward_embed())
                await channel.send(embed=ticket_embeds.make_reward_embed(), view=buttons.create_reward_claim_view())
            elif embed_val == "Booster":
                await channel.send(embed=reward_embeds.make_booster_reward_embed())
                await channel.send(embed=ticket_embeds.make_reward_embed(), view=buttons.create_reward_claim_view())
            else:
                await interaction.response.send_message("❌ Invalid reward embed type.", ephemeral=True)
                return
            await send_confirmation()
        elif cat_val == "Hosting Services":
            if not embed_val:
                await interaction.response.send_message("❌ Please specify a hosting embed to send.", ephemeral=True)
                return

            embed_map = {
                "Dirt Plan": service_embeds.make_dirt_plan_embed,
                "Wood Plan": service_embeds.make_wood_plan_embed,
                "Coal Plan": service_embeds.make_coal_plan_embed,
                "Stone Plan": service_embeds.make_stone_plan_embed,
                "Iron Plan": service_embeds.make_iron_plan_embed,
                "Gold Plan": service_embeds.make_gold_plan_embed,
                "Diamond Plan": service_embeds.make_diamond_plan_embed,
                "Netherite Plan": service_embeds.make_netherite_plan_embed,
                "Payments": service_embeds.make_locations_payments_embed,
            }
            factory = embed_map.get(embed_val)
            if not factory:
                await interaction.response.send_message("❌ Invalid hosting embed.", ephemeral=True)
                return

            if embed_val == "Payments":
                await channel.send(embed=factory(), view=buttons.create_server_order_create_view())
            else:
                await channel.send(embed=factory())
            await send_confirmation()
        else:
            await interaction.response.send_message("❌ Unknown category.", ephemeral=True)
