import hashlib
import secrets

from .models import Machine


class MachineService:
    @staticmethod
    def hash_token(token: str) -> str:
        return hashlib.sha256(str(token).encode("utf-8")).hexdigest()

    @staticmethod
    def issue_token(machine: Machine) -> str:
        token = secrets.token_urlsafe(32)
        machine.token_hash = MachineService.hash_token(token)
        machine.save(update_fields=["token_hash"])
        return token

    @staticmethod
    def revoke_token(machine: Machine) -> None:
        machine.token_hash = None
        machine.save(update_fields=["token_hash"])

    @staticmethod
    def authenticate(token: str) -> Machine | None:
        if not token:
            return None
        return Machine.objects.filter(
            token_hash=MachineService.hash_token(token)
        ).first()
