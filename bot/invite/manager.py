import os
import json
from typing import List, Dict, Optional, Any
from bot.logger import BotLogger

DATA_FILE = os.path.join("data", "invite_records.json")

class InviteRecord:
    def __init__(self, inviter_id: str, invited_user_ids: List[str]):
        self.inviter_id = str(inviter_id)
        self.invited_user_ids = [str(x) for x in invited_user_ids]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "inviterId": self.inviter_id,
            "invitedUserIds": self.invited_user_ids
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "InviteRecord":
        return cls(
            inviter_id=str(data.get("inviterId", "")),
            invited_user_ids=data.get("invitedUserIds", [])
        )

class InviteManager:
    def __init__(self, data_file: str = DATA_FILE):
        self.data_file = data_file
        self.invite_records: List[InviteRecord] = []
        self.invite_cache: Dict[str, int] = {}
        self.load_invite_records()

    def cache_invites(self, invites):
        self.invite_cache.clear()
        for invite in invites:
            self.invite_cache[invite.code] = invite.uses or 0

    def get_used_invite(self, new_invites):
        for invite in new_invites:
            old_uses = self.invite_cache.get(invite.code, 0)
            if (invite.uses or 0) > old_uses:
                return invite
        return None

    def load_invite_records(self):
        if not os.path.exists(self.data_file):
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            self.invite_records = []
            self.save_invite_records()
            return

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.invite_records = [InviteRecord.from_dict(d) for d in data]
        except Exception as ex:
            BotLogger.error(f"Failed to load invite records: {ex}", False)
            self.invite_records = []

    def save_invite_records(self):
        try:
            parent = os.path.dirname(self.data_file)
            if parent:
                os.makedirs(parent, exist_ok=True)
            temp_file = f"{self.data_file}.tmp"
            data = [r.to_dict() for r in self.invite_records]
            with open(temp_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            os.replace(temp_file, self.data_file)
        except Exception as ex:
            BotLogger.error(f"Failed to save invite records: {ex}", False)

    def add_invite(self, inviter_id: str | int, invitee_id: str | int):
        inviter_str = str(inviter_id)
        invitee_str = str(invitee_id)

        record = self.get_invite_record(inviter_str)
        if record:
            if invitee_str not in record.invited_user_ids:
                record.invited_user_ids.append(invitee_str)
        else:
            self.invite_records.append(InviteRecord(inviter_str, [invitee_str]))

        self.save_invite_records()

    def remove_invite(self, inviter_id: str | int, invitee_id: str | int):
        inviter_str = str(inviter_id)
        invitee_str = str(invitee_id)

        for record in self.invite_records:
            if record.inviter_id == inviter_str:
                if invitee_str in record.invited_user_ids:
                    record.invited_user_ids.remove(invitee_str)
                    self.save_invite_records()
                return

    def has_invite_record(self, member_id: str | int) -> bool:
        id_str = str(member_id)
        return any(r.inviter_id == id_str for r in self.invite_records)

    def get_inviter_id(self, user_id: str | int) -> Optional[str]:
        id_str = str(user_id)
        for record in self.invite_records:
            if id_str in record.invited_user_ids:
                return record.inviter_id
        return None

    def get_invites(self, member_id: str | int) -> int:
        record = self.get_invite_record(member_id)
        return len(record.invited_user_ids) if record else 0

    def get_invite_record(self, member_id: str | int) -> Optional[InviteRecord]:
        id_str = str(member_id)
        for record in self.invite_records:
            if record.inviter_id == id_str:
                return record
        return None

    def reset_invites(self, member_id: str | int):
        record = self.get_invite_record(member_id)
        if record:
            record.invited_user_ids.clear()
            self.save_invite_records()
