# hansa — charter and plan

Status: the charter this repository was created from, 2026-09-25 (drafted
2026-09-23, corrected and decided 2026-09-25). Named **hansa** on 2026-09-25 (the
drafts' working name was *assurance*; `assurance`, `surety` and most short
English words were taken on PyPI): the Hanseatic league, where merchants
were admitted by their towns, vouched for, disciplined by expulsion and
traded under their own law. The
three-repo split and this charter were authored in the drafts, not in the
chat record (which pointed at factbond as the design home of pooled cover);
plan D9 slims the charter accordingly: components A–E stay, F and A7 move.

## 1. Charter

**hansa** makes it cheap to answer, for any trade, *"who pays if it goes
wrong, and did they check?"* It provides the ecosystem around a market that
the market itself should not carry:

- **credentials and certification** — statements that a key holds a
  qualification, a licence, an independence status, cover; adapters that turn
  existing documents and credentials into them; registers that issue, revoke
  and accredit;
- **identity binding** — tying a key to the person at the door, strictly
  optional, government ID never required;
- **the insurer toolkit** — what specialist, chain-based insurers need to
  underwrite, price, sell and pay cover: title insurance, professional
  indemnity, product and inspection cover;
- **the personalised trust score** — manipulation-resistant reputation
  computed locally over public data.

### 1.1 Boundaries

- **Depends on** loopmarket (the statement and claim shapes, the gate, the
  escrow) and factbond (assertions, adjudication, the loss ledger). **Neither
  imports hansa.** Its adapters and services are the counterpart of
  loopmarket's outside solver species: they publish, loopmarket verifies.
- **Not a protocol for identity.** Government credentials are one adapter
  among several; the default binding is none.
- **Regulation and taxes are the makers' concern** — insurers and issuers
  comply where they operate; nothing here enforces or designs around it.
  *(added 2026-09-25, Peter)* The protocol is open source on the internet
  with no organisation behind it; compliance with any jurisdiction's law is
  entirely the responsibility of the makers who use it. This is to be
  stated as a disclaimer in loopmarket's README and here. What the design
  *does* hold itself to is good commercial practice: the solutions merchants,
  private courts and mutuals converged on because they were more efficient,
  safer and produced fewer conflicts (plan D10; `../../loopmarket/docs/plans/commercial-practice-review.md`).
- **Not factbond's mechanism.** *(corrected 2026-09-25)* factbond rejects
  identity as a *requirement* and caps per-fact notionals for solvency
  (`../../factbond/docs/plans/insurance-products.md` §4–§5, `../../factbond/docs/plans/netting-and-reserves.md` §5); its
  "micro-scale" is the consequence of unprovable reliance (invariant F3),
  and reliance in a cleared loop is provable. The solvency rule, the geared
  payout reserve and the calibration ledger stay in factbond. What is here
  is the product layer: underwriting requirements, identity binding levels,
  retention, watching and notice duty, exclusion.

### 1.2 Principles

1. Who pays, and did they check (the central principle).
2. Adopt, don't rebuild: consume EU/W3C credentials, national registers,
   passports; never mint a parallel diploma system.
3. Global data, local computation: records are public and uncensorable;
   judgements (scores, trust roots) are each relying party's own.
4. Everything a gate relies on is re-derivable from pinned data (loopmarket
   U3/U4) or bonded and challengeable (factbond).
5. Collateral substitutes for identity: the more at stake, the less anyone
   needs to know who you are.

## 2. Components

### A. Statements and adapters

The loopmarket gate reads one shape (`../../loopmarket/docs/plans/counterparty-gate.md` §2):
`{subject K, category C, issuer I, kind, as_of, until, evidence, path}`,
`kind ∈ signed | attested | self-bonded | insured`. hansa produces them:

