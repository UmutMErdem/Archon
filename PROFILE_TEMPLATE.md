# <Profile Name> Profile

<!--
HOW TO USE THIS TEMPLATE
A profile binds a persona's tool-agnostic rules to one concrete third-party tool, vendor, or region:
an EDA tool (type eda), a fabricator or assembler (type fab), or a sourcing region with its
suppliers (type sourcing). The persona says WHAT must be checked; the profile says HOW and WITH
WHICH VALUES for that tool, vendor, or region. Personas never name a single vendor's numbers.

1. Copy this file to `profiles/<type>_<name>.md` (e.g. `profiles/fab_pcbway.md`, `profiles/sourcing_de.md`).
2. Add YAML frontmatter at the top:
     ---
     profile: "<Display name>"
     type: "eda" | "fab" | "sourcing"
     applies_to: "<persona file>"          # e.g. "hardware_design.md"; several: "a.md, b.md"
     last_verified: "YYYY-MM-DD"           # date the Values table was last checked at its sources
     extends: "<base profile file>"        # optional, same type, e.g. "sourcing_base.md"
     signals: "<glob>, <glob>"             # optional, files that select this profile automatically
     ---
3. Keep the five headings below verbatim; scripts/validate_manifesto.py checks them.
4. Every row of the Values table has a Source (URL, document and revision, or "user-supplied") and
   a Checked date. A value nobody checked does not go in the table.
5. Values change (capability tables, prices, CLI flags). The engine re-verifies a profile whose
   last_verified date is older than 180 days before using its values (architecture/00_detection.md).
6. Run `python scripts/validate_manifesto.py` until it reports no errors.
-->

## Scope
<!-- Tool, vendor, or region; supported versions; what is out of scope. -->

## Bindings
<!-- Map persona rules to this tool or vendor: "Persona rule → how it is done here".
Format: - **<persona rule or check>:** <tool-specific way> -->

## Values
<!-- Dated, sourced values the persona leaves open. -->
| Parameter | Value | Source | Checked |
|---|---|---|---|

## Procedure
<!-- Ordered steps or commands that apply the persona's checks with this tool, vendor, or region. -->

## Pitfalls
<!-- Tool- or vendor-specific traps. Format: - **<Title>:** <what goes wrong and how to avoid it> -->
