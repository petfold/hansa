"""Identity binding at the door (A0's two witnesses, 2026-09-29;
`docs/CHARTER.md` §2.D, plan D8): a statement binds a *key*; the person at
the door must control it, and the counterparty must recognise them.

- **possession** (`door-at-least-possession`): the counterparty's device
  draws a fresh challenge, the practitioner's key signs it with the
  statement id, and the device checks the signature recovers to the
  statement's subject — once: a `DoorCheck` remembers the challenges it
  issued and spent, so a copied response dies at once (nothing reusable
  exists);
- **photo** (`door-at-least-photo`): at issuance the attester commits to
  the photo it bound to the key (a salted hash in the presentation, never
  the photo); at the door the practitioner discloses photo and salt to the
  counterparty's device, which opens the commitment and shows the face.

Why these two first: they need no infrastructure beyond the key and a
phone, and together they stop the copied code and the live relay without
the right face; proximity (NFC, distance bounding) is the next level. The
witness types enter loopmarket through factbond's roster and the
clearing's verifiable set (loopmarket R7); this module is the check itself.
"""

from __future__ import annotations

import hashlib
import hmac
import secrets

from .attester import recover, sign_id

DOOR_POSSESSION = "door-at-least-possession"
DOOR_PHOTO = "door-at-least-photo"


def _digest(challenge: str, statement_id: str) -> str:
    return hashlib.sha256(bytes.fromhex(challenge) + bytes.fromhex(statement_id)).hexdigest()


def respond(challenge: str, statement_id: str, private_key_hex: str) -> str:
    """The practitioner's device: sign the challenge with the statement id."""
    return sign_id(_digest(challenge, statement_id), private_key_hex)


class DoorCheck:
    """The counterparty's device: issues challenges and accepts each
    response at most once."""

    def __init__(self) -> None:
        self._open: set[str] = set()

    def challenge(self) -> str:
        c = secrets.token_hex(32)
        self._open.add(c)
        return c

    def possession(self, challenge: str, response: str, statement_id: str, subject: str) -> bool:
        """The response signs this challenge and statement by the subject's
        key, and the challenge was issued here and not spent."""
        if challenge not in self._open:
            return False                       # never issued here, or already spent: a replay
        self._open.discard(challenge)
        return recover(_digest(challenge, statement_id), response).lower() == subject.lower()


def photo_commitment(photo: bytes, salt: bytes) -> str:
    """What the attester puts in the presentation: a salted hash of the
    photo it bound to the key, so the public record says nothing of the face."""
    return hashlib.sha256(salt + photo).hexdigest()


def photo_opens(commitment: str, photo: bytes, salt: bytes) -> bool:
    """At the door: the disclosed photo and salt open the commitment."""
    return hmac.compare_digest(photo_commitment(photo, salt), commitment)


def new_salt() -> bytes:
    return secrets.token_bytes(32)
