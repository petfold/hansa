# hansa — research notes: what existing institutions teach

Status: reference, carried from the assurance drafts of 2026-09-23. Condensed from the chat record;
items marked *(to verify)* were not confirmed from a primary source.

## 1. TÜV — inspection, certification, liability

**Facts**
- Mannheim, 6 January 1866: after a brewery boiler explosion, twenty boiler
  owners founded the *Gesellschaft zur Überwachung und Versicherung von
  Dampfkesseln* — supervision **and insurance**. The same year the Hartford
  Steam Boiler Inspection and Insurance Company bundled inspection with
  insurance in the US.
- The associations were mutuals of the inspected; from 1871 membership
  exempted a boiler from state inspection. Today TÜVs are *Beliehene*
  (private bodies with delegated state authority); deregulation brought
  DEKRA and GTÜ as competitors.
- Two layers on cars: the statutory *Hauptuntersuchung* (pass/fail, graded
  defects) and the voluntary buyer-side *Gebrauchtwagencheck* (a report).
- Since 2013 TÜV Rheinland uses one mark with a ten-digit ID and QR code,
  resolvable in Certipedia; the ID binds to a product *model*, not an item.
- ISO/IEC 17020 (inspection bodies; independence Type A/B/C, *reportedly*
  simplified to A / non-A in a 2026 revision — *to verify*; the chat's hedge
  had been dropped) and ISO/IEC 17065 (certification bodies); accreditation
  in Germany by DAkkS.
- PIP breast implants: TÜV Rheinland certified the manufacturer's quality
  *system*; PIP swapped in industrial silicone. CJEU *Schmitt* (C-219/15,
  2017): notified bodies have no general duty of unannounced inspections. The
  French Cour de cassation (25 May 2023) confirmed TÜV had not met its duties
  and remanded — thirteen years after the fraud surfaced.
- Brumadinho (25 January 2019, 270 dead): TÜV SÜD issued the dam's stability
  declaration; criminal charges in Brazil, a Munich civil suit (~1,400
  claimants), hearings in May 2026.

**Lessons used**
- Inspection and insurance belong together; the insurer wants honest
  inspection → hansa E.3, E.6.
- The certified paying the certifier is the core incentive failure → the
  relying party pays; the insurer judges certifiers; per-certifier loss data
  → loopmarket items §3, factbond §5, hansa E.
- A process certificate is not an item certificate → `item(h)`.
- Courts are slow and uncapped, bonds fast and capped → both, sized to harm.
- Certification is a lifecycle (issue, surveillance, suspension, withdrawal)
  → registers with heartbeat and revocation.

## 2. Recognition of qualifications

- **EU Directive 2005/36/EC:** automatic recognition for seven sectoral
  professions (doctor, dental practitioner, nurse for general care, midwife,
  pharmacist, veterinary surgeon, architect) because training meets
  harmonised minimum requirements; a general system otherwise.
- **Directive 2013/55/EU:** the IMI alert mechanism for bans (from 18 January
  2016). An OCCRP/VG/Times investigation (October 2025) found over 100 doctors
  banned in one country and licensed in another; most EU countries do not
  publish bans. Push-based revocation fails → pull with absence proofs.
- **Germany, third-country dentists:** the *Approbation*, an equivalence
  check, and failing that a *Kenntnisprüfung* (written, oral, practical) —
  re-inspection when no recognition edge exists.
- **ECFMG (2024):** medical schools must be accredited by an agency recognised
  by the WFME (or NCFMEA) — trust sits one level above the school. EPIC does
  primary-source verification of diplomas with the issuing school.
- **Lisbon Recognition Convention (1997):** recognised unless the authority
  shows a "substantial difference" — the burden on the refuser (an optimistic
  edge). ENIC-NARIC issue statements of comparability.
