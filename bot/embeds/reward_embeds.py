import discord
from bot.embeds.help_embeds import FOOTER_TEXT, FOOTER_ICON

def make_invite_reward_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Invite・Rewards",
        description=(
            "Invite friends and unlock valuable perks:\n \n"
            "**● 2 Invites** — Access to free resources \n"
            "**● 5 Invites** — Free server optimization \n"
            "**● 7 Invites** — 5% Discount on orders *(Except hosting services)* \n"
            "**● 10 Invites** — 10% Discount on orders *(Except hosting services)* \n \n"
            "**Start inviting now and track your progress with `/invites`!**\n "
        ),
        color=0x00FFFF,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1119317556893855826/1384902539450781706/referral.png?ex=68541e7f&is=6852ccff&hm=c763fe09d307bd274294529df71e0d29ff4a9d04e9af127f605d5592c41a6359&")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_booster_reward_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Boost・Rewards",
        description=(
            "Boost the server and unlock benefits:\n \n"
            "**🔹 1x Boost Includes:**\n"
            "● Free server optimization (1x)\n"
            "● Access to free resources\n"
            "● Exclusive booster role\n"
            "● 5% Discount on orders *(Except hosting services)* \n \n"
            "**🔸 2x Boost Includes:**\n"
            "● Free server optimization (2x)\n"
            "● Access to free resources\n"
            "● Exclusive booster role\n"
            "● 10% Discount on orders *(Except hosting services)* \n \n"
            "**Boost now and get rewarded instantly!**\n "
        ),
        color=0xFF70FF,
    )
    embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/1114515644969386004.webp?size=96&quality=lossless")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
