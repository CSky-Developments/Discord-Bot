package io.arsh.invite;
import java.util.List;

public record InviteRecord(String inviterId, List<String> invitedUserIds) {}

