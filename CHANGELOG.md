# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/), and this project adheres to
[Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- **A0: the attester adapter and the door's first two witnesses**
  (2026-09-29; charter §3). `hansa.attester.Attester` checks, then
  attests: a statement in loopmarket's one shape (kind `attested`, its
  evidence a digest, its path the attester and the accreditors above it,
  `paid_by`, the deposit backing it, the `scheme`, the issuance source),
  its status issued in the attester's own register (`loopmarket.register`),
  and a presentation carrying the attester's signature over the statement
  id, the evidence basis (factbond's evidence class) and the photo's
  commitment; `revoke`, `suspend`, `publish` (heartbeat and root);
  `verify_presentation`. `hansa.binding`: possession — a fresh challenge
  signed with the statement id by the subject's key, accepted once by the
  counterparty's `DoorCheck` (a replay, another key or a challenge it never
  issued fails) — and photo — a salted commitment opened at the door. The
  gate, `tests/test_a0.py`: the dentist case end to end on memory stores —
  the attester's statement presented in the dentist's `cred/` sidecar, the
  chamber accrediting the attester, loopmarket's counterparty gate passing
  and the loop clearing; revoked in the attester's register, refused with
  the step named. Needs loopmarket's counterparty gate (its main branch,
  2026-09-29; the tests skip without it); `conftest.py` prefers the sibling
  checkouts.

- **The repository** (2026-09-25), created from the charter agreed with the
  assurance drafts: `docs/CHARTER.md` (components A–E and E′, the first
  gates A0–A5, the two identity-binding scales, the product layer's duties,
  the disclaimer), `docs/plans/credentials-cover-and-options.md` (the
  cross-repository plan shared with loopmarket and factbond),
  `docs/research-notes.md` (TÜV, recognition of qualifications, digital
  credentials, title insurance), `CLAUDE.md` (boundaries B1–B5), a package
  skeleton and a boundary test. No code.
