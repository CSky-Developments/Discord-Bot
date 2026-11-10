import discord
from bot.embeds.help_embeds import FOOTER_TEXT, FOOTER_ICON

def make_ticket_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Ticket**",
        description="To create a ticket, simply click on the **Create** button below.\nOur team will get back to you as soon as possible.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Thank you for creating a ticket.**",
        description="**Please wait for our staff to arrive.** They will be with you shortly. In the meantime, please provide any additional information or details in the ticket. If you no longer need assistance and wish to close the ticket, you can click on the **Close** button below.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to close this ticket?**\nPlease click on **Confirm** to proceed with closing the ticket, or click on **Cancel** to retract your request.",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_ticket_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**The closure of the ticket has been canceled!**",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Order Service**",
        description="To place an order, simply click on the **Place Order** button below.\nOur team will review your request and get back to you as soon as possible.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Thank you for placing an order.**",
        description="**Please wait for our staff to review your request.** They will get back to you shortly with further details. If you need to provide any additional information or have any questions, please mention it here. To cancel your order, simply click on the **Cancel** button below.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to cancel this order?**\n Please click on **Confirm** to proceed with canceling the order, or click on **Cancel** to retain your request.",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_order_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Order cancellation has been canceled!**",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_plugin_gen_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Plugin・Generation**",
        description=(
            "**Supported Versions:** `1.16.*` to `1.21.*`\n"
            "**How to Generate Your Plugin:**\n\n"
            "**Step 1: Get Your Gemini API Key**\n"
            "> • Visit [Google AI Studio](https://aistudio.google.com/app/apikey)\n"
            "> • Sign in with your Google account\n"
            "> • Click \"Create API Key\" and copy it\n\n"
            "**Step 2: Click Generate Below**\n"
            "> • Fill in your API key, plugin name, version, and description\n"
            "> • Be specific about what you want the plugin to do\n\n"
            "**Step 3: Wait for Generation**\n"
            "> • The AI will generate your custom plugin code\n"
            "> • Compilation happens automatically\n\n"
            "**Step 4: Download Your Plugin**\n"
            "> • Receive the compiled .jar file\n"
            "> • Get a README with usage instructions\n"
            "> • Ready to use on your server!\n\n"
            "**Average Generation Time:** `5-10 minutes\n`"
            "**Subscription Cost:** `90 INR/month` (only)"
        ),
        color=0xE74C3C,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_plugin_gen_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to cancel this plugin generation?**\nClick **Confirm** to proceed with cancellation, or click **Cancel** to continue.",
        color=0xE74C3C,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_plugin_gen_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Plugin generation cancellation has been aborted.**",
        color=0xE74C3C,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_reward_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Reward Claim**",
        description="To claim a reward, simply click on the **Claim** button below.\nOur team will process your request and provide you with the reward as soon as possible.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url="https://example.com/reward-system.png")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_reward_create_embed() -> discord.Embed:
    embed = discord.Embed(
        title="**Thank you for creating a reward claim ticket.**",
        description="**Please wait for our team to process your request.** They will be with you shortly. In the meantime, please provide any additional information or details in the ticket. If you change your mind and no longer wish to claim the reward, you can click on the **Cancel** button below.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url="https://example.com/reward-system.png")
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_reward_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to close this reward claim ticket?**\nPlease click on **Confirm** to proceed with closing the ticket, or click on **Cancel** to keep the ticket open.",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_reward_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**The closure of the reward claim ticket has been canceled!**",
        color=0x4482FF,
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
        title="**Thank you for considering a position at CSky Developments.**",
        description="**Please wait for the owner to arrive.** They will be with you shortly. In the meantime, we kindly request you to answer the following questions and provide any additional information or details. If you no longer wish to proceed with the application and would like to cancel it, you can simply click on the **Close** button below.",
        color=0x4482FF,
    )
    embed.set_thumbnail(url=FOOTER_ICON)
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_close_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**Are you sure you want to cancel this application?** Please click on **Confirm** to proceed with cancellation or click on **Cancel** to retract your request.",
        color=0x4482FF,
    )
    embed.set_footer(text=FOOTER_TEXT, icon_url=FOOTER_ICON)
    return embed

def make_staff_app_close_cancel_embed() -> discord.Embed:
    embed = discord.Embed(
        description="**The closure of the application has been canceled!**",
        color=0x4482FF,
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