- **Engineering:** the Washington Accord (accreditors recognising each other);
  EUR ING (Engineers Europe's register).
- **Aviation:** ICAO Annex 1 as the global floor; EASA gives no automatic
  conversion of third-country licences, only credits.

## 3. Digital credentials and identity

- **eIDAS 2.0** (Regulation (EU) 2024/1183): an EUDI Wallet in every member
  state by 24 December 2026; regulated private-sector acceptance from 24
  December 2027; formats SD-JWT VC and ISO mdoc.
- **EDC** (Europass): sealed learning credentials on the European Learning
  Model.
- **EBSI's trust model:** Root TAO → TAOs → Trusted Issuers accredited for
  specific credential types, public in the Trusted Issuers Registry.
- **Outside the EU** *(to verify)*: US state mobile driving licences (ISO
  18013-5), W3C VCs / Open Badges, per-state licence lookups; India's Aadhaar
  and DigiLocker; ePassports worldwide (state-signed chip data, readable by
  phone) — the basis for ZK proofs without a new government ID system.

## 4. Title insurance *(to verify in detail)*

A one-time premium at closing covers losses from title defects existing on
the policy date (forged deeds, undisclosed liens or heirs, record errors); a
lender's policy usually required, an owner's optional; most of the premium
pays for the title search. It thrives where registries are weak (US deed
recording); where the register guarantees title — Torrens systems with state
assurance funds, Germany's Grundbuch with public faith (§892 BGB) and the
notary — the state is in effect the insurer. Lesson: a register that
guarantees title is an insurer; where none does, someone sells the guarantee.

## 5. Other precedents

- Compulsory motor insurance *(to verify for the EU)*: the insurer pays the
  third-party victim despite the driver's breach, then recovers from its
  insured — the model for the revocation gap.
- Etherisc (flight delay, parametric, on Gnosis) and Nexus Mutual
  (discretionary mutual) as chain-based cover *(to verify)*.
- Rotating ticket barcodes and challenge–response as copy resistance.

## Sources

- [TÜV Rheinland — Wikipedia](https://en.wikipedia.org/wiki/T%C3%9CV_Rheinland) · [Technischer Überwachungsverein — Wikipedia](https://en.wikipedia.org/wiki/Technischer_%C3%9Cberwachungsverein) · [Certipedia](https://www.certipedia.com/)
- [TÜV Rheinland on the French Supreme Court PIP decisions](https://www.tuv.com/press/en/press-releases/tuev-rheinland-pip-implant-case-decisions-french-supreme-court.html) · [ECCHR on Brumadinho](https://www.ecchr.eu/en/case/the-safety-business-tuev-sueds-role-in-the-brumadinho-dam-failure-in-brazil/) · [Agência Brasil: Munich hearings](https://agenciabrasil.ebc.com.br/en/meio-ambiente/noticia/2026-01/hearings-over-dam-collapse-brumadinho-scheduled-munich)
- [HSB history](https://www.munichre.com/hsbeil/en/about-us/hsb-engineering-insurance/history.html) · [checkdenwagen: HU vs Gebrauchtwagencheck](https://www.checkdenwagen.de/magazin/wert-und-preis/unterschied-hu-gebrauchtwagencheck) · [DAkkS: inspection bodies](https://www.dakks.de/en/inspection-bodies.html) · [ITIC: inspection body types](https://iticglobal.org/inspection-body-types-a-b-and-c-explained-iso-iec-170202012-compliance-guide/)
- [Directive 2005/36/EC](https://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=OJ:L:2005:255:0022:0142:en:PDF) · [Directive 2013/55/EU](https://eur-lex.europa.eu/eli/dir/2013/55/oj/eng) · [OCCRP/VSquare: banned doctors](https://vsquare.org/bad-practice-how-banned-doctors-find-new-jobs-across-europe/)
- [Anerkennung in Deutschland: dentist](https://www.anerkennung-in-deutschland.de/html/en/2728.php) · [ECFMG accreditation requirement](https://www.ecfmg.org/news/2020/05/13/ecfmg-medical-school-accreditation-requirement-moved-to-2024/) · [Lisbon Recognition Convention](https://www.enic-naric.net/page-lisbon-recognition-convention)
- [Washington Accord](https://www.internationalengineeringalliance.org/accords/washington-accord) · [EUR ING](https://www.engineerseurope.com/what-eur-ing-certificate) · [ICAO licensing FAQ](https://www.icao.int/personnel-licensing-faq)
- [EUDI Wallet deadline](https://www.eadtrust.eu/en/blog/december-2026-deadline-eudi-wallet/) · [SD-JWT VC and mdoc](https://docs.igrant.io/concepts/eudi-wallet-verifiable-credential-formats/) · [EDC](https://europass.europa.eu/en/european-digital-credentials-learning) · [EBSI issuer trust model](https://hub.ebsi.eu/vc-framework/trust-model/issuer-trust-model-v4)
