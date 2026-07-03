package io.arsh.embeds;

import net.dv8tion.jda.api.EmbedBuilder;

import java.awt.*;

public class RewardEmbeds {

    public static final EmbedBuilder inviteReward = new EmbedBuilder()
            .setColor(new Color(0x00FFFF))
            .setTitle("Invite・Rewards")
            .setDescription("""
                    Invite friends and unlock valuable perks:
                   \s
                    **● 2 Invites** — Access to free resources \s
                    **● 5 Invites** — Free server optimization \s
                    **● 7 Invites** — 5% Discount on orders *(Except hosting services)* \s
                    **● 10 Invites** — 10% Discount on orders *(Except hosting services)* \s
                   \s
                    **Start inviting now and track your progress with `/invites`!**
                   \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1119317556893855826/1384902539450781706/referral.png?ex=68541e7f&is=6852ccff&hm=c763fe09d307bd274294529df71e0d29ff4a9d04e9af127f605d5592c41a6359&")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

    public static final EmbedBuilder boosterReward = new EmbedBuilder()
            .setColor(new Color(0xFF70FF))
            .setTitle("Boost・Rewards")
            .setDescription("""
                    Boost the server and unlock benefits:
                   \s
                    **🔹 1x Boost Includes:**
                    ● Free server optimization (1x)\s
                    ● Access to free resources\s
                    ● Exclusive booster role\s
                    ● 5% Discount on orders *(Except hosting services)* \s
                    \s
                    **🔸 2x Boost Includes:**
                    ● Free server optimization (2x)\s
                    ● Access to free resources\s
                    ● Exclusive booster role\s
                    ● 10% Discount on orders *(Except hosting services)* \s
                   \s
                    **Boost now and get rewarded instantly!**
                   \s""")
            .setThumbnail("https://cdn.discordapp.com/emojis/1114515644969386004.webp?size=96&quality=lossless")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

}