| adapter | source | kind |
|---|---|---|
| **eu** | EUDI Wallet (SD-JWT VC, ISO mdoc), EDC (sealed, ELM data model), EBSI VCs with the Trusted Issuers Registry chain | signed |
| **w3c** | W3C VCs, Open Badges elsewhere | signed |
| **attester** | a person or firm who checked paper, a primary source, or an official online register (licence lookups); records the evidence basis. *(corrected 2026-09-25)* The basis is **factbond's evidence-class catalogue** (`../../factbond/docs/plans/evidence-policy.md` §1–§3: countersign, locker, digital-proof, attested-photo, location, with weights per rung), not a parallel scale; where an order is needed it is named cumulatively (`verified-at-least-register-lookup`), see ontodag-core's `../../ontodag-core/docs/ASKS.md` and ontodag's `ROADMAP.md` §2 | attested |
| **self** | a factbond self-assertion (factbond's `../../factbond/docs/plans/assertion-extensions.md` §4) | self-bonded |
| **cover** | an insurer's cover give or reservation | insured |

Each adapter emits the statement plus the original presentation for the
maker's `cred/` sidecar; loopmarket clearing re-verifies the presentation
where it can, and the attester wraps it (kind *attested*, bonded) where
verification is too heavy. The wallet key is bound to the maker key by a
presentation whose challenge contains K. *(applied plan G5)* Every
statement records who paid the attester, the subject or the relier: the
disclosure issuer-pays ratings fell back on, and the input for the
relying party's own judgement of "did they check".

### B. Registers

Services that run loopmarket-shaped registers (`status/`, `revoked/`,
`accredit/`), heartbeat at a declared cadence, and announce under the
`register` role:

- **issuer registers** for attesters and bonded certifiers;
- **mirrors** of external registers — EU trusted lists, EBSI's registry,
  status lists, national licence lookups, stolen-goods registers — as
  content-addressed snapshots on Swarm, so proposals can pin them;
- **accreditation chains** mirroring EBSI's model (a root accredits
  accreditors, who accredit issuers for specific categories) and national
  accreditation (DAkkS-style), with the relying party choosing the root.

*(added 2026-09-25)* Two rules from the corpus apply to registers and to
the vocabulary pack (C): a wanter names **trust roots**, and the proposal
pins the root of every register on the path (plan D7); and "no pack may be
used to match bonded offers without a bond" (factbond `../../factbond/docs/plans/ontodag-first.md`
§2), so the credential pack carries a coverage give once bonded offers
match on it. *(applied plan G1, G2, E3)* Registers hansa runs are
transparency logs: append-only, consistency proofs between heartbeats,
inconsistency a refutable fact against the register's bond, monitored by
anyone for the winner's share; statements default to `until` in weeks with
cheap renewal; cadence at or below the shortest plausible `max_root_age`;
every accreditation and category names its `scheme`, the published check
procedure.

### C. Vocabulary pack

An ontodag pack for credentials, as ontodag's core pack seeds goods:

- occupations are **not** this pack's *(corrected 2026-09-25)*: ontodag-core
  already builds an `occupations` pack (`docs/OCCUPATIONS.md`, 2026-09-23:
  WordNet person synsets selected with ISCO-08 as witness, a few hundred
  nodes, ESCO as a later witness; see ontodag-core's `../../ontodag-core/docs/ASKS.md` and ontodag's `ROADMAP.md` §3a). This pack adds
  only the credential layer on top: qualification types and EQF levels
  mapped by catalogue edges, licensing status per occupation;
- recognition edges (EU Annex V sectoral professions: doctor, dentist, nurse,
  midwife, pharmacist, vet, architect; the Washington Accord for engineering
  programmes);
- independence (`inspector-type-a ⊑ inspector`, per ISO/IEC 17020);
- evidence basis (above), identity binding levels (D), cover kinds (E).

### D. Identity binding

*(applied plan D8, 2026-09-25)* Binding is **two things**, both nameable in
a requirement, not one ordered chain. A government eID with no photo shown
at the door does not help the counterparty recognise the person in front of
them; a photo with no issuance binding does not say the licence is that
person's.

**The door scale** — checks at presentation time, ordered, cumulative
names, each a witness type in loopmarket's roster:

1. `door-at-least-possession` — a fresh challenge–response from K (nothing
   reusable exists; a copied code dies at once);
2. `door-at-least-photo` — the photo bound to K at issuance, disclosed to
   the counterparty's phone at the door, never published; the public
   statement carries only a commitment to it;
3. `door-at-least-proximity` — NFC or Bluetooth distance bounding against a
   live relay.

**Issuance sources** — how K was bound to the person when the statement was
issued; a *set* the requirer accepts, since these are sources, not levels:

- `issued-by-attester-in-person` — an attester saw the person and the
  document;
