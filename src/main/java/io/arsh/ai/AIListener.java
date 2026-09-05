package io.arsh.ai;

import io.arsh.utils.Config;
import net.dv8tion.jda.api.entities.channel.Channel;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.util.Set;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;

public class AIListener extends ListenerAdapter {

    private final AI ai;
    private final Set<String> mutedChannelIds = ConcurrentHashMap.newKeySet();

    public AIListener(AI ai) {
        this.ai = ai;
    }

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (event.getAuthor().isBot()) return;
        String parentId = event.getChannel().asTextChannel().getParentCategoryId();
        if (parentId.equals(Config.TICKET_NORMAL)) {
            String channelId = event.getChannel().getId();
            if (event.getMessage().getContentRaw().contains("c!")) {
                if (!mutedChannelIds.contains(channelId)) {
                    mutedChannelIds.add(channelId);
                    event.getMessage().reply("> **AI muted!**").queue();
                } else {
                    mutedChannelIds.remove(channelId);
                    event.getMessage().reply("> **AI unmuted!**").queue();
                }
                return;
            }
            if (mutedChannelIds.contains(channelId)) return;

            event.getChannel().sendTyping().queue();
            String authorName = event.getAuthor().getName();
            String prompt = event.getMessage().getContentRaw();

            CompletableFuture.supplyAsync(() -> ai.getResponse(authorName, prompt))
                .thenAccept(response -> {
                    if (response != null && !response.isBlank()) {
                        event.getMessage().reply(response).queue(null, failure -> {});
                    }
                });
        }
    }
}
