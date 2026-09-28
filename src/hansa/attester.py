"""The attester adapter (A0, 2026-09-29; `docs/CHARTER.md` §2.A): a person
or firm who checked paper, a primary source or an official online register,
and says so as a *statement* in the one shape loopmarket's counterparty
gate reads (`loopmarket.schema.Statement`, kind `attested`).

An attester owns an issuer register (`loopmarket.register.Register`, its own
separately rooted book, announced under the `register` role): issuing a
statement writes its status there, revoking or suspending it is a later
write, and a relier reads the status under the root its proposal pinned.
The statement and its presentation go to the subject, who presents them in
its own book (`OfferRegistry.present`, the `cred/` sidecar) — hansa never
writes a maker's book.

Why the attester also signs the statement id, when the register's status
already is its speech: the signature travels with the presentation, so a
statement can be checked against its issuer outside the register (a door
check offline, a relier without the register's blobs yet); the register
stays the authority on whether it still stands.

The evidence `basis` is factbond's evidence-class catalogue (charter §2.A,
corrected 2026-09-25), never a parallel scale. eth-keys loads lazily for
the signature (B1: the shape works offline without it).
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field

from loopmarket.register import Register
from loopmarket.schema import Statement

ATTESTED = "attested"


def _keys():
    try:
        from eth_keys import keys
    except ImportError as exc:  # pragma: no cover - exercised only without the extra
        raise RuntimeError("an attester's signature needs eth-keys: pip install 'loopmarket[sig]'") from exc
    return keys


def address_of(private_key_hex: str) -> str:
    """The Ethereum-style address a key speaks as: the attester's issuer id."""
    keys = _keys()
    return keys.PrivateKey(bytes.fromhex(private_key_hex.removeprefix("0x"))).public_key.to_checksum_address()


def sign_id(id_hex: str, private_key_hex: str) -> str:
    """A recoverable signature over a 32-byte content id (a statement's, a
    challenge's digest) — the same form loopmarket's detached offer
    signatures take (`loopmarket.sigs`)."""
    keys = _keys()
    return keys.PrivateKey(bytes.fromhex(private_key_hex.removeprefix("0x"))) \
        .sign_msg_hash(bytes.fromhex(id_hex)).to_hex()


def recover(id_hex: str, sig_hex: str) -> str:
    """Who signed a 32-byte id, or "" for a malformed signature."""
    try:
        keys = _keys()
        sig = keys.Signature(signature_bytes=bytes.fromhex(sig_hex.removeprefix("0x")))
        return sig.recover_public_key_from_msg_hash(bytes.fromhex(id_hex)).to_checksum_address()
    except Exception:  # noqa: BLE001 — malformed: invalid, never an error
        return ""


@dataclass
class Attester:
    """An attester: its key (the issuer id is its address), its issuer
    register, the evidence class its checks rest on, and the accreditation
    path above it to a trust root (each hop a register that accredits the
    one below; the relier names the root)."""

    key: str
    register: Register
    basis: str = "digital-proof"
    above: tuple[str, ...] = ()
    paid_by: str = "subject"
    issued: list = field(default_factory=list)

    @property
    def address(self) -> str:
        return address_of(self.key)

    def attest(self, subject: str, category: str, *, as_of: int, until: int, evidence: bytes,
               deposit: tuple[str, str] | None = None, scheme: str = "",
               issuance: str = "issued-by-attester-in-person", photo_commitment: str = "",
               paid_by: str | None = None) -> tuple[Statement, dict]:
        """Check done: the statement about `subject`, its status issued in
        this attester's register, and the presentation the subject presents
        beside it — the attester's signature, the evidence basis, and, when
        the key was bound to a face at issuance, the photo's commitment
        (never the photo: it is disclosed at the door only)."""
        s = Statement(subject=subject, category=category, issuer=self.address, kind=ATTESTED,
                      as_of=as_of, until=until, evidence=hashlib.sha256(evidence).hexdigest(),
                      path=(self.address, *self.above), paid_by=paid_by or self.paid_by,
                      deposit=deposit, scheme=scheme, issuance=issuance)
        self.register.issue(s.statement_id, as_of)
        self.issued.append(s.statement_id)
        presentation = {"issuer_sig": sign_id(s.statement_id, self.key), "basis": self.basis}
        if photo_commitment:
            presentation["photo_commitment"] = photo_commitment
        return s, presentation

    def revoke(self, statement: Statement, at: int) -> None:
        self.register.revoke(statement.statement_id, at)

    def suspend(self, statement: Statement, at: int) -> None:
        self.register.suspend(statement.statement_id, at)

    def publish(self, at: int) -> str:
        """Heartbeat and commit: the root a relier's proposal pins, with its
        publication time (the root's age is what `max_root_age` bounds)."""
        self.register.heartbeat(at)
        return self.register.commit()


def verify_presentation(statement: Statement, presentation: dict | None) -> bool:
    """Does the presentation carry the issuer's own signature over the
    statement? Fail closed: no presentation, no signature, no pass."""
    if not isinstance(presentation, dict) or not presentation.get("issuer_sig"):
        return False
    return recover(statement.statement_id, presentation["issuer_sig"]) == statement.issuer
