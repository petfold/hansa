"""Identity binding at the door (A0, 2026-09-29; `docs/CHARTER.md` §2.D,
plan D8): the device side of loopmarket's two door witnesses.

The protocol — what the key signs, that a challenge is spent on its first
response, how the photo's commitment opens — is loopmarket's
(`loopmarket.witness`, R7), because clearing and settlement read it; this
module is what the practitioner's and the counterparty's phones run:

- **possession** (`door-at-least-possession`): the counterparty's device
  draws a fresh challenge, the practitioner's key signs it with the
  statement id, and the device accepts the response once — a copied
  response dies at once;
- **photo** (`door-at-least-photo`): at issuance the attester commits to
  the photo it bound to the key (a salted hash in the presentation, never
  the photo); at the door the practitioner discloses photo and salt to the
  counterparty's device, which opens the commitment and shows the face.

Why these two first: they need nothing beyond the key and a phone, and
together they stop the copied code and the live relay without the right
face; proximity (NFC, distance bounding) is the next level.
"""

from __future__ import annotations

import secrets

from loopmarket.witness import DoorCheck as _DoorCheck
from loopmarket.witness import photo_commitment, photo_opens
from loopmarket.witness import respond as _respond

DOOR_POSSESSION = "door-at-least-possession"
DOOR_PHOTO = "door-at-least-photo"

__all__ = ["DOOR_POSSESSION", "DOOR_PHOTO", "DoorCheck", "respond", "photo_commitment", "photo_opens",
           "new_salt"]


def respond(challenge: str, statement_id: str, private_key_hex: str) -> str:
    """The practitioner's device: sign the challenge with the statement id."""
    return _respond(challenge, statement_id, private_key_hex)


class DoorCheck(_DoorCheck):
    """The counterparty's device: issues challenges and accepts each
    response at most once, bound to the statement the gate read."""

    def possession(self, challenge: str, response: str, statement_id: str, subject: str) -> bool:
        return super().possession(challenge, response, statement_id, subject)


def new_salt() -> bytes:
    return secrets.token_bytes(32)