- `issued-by-web-of-trust` — bonded vouching by people who know the person
  (encouraged; Circles' trust graph as a source);
- `issued-by-state-document-zk` — a proof from an ePassport chip's signed
  data ("EU national", "over 18", a uniqueness nullifier) with no server and
  no state involvement at use *(to verify: which projects do this today and
  what they prove)*;
- `issued-by-state-document-eid` — a government eID, one adapter, never
  required.

The statement records its source; the requirement lists the acceptable ones
and names a door level. eIDAS's low / substantial / high maps onto the
sources, not onto the door scale.

The handover app: the practitioner's phone answers a fresh challenge from the
counterparty's phone (or shows a QR rotating every few seconds, signed over
the time); the counterparty's phone verifies, then shows the photo and the
statement ("certified electrician, current, insured ≥ X"). A live relay is
stopped by the photo; proximity checks (NFC or Bluetooth distance bounding)
close it further. Presentations are ZK and unlinkable where the credential
allows (BBS+-style signatures); SD-JWT's selective disclosure otherwise.

Key lending (the licensed practitioner lending K) is the residual risk,
priced by the bond and the insurer.

### E. The insurer toolkit

What a specialist insurer needs, most of it composition over loopmarket and
factbond primitives:

1. **Cover vocabulary:** `insure(subject(…) peril(…) period(…) limit(…)
   deductible(…))` — one graph-kind term with nested role heads *(corrected
   2026-09-25; positional arguments are not ontodag grammar, ontodag-core's `../../ontodag-core/docs/ASKS.md` and ontodag's `ROADMAP.md`
   §2)* — with **event cover** (factbond's parametric hedge when E is a feed
   event) and **fact cover** (the verification bet): title ("seller had the
   right to sell h as of D"), "not stolen", "certificate genuine", "licence
   valid at the time of service", inspection cover. Exclusions and
   deductibles as terms. *Professional indemnity* in the sense of negligence
   is **not** an objective trigger and is excluded from v1 (plan D10); what
   remains of it is fact cover on licence validity. Negligence-type claims
   are a **mutual's discretionary product** (plan D9, D10): judged by the
   mutual's own governance, paid from its pool, recorded as a bonded
   statement, labelled discretionary, never a certified fact. The whole of
   E is due a **legal review** before it is folded into a repository (plan
   D10).
2. **Distribution by solvers:** a wanter requiring "insured ≥ X" gets cover
   composed into the loop; insurers post offers, solvers sell at the point
   of need. *(corrected 2026-09-25)* Not "as an operator leg": loopmarket's
   operator algebra requires an operator to move the thing along a dimension
   and rejects one that moves nothing. The composition shape for cover and
   inspection legs is plan D4.
3. **Underwriting by composition:** the cover give requires an `inspect` leg
   (certificate-final and independent, plan E1, E2), an attester's search,
   an identity binding level, a **retention** (the insured's own deposit
   reservation, which pays first; the pool in excess; reinsurance above,
   plan F3), a claims history from the loss view within its look-back, and
   *(applied plan D-1)* a **presentation**: the `insure` term names a hash
   of the facts the insured declared, and a false presentation fact is a
   bonded negation the insurer may assert, reducing the payout
   proportionately. The insurer's own conditions of payout are enforced by
   the resolver (plan D-2): assignment of the insured's claim on the giver's
   reservation before `resolve`, and netting of what that reservation paid.
4. **Capital:** fully collateralised cover works today (the escrow). **Pooled
   cover** is the main enabler of specialist insurers. *(corrected
   2026-09-25)* It is **factbond's**, and largely already planned there:
   `../../factbond/docs/plans/netting-and-reserves.md` §5–§6 adopts a geared payout reserve
   (Nexus-shaped minimum capital requirement, capacity factor, concentration
   cap; gearing a simulation output, G4; a Solvency-II style target), with
   per-fact notional caps that are load-bearing and a rule at the cap that
   is **fail-closed, never pro-rata on shortfall** (F4). factbond also
   insists the *bond pool* (process) and the *payout reserve* (claims) are
   never conflated; "shared pool" above meant the latter. Reinsurance as a
   substitute for caps is rejected there (`../../factbond/docs/plans/insurance-products.md` §4); as
   cover on an insurer's own book it is free recursion. Plan D9 moves A7 to
   factbond as "the geared reserve applied to cover gives", with a mutual
   as the first pooled form.
5. **Pricing from public data:** the loss ledger (factbond §5) and per-category
   claim outcomes — new insurers price from shared data, the incumbents' moat
   removed.
6. **Watching and notice duty:** the insurer watches the registers its cover
   depends on; cover for new sales ends at a revocation; for cleared,
   unperformed legs it writes `notice/` to the insured; **harm between the
   revocation and the notice is the insurer's**, recovered afterwards from the
   insured (the retention deposit; the harmed wanter's claim on the insured's
   deposit reservation, assigned to the insurer via `LoopEscrow.assign` as a
   condition of payout — subrogation, *corrected 2026-09-25*; and outside the
   protocol with loopmarket's records as evidence). Compulsory motor
   insurance's pay-then-recover practice is the precedent *(to verify for
   the EU; the chat's hedge, restored here)*.
7. **Exclusion:** a specific, refutable claim record against a key in the
   loss view; bound to the person by the underwriting binding level, so a
   fresh key does not escape it. *(applied plan F5)* Exclusion is the last
   rung, not the first: after a paid claim the insurer or mutual raises the
   member's retention or caps its cover first; an exclusion has an internal
   second instance under a deadline, and cover is suspended, not cancelled,
   while review is pending.
8. **Rating insurers:** solvency visible on chain; ratings as bonded
   statements about insurers.
9. **Terms construed against the drafter** *(applied plan D-3)*: a cover
   term an adjudicator finds unadjudicable never releases the reservation
   to the insurer, and its drafter forfeits a validity slice. Tail cover is
   `extendClaim`, sold as a give (D-4).

### E′. The mutual's rules *(applied plan D9, F1–F8, 2026-09-25)*

The first pooled form is a mutual on factbond's geared reserve; hansa
supplies its underwriting requirements. Its own rules, from the record of
friendly societies, fire mutuals, P&I clubs, the diamond and cotton
exchanges, the Hanse and Nexus Mutual:

1. **Admission is a survey and a vouch, both, priced.** An attester's or
   register statement, and a member's bonded specific vouch; an entrant
   without a vouch is admitted on a survey alone at a higher initial
   retention.
2. **Vouching pays.** The voucher receives a share of the vouchee's
   premiums or calls for the life of the vouch.
3. **Order of recourse.** The member's own deposit reservation first, the
   pool in excess, reinsurance above; a pool payout for a member's fault
   takes an automatic claim on that member's deposit. No supplementary
   calls: the pool fails closed at the cap, because capital cannot be called
   from a key.
4. **Contributions are risk-rated** by each member's reserved exposure
   and loss record; exit is free; sibling mutuals may form.
5. **Sanctions are graduated**, and exclusion has an internal second
   instance (E.7).
6. **The claims judge is a named committee** of bonded members, excluded
   from their own vouchees' cases, with a separate reversal and replacement
   power, a claimant deposit refunded on acceptance, a fixed decision
   window and a cool-down before payout; decisions are bonded statements,
   labelled discretionary, final on the merits.
7. **Rule changes are by non-liquid member voice**: bonded,
   non-transferable proposals, one member one voice; admission, exclusion
   and claims stay with bonded statements and the committee.
8. **No restriction on outside dealing.** The mutual never restricts
   members' trades outside it; "member of mutual M" is a wanter's optional
   requirement, never a market-wide one.

### F. The personalised trust score (open decision 8 of the chat)

*(corrected 2026-09-25)* Deferred by plan D9: not in this charter's first
version. The reasons, kept here so the decision is traceable:

- the data list below counted countersigns as positive evidence, against
  loopmarket's planned U12 ("delivery never adds credit … nothing positive
  ever flows from the settlement layer", `ARCHITECTURE.md` §11, refined
  2026-09-07) and THREATS T8 ("an undisputed edge is priced unknown, never
  good");
- factbond's calibration ledger already is the per-asserter outcome record;
- P4 §5 item 5 requires every reputation format to accept an
  association-set membership proof in place of an address history, which
  the design below did not;
- it answers only the "newcomer with no capital" case, weakly, and bonded
  vouching answers that case in v1.

What survives: an *attested statement* "from seeds S, with function F
version v, over data roots D, K scores ≥ x" is a fine statement kind for
the gate, produced by a scoring service outside the corpus, re-derivable
and bonded like any attester's statement. The design as drafted:

Reputation without a platform and without wash trades.

- **Data** (public, uncensorable): adjudicated claims (certified, refuted —
  factbond's calibration ledger), bonded vouching, insurers' loss records.
  Cleared fills and countersigns enter only as the *exit* of exposure, never
  as credit (U12). **Only edges with value at stake count** — personal-scale
  trades cost nothing and are ignored as signals.
- **Function:** trust flows from the *viewer's* seeds (its own key, its past
  counterparties, institutions it chose) over the weighted graph —
  personalised PageRank / EigenTrust style; weights by value at stake and
  outcome; adjudicated failures as negative evidence. A sybil cluster gains
  little: trust enters it only through real edges from the seeds.
- **No global number.** Each relying party computes its own. For a gate, a
  scoring service publishes an **attested statement** — "from seeds S, with
  function F version v, over data roots D, K scores ≥ x" — re-derivable by
  anyone, hence challengeable and bonded. loopmarket clearing never computes a
  score and no score is ever a selection weight.
- **Cold start:** newcomers substitute a bond ("score ≥ x or bonded ≥ B").
- **Privacy:** the graph reveals relationships — P4's concern; seeds and
  functions stay local.

## 3. Phasing and gates

| Phase | Deliverable | Gate |
|---|---|---|
| A0 | repo, statement shape shared with loopmarket's R1, attester adapter, possession + photo binding | the dentist case end to end on memory stores: attester statement, `cred/` sidecar, loopmarket gate passes; revoked in the attester's register ⇒ refused |
| A1 | registers as a service + external mirrors (one national licence lookup, one stolen-goods register) | a heartbeat lapse makes statements meet nothing; a mirror snapshot pinned and re-verified |
| A2 | vocabulary pack (ESCO subset, Annex V, evidence basis, binding levels) | the pack loads into ontodag; recognition edges order as expected |
| A3 | cover toolkit on fully collateralised escrow: title fact cover, licence-validity fact cover with retention, presentation, certificate-final inspection | the buyer asserts "no title as of D", the insurer disputes, a certified claim pays net of the giver's reservation after assignment; a false presentation reduces the payout; a claim on an attribute the inspector certified runs against the inspector; revocation-gap harm paid, then recovered from the retention |
| A4 | EU adapter (EDC / SD-JWT VC, EBSI chain) | a sealed EDC diploma yields a verified statement; a tampered one refused |
| A5 | handover app (challenge–response, rotating QR, photo) | a replayed code fails; a relay without the right face is refused by the counterparty |
| ~~A6~~ | trust score library — **deferred** (F; plan D9); attested score statements remain an ordinary attester product | — |
| ~~A7~~ | pooled cover — **moved to factbond** (plan D9: the geared reserve of `../../factbond/docs/plans/netting-and-reserves.md` applied to cover gives; a mutual as the first pooled form) | factbond G3/G4 |

## 4. Open

- The repository's name ("hansa" means life insurance in British usage
  and quality assurance in engineering; a name saying "credentials and
  cover" would collide less).
- Which ZK credential scheme first (BBS+ vs circuits over SD-JWT); which
  passport-ZK project to adopt rather than build (to verify they exist as
  assumed).
- Who may attest each evidence class (factbond's catalogue).

Decided in `plans/credentials-cover-and-options.md` and **applied here on 2026-09-25**: D3
(E.1, E.3, E.6: the insured asserts the trigger, one payout through the
reservation, the indemnity rule, subrogation by assignment as a condition
of payout), D4 (A, E.2: composed cover is a `requires.legs` entry; the
*insured* kind after pooled cover), D8 (D), D9 (E.4, E.5, F, §3: A7 to
factbond with a mutual first, A6 deferred), D10 (E.1: objective triggers;
negligence as a mutual's discretionary product; a legal review before
fold-in).

The practice review's amendments (`../../loopmarket/docs/plans/commercial-practice-review.md`, decided
2026-09-25) are applied: D-1 to D-4 and F3, F5 (E.3, E.7, E.9), F1–F8
(E′), G1, G2, E3 (B), G5 (A), E1, E2 (E.3, §3 A3).
