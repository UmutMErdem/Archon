---
profile: "JLCPCB (rigid PCB and PCBA)"
type: "fab"
applies_to: "hardware_design.md"
last_verified: "2026-11-21"
---

# JLCPCB (Rigid PCB and PCBA) Profile

## Scope
JLCPCB rigid PCB fabrication and SMT assembly, with LCSC as its parts catalog. Flex, rigid-flex, and HDI have separate capability pages and are out of scope here. Every value below is a snapshot; the live [capabilities page](https://jlcpcb.com/capabilities/pcb-capabilities) and the order form win over this table.

## Bindings
- **Fabricator capability table (Source Precedence level 4):** Values table below, re-read before each order. Where the persona's DFM Quick Reference is more conservative (6/6 mil), keep the persona value unless it costs layers or board area; then log both options in DECISIONS.md.
- **Stack-up and impedance:** Choose a published JLCPCB stack-up code (for example the JLC04161H family for 4 layers, 1.6 mm) and compute widths with the [JLCPCB impedance calculator](https://jlcpcb.com/help/article/User-Guide-to-the-JLCPCB-Impedance-Calculator) for that code. Enter the code's real dielectric thicknesses and Dk into the EDA stack-up; never reuse widths computed for another code.
- **Fabrication notes:** State the stack-up code, impedance control, finish, via treatment (IPC-4761 type), and any test requirement in the order remarks and in the fabrication drawing; options not selected in the order form are not produced.
- **Parts selection (Cost & Sourcing Optimization):** For assembled boards prefer parts in the assembler's Basic library (no feeder loading fee), then Preferred Extended, then Extended. Record the LCSC code per BOM line as the price and stock baseline for the sourcing profile.
- **Assembly data:** BOM with LCSC codes and CPL (centroid) file from the EDA tool; check rotation and polarity in the order preview, part by part, for polarized parts.

## Values
| Parameter | Value | Source | Checked |
|---|---|---|---|
| Minimum trace / space, 1 oz outer, 2 layers | 5 mil | [JLCPCB copper weight help](https://jlcpcb.com/help/article/jlcpcb-copper-weight) | 2026-11-21 |
| Minimum trace / space, 1 oz, 4–6 layers | 3.5 mil | [JLCPCB copper weight help](https://jlcpcb.com/help/article/jlcpcb-copper-weight) | 2026-11-21 |
| Minimum drill | 0.20 mm (maximum 6.30 mm) | [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) | 2026-11-21 |
| Minimum via hole | 0.3 mm on 1–2 layers, 0.2 mm on multilayer | [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) | 2026-11-21 |
| Minimum annular ring, 1 oz plated hole | 0.13 mm | [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) | 2026-11-21 |
| Extended part feeder loading fee | USD 1.5–3 per unique Extended part depending on PCBA type; Basic parts none | [JLCPCB assembly price](https://jlcpcb.com/help/article/pcb-assembly-price), [TechOverflow overview](https://techoverflow.net/2024/04/09/jlcpcb-pcba-assembly-price-overview/) | 2026-11-21 |

## Procedure
1. Re-read the capabilities page and the chosen stack-up page; update the Values table and `last_verified` if anything changed.
2. Set Board Setup constraints to the fabricator minimums and keep net classes at or above the persona defaults.
3. Compute impedance widths for the selected stack-up code with the fabricator calculator; record them in the impedance target table with the code name.
4. Generate Gerber, drill, BOM, and CPL; upload and review the fabricator's Gerber and assembly previews before paying.
5. Record the order number, stack-up code, and options in DECISIONS.md with the release revision.

## Pitfalls
- **Fee figures from old forum posts:** the Extended-part fee and Basic library changed over time; use the live quote.
- **Widths from another stack-up:** a 90 Ω pair computed for one prepreg type misses target on another code with a different dielectric thickness.
- **Silent defaults:** finish, via tenting, and impedance control fall back to the order form's defaults when not selected.
