---
type: Source
title: TriStar MPPT MODBUS Specification V10.2
description: Source metadata and maintenance information for this knowledge bundle
tags: [tristar, modbus, provenance]
---

# Source

- Title: TriStar MPPT MODBUS Specification
- Version: V10.2
- Date: 5 December 2011
- Publisher: Morningstar Corporation
- Canonical source URL: https://www.archcape.com/radio/acrepeater/manuals/TSMPPT.APP.Modbus.EN.10.2.pdf
- Pages: 26
- SHA-256: `f81c4b382b01dccab15921d0ea3d7d14a909452cda728d439cccc318891d6b93`

## Update policy

These documents are an extracted and curated representation of V10.2. When adopting a
new specification, update the version, date, and SHA-256, then review changed registers
and page references.

The local PDF has been verified against the SHA-256 above. If obtaining another copy
from the canonical URL, verify its hash before processing it. Page references in this
bundle use the PDF's printed page numbers (which match its 1-based page positions).

## Extraction coverage and evidence

The Markdown documents summarize the V10.2 sections and preserve known discrepancies.
They are not a verbatim transcription; reserved ranges and some illustrative examples
remain in the source PDF. `registers.json` is a curated subset, not a complete registry.
Absence of a register or field from JSON does not establish absence from the specification.

- Pages 3-4: RAM addresses, Logical Addresses, units, `Signed` column, and scaling.
- Page 14: charge-Ah and kWh counter descriptions.
- Page 25: scaling and two-word examples; hourmeter word order conflicts with page 3.
- Page 26: revision history, including the V08 addition of the signed-data column.

Preserve source facts separately from interpretation: a checked `Signed` cell is
explicit; reading blank cells as unsigned is an interpretation without an explicit
legend in the PDF. See [Scaling and signedness](scaling.md#signedness).

The separately supplied `TS-MPPT-600V_modbus_doc_public.Aug-2014.pdf` describes a
different controller model. It is not an authoritative source for this MPPT-45/60
bundle; do not merge its register definitions without model-specific attribution.

Coverage review for issue #76 includes pages 2–7 (communication and tables),
8–24 (variable descriptions), 25 (worked examples), and 26 (references and
revision history). The [driver inventory](driver-coverage.md) separates current
implementation from source coverage.
