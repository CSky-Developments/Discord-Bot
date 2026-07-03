package io.arsh.message;

public class MessageEntry {
    String content;
    String authorId;
    long timestamp;
    MessageEntry(String content, String authorId, long timestamp) {
        this.content = content;
        this.authorId = authorId;
        this.timestamp = timestamp;
    }
}