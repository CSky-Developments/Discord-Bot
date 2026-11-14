import discord
from bot.embeds.help_embeds import (
    FOOTER_TEXT,
    FOOTER_ICON,
    CSKY_SERVICES_URL,
    CSKY_TERMS_URL,
    CSKY_STORE_URL,
)

def make_ticket_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Support Ticket",
        description=(
            "Need help with a store purchase, license, or general inquiry? Click **Create** below to open a private support ticket.\n\n"
            f"• **Store & Downloads:** [store.csky.dev]({CSKY_STORE_URL})\n"
            f"• **Terms & Policies:** [csky.dev/terms]({CSKY_TERMS_URL})"
        ),
        color=0x1A73E8,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Support Ticket Opened",
        description=(
            "Please wait for our staff to arrive. While you wait, share your question, order number, or server logs here.\n\n"
            "If your issue is resolved, click **Close** below."
        ),
        color=0x1A73E8,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to close this ticket?**\nClick **Confirm** to proceed with closing, or **Cancel** to keep it open.",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Ticket closure has been canceled.**",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Commission & Order Service",
        url="https://csky.dev/contact",
        description=(
            "Start a custom plugin, resource pack, server setup, or optimization order. "
            "Click **Place Order** below to open a ticket, or submit your full brief via **[csky.dev/contact](https://csky.dev/contact)**.\n\n"
            "• **Public Track (40%–60% Off):** Discounted build; CSky retains BuiltByBit distribution rights.\n"
            "• **Private Track (100% Exclusive):** Exclusive IP + full Java 21 / Kotlin source delivery.\n\n"
            f"• **Services & Stack:** [csky.dev/services]({CSKY_SERVICES_URL})\n"
            f"• **Ready-Made Store:** [store.csky.dev]({CSKY_STORE_URL})\n"
            f"• **Terms & 14-Day Warranty:** [csky.dev/terms]({CSKY_TERMS_URL})"
        ),
        color=0x1A73E8,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Order Ticket Opened",
        description=(
            "Our team will review your project shortly. Please share your server software, Minecraft version, commission track (Public or Private), specifications, and estimated budget.\n\n"
            f"**Commercial & Billing Policy ([csky.dev/terms]({CSKY_TERMS_URL})):**\n"
            "> • **Deposit:** 50% upfront deposit, 50% upon final sandbox approval.\n"
            "> • **Warranty:** 14-day post-delivery bug fix warranty included.\n"
            "> • **Authorized Billing:** Quotes & payments are handled **only** in this ticket by **Killer_Nova** or **Arsh** via **Tebex**, **Stripe**, or ticket-verified **UPI**."
        ),
        color=0x1A73E8,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to cancel this order?**\nClick **Confirm** to cancel the order, or **Cancel** to keep this ticket open.",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Order cancellation has been canceled.**",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Staff Application**",
        description=(
            "**Thank you for considering a position at CSky Developments, your premier destination for Minecraft server solutions. We are currently looking for talented individuals to join our team in the following roles:**\n"
            "1. **Developer:** As a Developer at CSky Developments, you will be responsible for creating and maintaining plugins, texture packs, custom builds, and server setups. You should have a strong understanding of Java and Minecraft server architecture. Experience with plugin development frameworks, such as Bukkit or Spigot, is highly desirable.\n"
            "2. **Moderator:** In the role of Moderator, you will be entrusted with maintaining a positive and welcoming community environment on our servers. Your responsibilities will include enforcing server rules, resolving conflicts, and assisting players with any issues they may encounter. Good communication and problem-solving skills are essential for this role.\n"
            "3. **Supporter:** As a Supporter, you will provide prompt and efficient assistance to our players, addressing their inquiries, troubleshooting technical problems, and guiding them through gameplay-related challenges. You should have excellent communication skills, a friendly demeanor, and a passion for helping others.\n\n"
            "**To apply for a role, please select the field you are interested in and click on the respective button below. We will review your application and contact you for further steps in the hiring process.**"
        ),
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="Staff Application Received",
        description=(
            "Thank you for applying to **CSky Developments**. Our leadership team will review your submission shortly.\n\n"
            "Feel free to drop any extra portfolio links, code samples, or notes here. "
            "If you wish to withdraw, click **Close** below."
        ),
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to withdraw this application?**\nClick **Confirm** to close, or **Cancel** to keep it open.",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Application withdrawal has been canceled.**",
        color=0x1A73E8,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_developer_questions_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Answer the following.**",
        description=(
            "**1.** Do you have experience in Java programming?\n"
            "**2.** Are you familiar with plugin development frameworks like Bukkit or Spigot?\n"
            "**3.** Have you ever collaborated with other developers on a project? If yes, please explain your role and contribution.\n"
            "**4.** How do you ensure compatibility and performance optimization when developing plugins?\n"
            "**5.** Can you provide examples of plugins or texture packs you have created or worked on?\n"
            "**6.** What is your experience with custom builds and server setups?\n"
            "**7.** Can you describe your experience with server optimization and configuration?\n"
            "**8.** How do you stay updated on the latest trends and developments in the Minecraft modding community?\n"
            "**9.** Can you provide a portfolio or code samples to showcase your programming skills?\n"
            "**10.** Are you comfortable working in a team environment?"
        ),
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_moderator_questions_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Answer the following.**",
        description=(
            "**1.** Have you ever worked as a moderator before? If yes, please describe your experience.\n"
            "**2.** How would you handle a situation where two players are engaged in a heated argument?\n"
            "**3.** What steps would you take to enforce server rules in a fair and consistent manner?\n"
            "**4.** Can you provide an example of a conflict resolution you successfully managed in a gaming community?\n"
            "**5.** How would you handle a player who repeatedly violates the rules despite warnings?\n"
            "**6.** Are you comfortable communicating with players through written channels, such as chat or forums?\n"
            "**7.** How would you respond to a player who reports a bug or technical issue on the server?\n"
            "**8.** Can you describe your approach to maintaining a positive and welcoming community environment?\n"
            "**9.** Have you ever encountered a situation where you had to ban a player? If yes, please explain the circumstances.\n"
            "**10.** How do you handle stressful situations or conflicts between players in an impartial manner?"
        ),
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_supporter_questions_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Answer the following.**",
        description=(
            "**1.** Do you have previous experience in providing customer support or assistance?\n"
            "**2.** Can you describe a situation where you successfully resolved a technical problem for a player?\n"
            "**3.** How do you prioritize and manage multiple player inquiries or issues simultaneously?\n"
            "**4.** How would you guide a new player through the basic gameplay mechanics and features?\n"
            "**5.** Have you ever encountered a situation where a player was engaging in toxic behavior? How did you handle it?\n"
            "**6.** What steps would you take to ensure a positive and helpful interaction with players?\n"
            "**7.** How do you handle situations where you do not have an immediate solution to a player's problem?\n"
            "**8.** How would you prioritize and respond to player inquiries and support tickets?\n"
            "**9.** Are you comfortable troubleshooting technical problems related to the game client or server?\n"
            "**10.** How do you stay up-to-date with the latest updates, patches, and changes in the game?"
        ),
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed
