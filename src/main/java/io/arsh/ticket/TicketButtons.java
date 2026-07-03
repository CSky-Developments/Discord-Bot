package io.arsh.ticket;

import net.dv8tion.jda.api.entities.emoji.Emoji;
import net.dv8tion.jda.api.interactions.components.ActionRow;
import net.dv8tion.jda.api.interactions.components.buttons.Button;
import net.dv8tion.jda.api.interactions.components.buttons.ButtonStyle;

public class TicketButtons {

        public static final Button ticketCreateButton = Button.of(ButtonStyle.SUCCESS, "Ticket_Create_Button", "Create",
                        Emoji.fromCustom("Ticket", 1118483344397705237L, false));
        public static final Button ticketCloseButton = Button.of(ButtonStyle.DANGER, "Ticket_Close_Button", "Close",
                        Emoji.fromCustom("TicketClose", 1118940954771075174L, false));
        public static final Button ticketCloseConfirmButton = Button.of(ButtonStyle.SUCCESS, "Ticket_Close_Confirm_Button", "Confirm",
                        Emoji.fromCustom("CloseConfirm", 1118942133517295757L, false));
        public static final Button ticketCloseCancelButton = Button.of(ButtonStyle.DANGER, "Ticket_Close_Cancel_Button", "Cancel",
                        Emoji.fromCustom("CloseCancel", 1118844964273659924L, false));
        public static final Button ticketDeleteButton = Button.of(ButtonStyle.DANGER, "Ticket_Delete_Button", "Delete",
                        Emoji.fromCustom("Delete", 1118844967327113316L, false));

        public static final ActionRow ticketCreateRow = ActionRow.of(ticketCreateButton);
        public static final ActionRow ticketCloseRow = ActionRow.of(ticketCloseButton);
        public static final ActionRow ticketCloseConfirmRow = ActionRow.of(ticketCloseConfirmButton, ticketCloseCancelButton);
        public static final ActionRow ticketDeleteRow = ActionRow.of(ticketDeleteButton);

        public static final Button orderCreateButton = Button.of(ButtonStyle.SUCCESS, "Order_Create_Button", "Place Order",
                        Emoji.fromCustom("Order", 1118978541871181915L, false));
        public static final Button orderCloseButton = Button.of(ButtonStyle.DANGER, "Order_Cancel_Button", "Cancel",
                        Emoji.fromCustom("OrderClose", 1118978536557006948L, false));
        public static final Button orderCloseConfirmButton = Button.of(ButtonStyle.SUCCESS, "Order_Cancel_Confirm_Button", "Confirm",
                        Emoji.fromCustom("CloseConfirm", 1118942133517295757L, false));
        public static final Button orderCloseCancelButton = Button.of(ButtonStyle.DANGER, "Order_Cancel_Cancel_Button", "Cancel",
                        Emoji.fromCustom("CloseCancel", 1118844964273659924L, false));
        public static final Button orderDeleteButton = Button.of(ButtonStyle.DANGER, "Order_Delete_Button", "Delete",
                        Emoji.fromCustom("Delete", 1118844967327113316L, false));

        public static final ActionRow orderCreateRow = ActionRow.of(orderCreateButton);
        public static final ActionRow orderCloseRow = ActionRow.of(orderCloseButton);
        public static final ActionRow orderCloseConfirmRow = ActionRow.of(orderCloseConfirmButton, orderCloseCancelButton);
        public static final ActionRow orderDeleteRow = ActionRow.of(orderDeleteButton);
        public static final Button pluginGenerateButton = Button.of(ButtonStyle.SUCCESS, "Plugin_Generate_Button", "Generate",
                        Emoji.fromCustom("Developer", 1117845118154711112L, false));
        public static final Button pluginCancelButton = Button.of(ButtonStyle.DANGER, "Plugin_Cancel_Button", "Cancel",
                        Emoji.fromCustom("Developer_Cancel", 1123522806815129680L, false));
        public static final Button pluginCancelConfirmButton = Button.of(ButtonStyle.SUCCESS, "Plugin_Cancel_Confirm_Button", "Confirm",
                        Emoji.fromCustom("CloseConfirm", 1118942133517295757L, false));
        public static final Button pluginCancelAbortButton = Button.of(ButtonStyle.DANGER, "Plugin_Cancel_Abort_Button", "Abort",
                        Emoji.fromCustom("CloseCancel", 1118844964273659924L, false));
        public static final Button pluginDeleteButton = Button.of(ButtonStyle.DANGER, "Plugin_Delete_Button", "Delete",
                        Emoji.fromCustom("Delete", 1118844967327113316L, false));

