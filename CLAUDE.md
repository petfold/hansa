# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

`hansa` is the ecosystem around loopmarket that the market itself should not carry: **statements** about a maker's key (a credential, a licence, an independence status, a deposit-backed declaration) in the one shape loopmarket's counterparty gate reads; **adapters** that turn EU and W3C credentials, attesters' checks and makers' own declarations into statements; **registers** that issue, suspend, revoke and accredit, as transparency logs pinned per proposal; the **credential vocabulary** on ontodag-core's occupations pack; **identity binding** as a door scale plus issuance sources; and the **insurer's product layer** (underwriting requirements, presentation, retention, notice duty, sanctions) with the rules of the first pooled form, a mutual on factbond's reserve. The charter is `docs/CHARTER.md`; the cross-repository plan is `docs/plans/credentials-cover-and-options.md` (its D8, D9 and D10 and the amendments D, E, F, G are this repository's side); `docs/research-notes.md` is the record of the institutions the design learned from.

Created 2026-09-25. **No code yet**; the first gate is A0 (the charter's §3).

## The stack and its direction

```
hansa  →  loopmarket  →  ontodag  →  recordstore  →  Swarm (optional)
           →  factbond
```

- **loopmarket** defines the *shape* the gate reads (a statement, a claim, a reservation) and verifies it; hansa produces statements and cover offers. `../loopmarket/docs/plans/counterparty-gate.md` is the gate; `options-and-cover.md` and `items-and-ownership.md` there are the designs this repository's products plug into.
- **factbond** adjudicates: the `self-knowable` class, the clocks, the evidence fee, the calibration ledger with its loss view, the geared reserve and the mutual's rules (`../factbond/docs/plans/assertion-extensions.md`, `evidence-policy.md`, `netting-and-reserves.md`).
- **ontodag / ontodag-core**: the catalogue; the credential pack here sits on core and the occupations pack and adds nothing to them (`../ontodag-core/docs/ASKS.md`).

## Boundaries (to be enforced by `tests/test_boundaries.py` as code lands)

- **B1 The core works offline.** `import hansa` and every adapter's *shape* must function with no network and no optional dependency; format verification (EU seals, X.509, SD-JWT, ZK) lives behind optional extras, lazily imported.
- **B2 One-directional dependencies.** hansa imports loopmarket and factbond; never the reverse. The one dependency the other way is data, not code: factbond's evidence policy names identity-binding levels this repository's vocabulary defines.
- **B3 No identity requirement.** Government credentials are one issuance source among several; the default binding is none; collateral substitutes for identity.
- **B4 Everything a gate relies on is re-derivable** from pinned data (loopmarket U3/U4) or bonded and challengeable (factbond); an unverifiable statement meets nothing.
- **B5 Nothing positive from history.** No adapter, register or product counts fills, countersigns, rulings or inspections as a signal (loopmarket U12); acceptance is by stake, accreditation or negative record.

## Principles (charter §1.2)

Who pays, and did they check. Adopt, don't rebuild (consume EU/W3C credentials, national registers, passports; never mint a parallel diploma system). Global data, local computation (records public and uncensorable; judgements each relying party's own). Collateral substitutes for identity. Compliance with any jurisdiction's law is the makers' concern; the standard is good commercial practice (`../loopmarket/docs/plans/commercial-practice-review.md`).

## Running tests

```bash
python3 -m pytest -q
```
