package io.arsh.embeds;

import net.dv8tion.jda.api.EmbedBuilder;
import net.dv8tion.jda.api.entities.emoji.Emoji;
import net.dv8tion.jda.api.interactions.components.ActionRow;
import net.dv8tion.jda.api.interactions.components.buttons.Button;
import net.dv8tion.jda.api.interactions.components.buttons.ButtonStyle;

import java.awt.*;

public class ServiceEmbeds {

    public static final EmbedBuilder building = new EmbedBuilder()
            .setColor(new Color(0xF35A46))
            .setTitle("Build・Building")
            .setDescription("""
                     **Accepted Versions:** `1.8.8`, `1.16`–`1.21.5`
                    
                     **Build pricing is based on (but not limited to):**
                     ● **Size** — e.g., `1000x1000`, larger scale may increase cost. \s
                     ● **Time Required** — How long the build will take. \s
                     ● **Version Compatibility** — Specific version requests may affect pricing. \s
                     ● Additional factors depending on your request.
                    
                     **Minimum Price:** `119 INR/build`
                    \s""")
            .setThumbnail("https://media.forgecdn.net/avatars/308/39/637390518902846753.png")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

    public static final EmbedBuilder serverSetup = new EmbedBuilder()
            .setColor(new Color(0x4DAEE1))
            .setTitle("Server・Setup")
            .setDescription("""
                     **Accepted Versions:** `1.8.8`, `1.16`–`1.21.5`
                    \s
                     **Setup pricing is based on (but not limited to):**
                     ● **Type of Server** — e.g. Game, Network, Modded, SMP, etc. \s
                     ● **Software** — Type of server software (e.g., Paper, Velocity, BungeeCord, Forge). \s
                     ● **Version Compatibility** — Specific version requirements may affect pricing. \s
                     ● **Features** — Number of features, custom systems, and level of personalization. \s
                     ● **Sounds & Effects** — Quantity and complexity of sound or particle effects. \s
                     ● **Time Required** — How long the setup will take to develop. \s
                     ● Other factors depending on the project scope.
                    \s
                     **Minimum Price:** `179 INR/setup`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387109204774490192/setup.png?ex=685c259d&is=685ad41d&hm=5e5738eea1e0e143f0017681faa814c8a35ba854aa9081ee6630901723f2b59f&")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

    public static final EmbedBuilder texturePack = new EmbedBuilder()
            .setColor(new Color(0x6AAFB8))
            .setTitle("Texture・Pack")
            .setDescription("""
                     **Supported Versions:** `1.8`, `1.16`–`1.21.5`
                    \s
                     **Texture Pack pricing is based on (but not limited to):**
                     ● **Resolution** — e.g., `16x`, `32x`, `64x`, `128x`, etc. \s
                     ● **Pack Type** — PvP, Custom UI, RPG, Realistic, Vanilla+, etc. \s
                     ● **Assets Required** — Number of items, blocks, GUIs, entities, and other custom elements. \s
                     ● **Style & Complexity** — Level of detail, animations, or visual effects. \s
                     ● **Version Compatibility** — Whether you want it to support multiple versions. \s
                     ● **Time Required** — How long the project will take. \s
                     ● Other specific requests or branding needs.
                    \s
                     **Minimum Price:** `119 INR/pack`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387105728023629895/14685847-logo_l.webp?ex=685c2260&is=685ad0e0&hm=8cc279d2d9b649b1801f94f1b1b0b4554fd0c3da3543c9ae4969506c9acc7374&")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

    public static final EmbedBuilder dirtPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Dirt Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `2GB RAM` \s
                     ● <:cpu:1387022883213283399> `100% CPU (1 vCore)` \s
                     ● <:disk:1387022200522932285> `10GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `69 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128485767675934/dirt.png?ex=685c3792&is=685ae612&hm=6f506de246b368e89993d03cb686f3778eab67ed7f467e9c2c271efe3d88edd5&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder woodPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Wood Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `4GB RAM` \s
                     ● <:cpu:1387022883213283399> `200% CPU (2 vCores)` \s
                     ● <:disk:1387022200522932285> `20GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `149 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128486128390315/wood.png?ex=685c3792&is=685ae612&hm=6e0e5e1b5667d33cefd1e77a41c9a1ad6bf701127d2f15752a98bf3fda6b4e02&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder coalPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Coal Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `5GB RAM` \s
                     ● <:cpu:1387022883213283399> `200% CPU (2 vCores)` \s
                     ● <:disk:1387022200522932285> `20GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `169 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128485327142912/coal.png?ex=685c3792&is=685ae612&hm=0234b78196466d96d2698684b8929ca17c9adb1830cacfb3c650451e0cf65e79&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder stonePlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Stone Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `6GB RAM` \s
                     ● <:cpu:1387022883213283399> `200% CPU (2 vCores)` \s
                     ● <:disk:1387022200522932285> `30GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `199 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128486463930564/stone.png?ex=685c3792&is=685ae612&hm=104da46e0ec0e84cb00e3c01540ce6642231ca8075c5f1c985827d0dc3bed9bf&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder ironPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Iron Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `8GB RAM` \s
                     ● <:cpu:1387022883213283399> `300% CPU (3 vCores)` \s
                     ● <:disk:1387022200522932285> `40GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `299 / month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128484991860747/iron.png?ex=685c3792&is=685ae612&hm=2a819b76b031edf3d4a07bf46f98a59e08feba9d77a1846d338ad87d92a3e6f2&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder goldPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Gold Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `10GB RAM` \s
                     ● <:cpu:1387022883213283399> `300% CPU (3 vCores)` \s
                     ● <:disk:1387022200522932285> `40GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `349 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128487642402918/gold.png?ex=685c3793&is=685ae613&hm=87b48ef2f624722168dcdb8dddf1e291ac208fde2be3c3976f24a00fb75d0dfe&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder diamondPlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Diamond Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `12GB RAM` \s
                     ● <:cpu:1387022883213283399> `300% CPU (3 vCores)` \s
                     ● <:disk:1387022200522932285> `50GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `399 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128487243939850/diamond.png?ex=685c3792&is=685ae612&hm=a7327b35dbdfc035871ba241df9829f8f565c7f476e4a80bdff05e443a88f14d&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder netheritePlan = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Netherite Plan")
            .setDescription("""
                     **Specifications:** \s
                     ● <:ram:1387022203039645816> `16GB RAM` \s
                     ● <:cpu:1387022883213283399> `400% CPU (4 vCores)` \s
                     ● <:disk:1387022200522932285> `50GB DISK`
                    \s
                     **Billing:** Monthly (long-term options available) \s
                     **Price:** `499 INR/month`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1111724820086915158/1387128486854004736/Netherite.png?ex=685c3792&is=685ae612&hm=b1bd41d612a0372762ad5fca61fa2780c8d2a24bea267e103a7ddd8caed04a08&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");

    public static final EmbedBuilder locationsAndPayments = new EmbedBuilder()
            .setColor(new Color(0x068DE9))
            .setTitle("Locations & Payment Methods")
            .setDescription("""
                     **🌎 Server Locations:** \s
                     ● `India` :flag_in: \s
                     ● `Germany` :flag_de: \s
                    \s
                     **💳 Accepted Payment Methods:** \s
                     ● `UPI` <:upi:1384893594065834127> \s
                     ● `PayPal` <:paypal:1384893599837061130> *(Extra Charges Apply)* \s
                     ● `Crypto (Litecoin)` <:ltc:1384893606829101189> *(10% Extra Fee)*
                    \s
                     To place an order, simply click on the **Place Order** button below. \s
                     It will send you link to ArialNode's discord where you can create ticket to order your server." \s
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&")
            .setFooter("・ArialNodes", "https://cdn.discordapp.com/attachments/1119317556893855826/1384873606021910649/ArialNodes.jpeg?ex=6854038d&is=6852b20d&hm=345f2e4d59144d461cd1c544253c724507849b7e6fe5410a2b96112e4710682b&");
    private static final Button serverOrderCreateButton = Button.of(ButtonStyle.SUCCESS, "Server_Order_Create_Button", "Place Order",
            Emoji.fromCustom("Order", 1118978541871181915L, false));
    public static final ActionRow serverOrderCreateRow = ActionRow.of(serverOrderCreateButton);

    public static EmbedBuilder serverOptimization = new EmbedBuilder()
            .setColor(new Color(0xE5B432))
            .setTitle("Server・Optimization")
            .setDescription("""
                     **Supported Versions:** `1.8.8`, `1.16`–`1.21.5`
                    \s
                     **Optimization pricing is based on (but not limited to):**
                     ● **Server Type** — SMP, PvP, Modded, Network, etc. \s
                     ● **Software** — Paper, Purpur, Velocity, BungeeCord, Fabric, Forge, etc. \s
                     ● **Performance Goals** — TPS stability, lower RAM usage, improved CPU efficiency. \s
                     ● **Plugin/Mod Count** — Number of plugins or mods that need profiling/tuning. \s
                     ● **World Size & Player Capacity** — Impacts memory, chunk handling, and GC behavior. \s
                     ● **Time Required** — How long optimization will take (profiling, testing, tuning). \s
                     ● Other factors like hosting limitations, version-specific fixes, and custom requests.
                    \s
                     **Minimum Price:** `99 INR/setup`
                    \s""")
            .setThumbnail("https://cdn.discordapp.com/attachments/1119317556893855826/1384898863264960603/optimization.png?ex=68541b13&is=6852c993&hm=651f2b15ee15398bbdd52a063bd7cb793e65d87bfea2ae79d931aeb0131d12d0&")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

//    public static EmbedBuilder modDev = new EmbedBuilder()
//            .setColor(new Color(0x7C9AFF))
//            .setTitle("Mod・Development")
//            .setDescription("""
//                    **Supported Versions:** `1.12.2`, `1.16.5`, `1.18.2`, `1.20.1`, `1.20.4`, `1.21+`
//                   \s
//                    **Mod pricing is based on (but not limited to):**
//                    ● **Mod Loader** — Forge, Fabric, NeoForge (some features may vary). \s
//                    ● **Type of Mod** — Client-side, server-side, hybrid, UI-only, gameplay, etc. \s
//                    ● **Complexity** — Amount of logic, mechanics, and systems involved. \s
//                    ● **Assets & Visuals** — Models, textures, GUIs, sound effects, animations, etc. \s
//                    ● **External Systems** — Database handling, config systems, cross-mod compatibility. \s
//                    ● **Version Targeting** — One version or multi-version support (may affect time/cost). \s
//                    ● **Time Required** — Total time to plan, develop, test, and deliver. \s
//                    ● Other custom requests or scalability considerations.
//                   \s
//                    **Minimum Price:** `6 USD / mod`
//                   \s""")
//            .setThumbnail("https://cdn-icons-png.flaticon.com/512/4310/4310650.png")
//            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");
//

    public static EmbedBuilder pluginDevelopment = new EmbedBuilder()
            .setColor(new Color(0x938FF1))
            .setTitle("Plugin・Development")
            .setDescription("""
                    **Supported Versions:** `1.8.8`, `1.16`–`1.21.5`
                    
                    **Plugin pricing is based on (but not limited to):**
                    ● **Type of Plugin** — Simple utilities, minigames, core systems, APIs, etc.  
                    ● **Complexity** — Amount of logic, conditions, and feature depth.  
                    ● **Commands & GUIs** — Number of commands, menus, and custom interfaces.  
                    ● **Performance Requirements** — Asynchronous handling, optimization goals, etc.  
                    ● **External Integrations** — MySQL, MongoDB, APIs, Discord bots, Bungee support, etc.  
                    ● **Time Required** — How long the project will take to plan, code, and test.  
                    ● Other custom requests or scalability considerations.
                    
                    **Minimum Price:** `179 INR/plugin`
                    """)
            .setThumbnail("https://cdn.discordapp.com/attachments/1119317556893855826/1384899272666910833/plug-in.png?ex=68541b74&is=6852c9f4&hm=d3c64877d9b7da3d6aca443501118afdc6632fd6d92a92eb475cd97cbf6e8d45&")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");


    public static final EmbedBuilder serviceOrder = new EmbedBuilder()
            .setColor(new Color(0x4482FF))
            .setTitle("**Order Service**")
            .setDescription("To place an order, simply click on the **Place Order** button below.\nOur team will review your request and get back to you as soon as possible.")
            .setFooter("・CSky Developments", "https://cdn.discordapp.com/attachments/1112390125276631080/1112442565766168808/CSkyDevelopements.png");

}
