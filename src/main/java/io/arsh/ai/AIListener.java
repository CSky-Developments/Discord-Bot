package io.arsh.ai;

import io.arsh.utils.Config;
import net.dv8tion.jda.api.entities.channel.Channel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.util.ArrayList;
import java.util.List;

public class AIListener extends ListenerAdapter {

    private final AI ai;
    private List<Channel> muteChannel = new ArrayList<>();

    public AIListener(AI ai) {
        this.ai = ai;
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (event.getAuthor().isBot()) return;
        String parentId = event.getChannel().asTextChannel().getParentCategoryId();
        if (parentId.equals(Config.TICKET_NORMAL)) {
            if (event.getMessage().getContentRaw().contains("c!")) {
                if (!muteChannel.contains(event.getChannel())) {
                    muteChannel.add(event.getChannel());
                    event.getMessage().reply("> **AI muted!**").queue();
                } else {
                    muteChannel.remove(event.getChannel());
                    event.getMessage().reply("> **AI unmuted!**").queue();
                }
                return;
            }
            if (muteChannel.contains(event.getChannel())) return;
            String response = ai.getResponse(event.getAuthor().getName(), event.getMessage().getContentRaw());
            if (response != null) {
                event.getMessage().reply(response).queue();
                event.getChannel().sendTyping().queue();
            }
        }
    }
}
