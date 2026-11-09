import hashlib
import secrets

from .models import Machine


class MachinesService:
    def hash_token(self, token: str) -> str:
        return hashlib.sha256(str(token).encode("utf-8")).hexdigest()

    def issue_token(self, machine: Machine) -> str:
        token = secrets.token_urlsafe(32)
        machine.token_hash = self.hash_token(token)
        machine.save(update_fields=["token_hash"])
        return token

    def revoke_token(self, machine: Machine) -> None:
        machine.token_hash = None
        machine.save(update_fields=["token_hash"])

    def authenticate(self, token: str) -> Machine | None:
        if not token:
            return None
        return Machine.objects.filter(token_hash=self.hash_token(token)).first()