        public static final ActionRow pluginGenerateRow = ActionRow.of(pluginGenerateButton);
        public static final ActionRow pluginCancelRow = ActionRow.of(pluginCancelButton);
        public static final ActionRow pluginCancelConfirmRow = ActionRow.of(pluginCancelConfirmButton, pluginCancelAbortButton);
        public static final ActionRow pluginDeleteRow = ActionRow.of(pluginDeleteButton);

        public static final Button rewardClaimButton = Button.of(ButtonStyle.SUCCESS, "Reward_Claim_Button", "Claim",
                        Emoji.fromCustom("Gift", 1118971206515818568L, false));
        public static final Button rewardCloseButton = Button.of(ButtonStyle.DANGER, "Reward_Close_Button", "Close",
                        Emoji.fromCustom("GiftClose", 1118971201818202213L, false));
        public static final Button rewardCloseConfirmButton = Button.of(ButtonStyle.SUCCESS, "Reward_Close_Confirm_Button", "Confirm",
                        Emoji.fromCustom("CloseConfirm", 1118942133517295757L, false));
        public static final Button rewardCloseCancelButton = Button.of(ButtonStyle.DANGER, "Reward_Close_Cancel_Button", "Cancel",
                        Emoji.fromCustom("CloseCancel", 1118844964273659924L, false));
        public static final Button rewardDeleteButton = Button.of(ButtonStyle.DANGER, "Reward_Delete_Button", "Delete",
                        Emoji.fromCustom("Delete", 1118844967327113316L, false));

        public static final ActionRow rewardClaimRow = ActionRow.of(rewardClaimButton);
        public static final ActionRow rewardCloseRow = ActionRow.of(rewardCloseButton);
        public static final ActionRow rewardCloseConfirmRow = ActionRow.of(rewardCloseConfirmButton, rewardCloseCancelButton);
        public static final ActionRow rewardDeleteRow = ActionRow.of(rewardDeleteButton);

        public static final Button developerButton = Button.of(ButtonStyle.DANGER, "Developer_Button", "Developer",
                        Emoji.fromCustom("Developer", 1117845118154711112L, false));
        public static final Button moderatorButton = Button.of(ButtonStyle.SUCCESS, "Moderator_Button", "Moderator",
                        Emoji.fromCustom("Moderator", 1117846138935066738L, false));
        public static final Button supporterButton = Button.of(ButtonStyle.PRIMARY, "Supporter_Button", "Supporter",
                        Emoji.fromCustom("Supporter", 1117847120565776444L, false));
        public static final Button developerCloseButton = Button.of(ButtonStyle.DANGER, "Developer_Close_Button", "Close",
                        Emoji.fromCustom("Developer_Cancel", 1123522806815129680L, false));
        public static final Button moderatorCloseButton = Button.of(ButtonStyle.DANGER, "Moderator_Close_Button", "Close",
                        Emoji.fromCustom("Moderator_Cancel", 1123522816780800001L, false));
        public static final Button supporterCloseButton = Button.of(ButtonStyle.DANGER, "Supporter_Close_Button", "Close",
                        Emoji.fromCustom("Supporter_Cancel", 1123522822313087046L, false));
        public static final Button appCloseConfirmButton = Button.of(ButtonStyle.SUCCESS, "App_Close_Confirm_Button", "Confirm",
                        Emoji.fromCustom("CloseConfirm", 1118942133517295757L, false));
        public static final Button appCloseCancelButton = Button.of(ButtonStyle.DANGER, "App_Close_Cancel_Button", "Cancel",
                        Emoji.fromCustom("CloseCancel", 1118844964273659924L, false));
        public static final Button appDeleteButton = Button.of(ButtonStyle.DANGER, "App_Delete_Button", "Delete",
                        Emoji.fromCustom("Delete", 1118844967327113316L, false));

        public static final ActionRow appCreateRow = ActionRow.of(developerButton, moderatorButton, supporterButton);
        public static final ActionRow developerCloseRow = ActionRow.of(developerCloseButton);
        public static final ActionRow moderatorCloseRow = ActionRow.of(moderatorCloseButton);
        public static final ActionRow supporterCloseRow = ActionRow.of(supporterCloseButton);
        public static final ActionRow appCloseConfirmRow = ActionRow.of(appCloseConfirmButton, appCloseCancelButton);
        public static final ActionRow appDeleteRow = ActionRow.of(appDeleteButton);

}
