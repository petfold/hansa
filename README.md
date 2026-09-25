# hansa

[![license](https://img.shields.io/badge/license-BSD--3--Clause-blue)](LICENSE)

Credentials, cover and identity binding for the
[loopmarket](https://github.com/petfold/loopmarket) /
[factbond](https://github.com/petfold/factbond) /
[ontodag](https://github.com/petfold/ontodag) stack: the ecosystem around a
market that the market itself should not carry.

**hansa** makes it cheap to answer, for any trade, *who pays if it goes
wrong, and did they check?* Trust in a credential, an item, a title or a
service is a solvent party's commitment to pay when it fails, by a party
with every reason to check first. Bonds are the small, self-written form;
cover the large, pooled form; and everything here exists to make that
commitment expressible, checkable and cheap to offer:

- **statements and adapters** — one statement shape loopmarket's gate reads
  (`{subject, category, issuer, kind, as_of, until, evidence, path, deposit?,
  paid_by, scheme}`; kinds *signed*, *attested*, *self-bonded*), produced
  from EU and W3C credentials, from attesters who checked paper or a
  register, and from a maker's own deposit-backed declaration;
- **registers** — transparency logs that issue, suspend, revoke and
  accredit, separately rooted and pinned per proposal; mirrors of external
  registers as content-addressed snapshots;
- **the credential vocabulary** — the layer on ontodag-core's occupations
  pack: licensing status, recognition edges, the identity door scale, the
  published `scheme` of every check;
- **identity binding** — a door scale (possession, photo, proximity) and a
  set of issuance sources (attester in person, web of trust, a state
  document via ZK, a government eID); the protocol never requires a
  government credential;
- **the insurer's product layer** — underwriting requirements, presentation,
  retention, watching and notice duty, graduated sanctions; and the rules
  of the first pooled form, a mutual on factbond's reserve.

**Status: created 2026-09-25 from `docs/CHARTER.md`; no code yet.** The
name is the Hanseatic league's: merchants admitted by their towns, vouched
for, disciplined by expulsion, trading under their own law (the drafts'
working name was *assurance*). The
first gate is A0: the dentist case end to end on memory stores — a
practice's attested statement about a dentist's key, backed by the
practice's deposit, in the maker's `cred/` sidecar; loopmarket's gate
passes it; a revoked, suspended, expired, unaccredited or silent-register
statement is refused, and the rejection record enumerates why. The
cross-repository plan this repo was created under is
`docs/plans/credentials-cover-and-options.md`; the research it rests on is
`docs/research-notes.md`; the practice record the design was checked
against is loopmarket's `docs/plans/commercial-practice-review.md`.

```
hansa  →  loopmarket (>=0.12.0)  →  ontodag  →  recordstore  →  Swarm (optional)
           →  factbond (0.1.0)
```

hansa depends on loopmarket (the statement and claim shapes, the gate,
the escrow) and on factbond (assertions, adjudication, the calibration
ledger); **neither imports hansa**. Its adapters and services are the
counterpart of loopmarket's outside solver species: they publish, loopmarket
verifies.

hansa is open source on the internet with no organisation behind it.
Compliance with any jurisdiction's law is entirely the responsibility of the
makers, issuers and insurers who use it; the protocol neither enforces nor
designs around it. What the design holds itself to is good commercial
practice: the solutions merchants, private courts and mutuals converged on
because they were more efficient, safer and produced fewer conflicts.
