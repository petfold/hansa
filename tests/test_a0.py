"""A0's gate (`docs/CHARTER.md` §3): the dentist case end to end on memory
stores. An attester checks the dentist's licence and attests it in its
own register; the dentist presents the statement in his own book's `cred/`
sidecar; the chamber, the patient's trust root, accredits the attester;
loopmarket's counterparty gate passes and the loop clears. Revoked in the
attester's register, the same statement is refused. At the door the
dentist's key answers a fresh challenge once — a replay fails — and the
photo the attester bound opens its commitment.

Needs the loopmarket checkout that carries the v6 statement and the gate
(`conftest.py` prefers the sibling checkout); skips otherwise."""

import secrets

import pytest

pytest.importorskip("loopmarket.gate", reason="needs loopmarket with the counterparty gate (R4)")
pytest.importorskip("eth_keys", reason="needs eth-keys: pip install 'loopmarket[sig]'")

from ontodag import OntoDAG  # noqa: E402
from recordstore import MemoryBytesStore, RecordStore  # noqa: E402

from loopmarket import (  # noqa: E402
    Accept, Acceptance, Bond, Credential, MockClearing, OfferRegistry, Ontology, Requires, SolverAgent, Thing,
    TimeWindow, give, want,
)
from loopmarket.register import Register  # noqa: E402

from hansa.attester import Attester, address_of, verify_presentation  # noqa: E402
from hansa.binding import DoorCheck, new_salt, photo_commitment, photo_opens, respond  # noqa: E402

NOW = 1_790_000_000
V = dict(valid=TimeWindow(NOW - 10, NOW + 30 * 86_400))
EUR = Acceptance(("stablecoin-eur",), "EUR", 1)


def _key():
    return "0x" + secrets.token_hex(32)


def _catalogue():
    cat = Ontology(OntoDAG())
    cat.load({"dentistry": [], "lesson": [], "licence": [], "dentist-licensed": ["licence"], "stablecoin-eur": []})
    return cat


class Case:
    def __init__(self):
        self.blobs = MemoryBytesStore()
        self.chamber_key, self.dentist_key = _key(), _key()
        self.chamber = Register(RecordStore(self.blobs))
        self.attester = Attester(_key(), Register(RecordStore(self.blobs)), basis="digital-proof",
                                 above=(address_of(self.chamber_key),))
        self.chamber.accredit(self.attester.address, "licence", by=address_of(self.chamber_key),
                              since=NOW - 365 * 86_400, until=NOW + 365 * 86_400, scheme="5c" * 32)
        self.chamber.heartbeat(NOW - 60)
        self.chamber.commit()
        self.dentist = address_of(self.dentist_key)
        self.patient = "0x" + "a0" * 20
        self.judge = "0x" + "77" * 20
        self.book = OfferRegistry(RecordStore(self.blobs))
        self.give = give(self.dentist, Thing(("dentistry",), 10, "visit", step=1), 300, **V, nonce=1,
                         bond=Bond(Thing(("stablecoin-eur",), 500, "EUR"), 500, "0xE"), arbitrator=self.judge)
        self.want = want(self.patient, Thing(("dentistry",), 1, "visit"), 40, **V, nonce=2,
                         requires=Requires(accepts=(EUR,), resolvers=Accept(keys=(self.judge,)),
                                           counterparty=(Credential("dentist-licensed", ("attested",), min_bond=20,
                                                                    roots=(address_of(self.chamber_key),),
                                                                    max_root_age=86_400),)))
        self.book.publish_many([self.give, self.want, give(self.patient, Thing(("lesson",), 1, "hour"), 10, **V, nonce=3),
                                want(self.dentist, Thing(("lesson",), 1, "hour"), 35, **V, nonce=4)])
        self.photo, self.salt = b"the dentist's face", new_salt()
        self.statement, self.presentation = self.attester.attest(
            self.dentist, "dentist-licensed", as_of=NOW - 1_000, until=NOW + 28 * 86_400,
            evidence=b"licence register lookup, entry 4711", deposit=(self.give.offer_id, "0xE"),
            scheme="5c" * 32, photo_commitment=photo_commitment(self.photo, self.salt))
        self.attester.publish(NOW - 60)
        self.book.present(self.statement, self.presentation)
        self.book.commit()

    @property
    def registers(self):
        return {self.attester.address: self.attester.register, address_of(self.chamber_key): self.chamber}

    def solve(self):
        clearing = MockClearing(self.book, _catalogue(), clock=lambda: NOW,
                                register_at=lambda rid, root: Register(RecordStore.at(root, self.blobs)))
        agent = SolverAgent(self.book, _catalogue(), clearing=clearing, solver_id="t", registers=self.registers)
        return agent.step(now=NOW), clearing


def test_the_attested_dentist_passes_loopmarkets_gate_and_the_loop_clears():
    case = Case()
    assert verify_presentation(case.statement, case.presentation)
    (receipt,), _ = case.solve()
    assert receipt.accepted
    rec = case.book.store.get(f"loop/{receipt.loop_id}")
    assert set(rec["register_roots"]) == set(case.registers)


def test_revoked_in_the_attesters_register_the_statement_is_refused():
    case = Case()
    case.attester.revoke(case.statement, NOW - 30)
    case.attester.publish(NOW - 30)
    receipts, clearing = case.solve()
    assert receipts == []                                   # the solver finds no admissible loop
    from loopmarket.clearing import LoopProposal
    from loopmarket.graph import Loop
    from loopmarket.matching import Match
    offers = {o.offer_id: o for o in case.book.offers()}
    lesson = next(o for o in offers.values() if o.maker == case.patient and o.kind == "give")
    wants_lesson = next(o for o in offers.values() if o.maker == case.dentist and o.kind == "want")
    loop = Loop((Match(give=case.give, want=case.want), Match(give=lesson, want=wants_lesson)))
    pins = tuple(sorted((r, reg.root) for r, reg in case.registers.items()))
    verdict = clearing.rehearse(LoopProposal(loop, case.book.store.root, "", "t", NOW, pins))
    assert not verdict.accepted and "3 revoked" in verdict.reason


def test_the_key_at_the_door_answers_once_and_the_photo_opens():
    case = Case()
    door = DoorCheck()
    c = door.challenge()
    answer = respond(c, case.statement.statement_id, case.dentist_key)
    assert door.possession(c, answer, case.statement.statement_id, case.dentist)
    assert not door.possession(c, answer, case.statement.statement_id, case.dentist)      # a replay dies
    c2 = door.challenge()
    assert not door.possession(c2, respond(c2, case.statement.statement_id, _key()), case.statement.statement_id,
                               case.dentist)                                               # another key
    assert not door.possession("00" * 32, answer, case.statement.statement_id, case.dentist)  # never issued here
    commitment = case.presentation["photo_commitment"]
    assert photo_opens(commitment, case.photo, case.salt)
    assert not photo_opens(commitment, b"someone else", case.salt)
    # a forged presentation does not verify against the issuer
    forged = dict(case.presentation, issuer_sig=respond(c2, case.statement.statement_id, _key()))
    assert not verify_presentation(case.statement, forged)
