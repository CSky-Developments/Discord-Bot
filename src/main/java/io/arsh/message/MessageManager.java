package io.arsh.message;

import io.arsh.utils.Config;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Message;
import net.dv8tion.jda.api.entities.channel.concrete.TextChannel;
import net.dv8tion.jda.api.events.message.MessageDeleteEvent;
import net.dv8tion.jda.api.events.message.MessageReceivedEvent;
import net.dv8tion.jda.api.events.message.MessageUpdateEvent;
import net.dv8tion.jda.api.hooks.ListenerAdapter;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ConcurrentLinkedQueue;

public class MessageManager extends ListenerAdapter {

    private final Map<String, MessageEntry> messageCache = new ConcurrentHashMap<>();
    private final ConcurrentLinkedQueue<String> messageOrder = new ConcurrentLinkedQueue<>();
    private static final int CACHE_LIMIT = 10000;

    @Override
    public void onMessageReceived(MessageReceivedEvent event) {
        if (event.getAuthor().isBot() || event.getChannel().getId().equals(Config.LOG_CHANNEL_ID)) return;
        String messageId = event.getMessageId();
        String content = event.getMessage().getContentRaw();
        if (content.isEmpty()) return;
        String authorId = event.getAuthor().getId();
        messageCache.put(messageId, new MessageEntry(content, authorId, System.currentTimeMillis()));
        messageOrder.add(messageId);
        while (messageOrder.size() > CACHE_LIMIT) {
            String oldestMessageId = messageOrder.poll();
            if (oldestMessageId != null) {
                messageCache.remove(oldestMessageId);
            }
        }
    }

    @Override
    public void onMessageDelete(MessageDeleteEvent event) {
        TextChannel textChannel = event.getChannel().asTextChannel();
        MessageEntry cachedEntry = messageCache.get(event.getMessageId());
        if (cachedEntry != null) {
            String content = cachedEntry.content;
            String authorName = event.getGuild().getMemberById(cachedEntry.authorId).getUser().getName();
            String logMessage = String.format("Messages of `%s` was deleted in `%s`: ```Content: %s```",
                    authorName,
                    textChannel.getName(),
                    content);
            messageCache.remove(event.getMessageId());
            messageOrder.remove(event.getMessageId());
            Logger.info(logMessage, true);
        }
    }

    @Override
    public void onMessageUpdate(MessageUpdateEvent event) {
        TextChannel textChannel = event.getChannel().asTextChannel();
        Message updatedMessage = event.getMessage();
        if (updatedMessage.getContentRaw().isEmpty()) return;
        String newContent = updatedMessage.getContentRaw();
        MessageEntry cachedEntry = messageCache.get(event.getMessageId());
        if (cachedEntry != null && !cachedEntry.content.isEmpty()) {
            String oldContent = cachedEntry.content;
            String authorMention = event.getAuthor().getName();
            String logMessage = String.format("`%s` edited their message in `%s`: ```Original: %s``` ```Edited: %s```",
                    authorMention,
                    textChannel.getName(),
                    oldContent,
                    newContent);
            messageCache.put(event.getMessageId(), new MessageEntry(newContent, cachedEntry.authorId, System.currentTimeMillis()));
            Logger.info(logMessage, true);
        }
    }

}
