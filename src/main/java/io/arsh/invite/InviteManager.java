package io.arsh.invite;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.arsh.utils.Logger;
import net.dv8tion.jda.api.entities.Guild;
import net.dv8tion.jda.api.entities.Invite;
import net.dv8tion.jda.api.entities.Member;

import java.io.File;
import java.io.IOException;
import java.util.*;

public class InviteManager {

    private final Guild guild;
    private List<InviteRecord> inviteRecords;
    private final ObjectMapper mapper;
    private final File recordFile;

    private final Map<String, Integer> inviteCache = new HashMap<>();

    public InviteManager(Guild guild) {
        Logger.info("Initializing invite tracker...", false);
        this.guild = guild;
        this.inviteRecords = new ArrayList<>();
        this.mapper = new ObjectMapper();
        this.recordFile = new File("./data/invite_records.json");
        Logger.info("Loading invite records...", false);
        loadInviteRecords();
        Logger.info("Successfully loaded invite records!", false);
        Logger.info("Successfully initialized invite tracker!", false);
    }

    public void cacheInvites(List<Invite> invites) {
        inviteCache.clear();
        for (Invite invite : invites) {
            inviteCache.put(invite.getCode(), invite.getUses());
        }
    }

    public Invite getUsedInvite(List<Invite> newInvites) {
        for (Invite invite : newInvites) {
            int oldUses = inviteCache.getOrDefault(invite.getCode(), 0);
            if (invite.getUses() > oldUses) {
                return invite;
            }
        }
        return null;
    }

    public void loadInviteRecords() {
        try {
            if (!recordFile.exists()) {
                recordFile.getParentFile().mkdirs();
                recordFile.createNewFile();
                mapper.writeValue(recordFile, new ArrayList<InviteRecord>());
            }
            this.inviteRecords = mapper.readValue(recordFile, new TypeReference<>() {});
        } catch (IOException ex) {
            Logger.error(ex.getMessage(), false);
            this.inviteRecords = new ArrayList<>();
        }
    }

    public void saveInviteRecords() {
        try {
            mapper.writeValue(recordFile, inviteRecords);
        } catch (IOException ex) {
            Logger.error(ex.getMessage(), false);
        }
    }

    public void addInvite(Member inviter, Member invitee) {
        if (hasInviteRecord(inviter)) {
            List<String> invited = getInviteRecord(inviter).invitedUserIds();
            if (!invited.contains(invitee.getId())) {
                invited.add(invitee.getId());
            }
        } else {
            inviteRecords.add(new InviteRecord(inviter.getId(), new ArrayList<>(List.of(invitee.getId()))));
        }
        saveInviteRecords();
    }

    public void removeInvite(String inviterId, String inviteeId) {
        for (InviteRecord record : inviteRecords) {
            if (record.inviterId().equals(inviterId)) {
                record.invitedUserIds().remove(inviteeId);
                saveInviteRecords();
                return;
            }
        }
    }

    public boolean hasInviteRecord(Member member) {
        String id = member.getId();
        for (InviteRecord record : inviteRecords) {
            if (record.inviterId().equals(id)) {
                return true;
            }
        }
        return false;
    }

    public Member getInviter(String userId) {
        for (InviteRecord record : inviteRecords) {
            if (record.invitedUserIds().contains(userId)) {
                return guild.getMemberById(record.inviterId());
            }
        }
        return null;
    }

    public int getInvites(Member member) {
        String id = member.getId();
        for (InviteRecord record : inviteRecords) {
            if (record.inviterId().equals(id)) {
                return record.invitedUserIds().size();
            }
        }
        return 0;
    }

    public InviteRecord getInviteRecord(Member member) {
        String id = member.getId();
        for (InviteRecord record : inviteRecords) {
            if (record.inviterId().equals(id)) {
                return record;
            }
        }
        return null;
    }

    public void resetInvites(Member member) {
        InviteRecord record = getInviteRecord(member);
        if (record != null) {
            record.invitedUserIds().clear();
            saveInviteRecords();
        }
    }

}
