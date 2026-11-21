---
profile: "KiCad 9 / 10"
type: "eda"
applies_to: "hardware_design.md"
last_verified: "2026-11-21"
signals: "*.kicad_pro, *.kicad_sch, *.kicad_pcb, *.kicad_dru"
---

# KiCad 9 / 10 Profile

## Scope
KiCad 9 and 10 schematic, PCB, and `kicad-cli` automation. Run `kicad-cli version` first and record the result in PROJECT_STATE.md; check every CLI option with `kicad-cli <command> -h` on that version before relying on it. Out of scope: KiCad 7 and older (different rule syntax and hidden-pin behavior).

## Bindings
- **Source documents and project library:** Copy every used symbol, footprint, and 3D model into `lib/` and register it in `sym-lib-table` / `fp-lib-table` with `${KIPRJMOD}` paths. Put the local datasheet path (`${KIPRJMOD}/docs/datasheets/...`) in each symbol's `Datasheet` field and SPICE models in `Sim.Library` / `Sim.Name`.
- **Symbol pins match the datasheet:** No hidden `power_in` pins in project symbols; KiCad joins hidden power-input pins to the global net of the same name. Since KiCad 8 power symbols use one visible pin.
- **Schematic connectivity:** Wire inside a functional block; local label within one sheet; hierarchical label plus sheet pin between sheets; power symbol or justified global label only for design-wide nets. All global labels with the same name connect across sheets. A named group bus `USB1{DP DM}` creates nets `USB1.DP` and `USB1.DM`; check the real names in the netlist.
- **ERC with zero unexplained waivers:** `kicad-cli sch erc` with `--exit-code-violations`; report active violations and exclusions separately, each exclusion justified in DECISIONS.md.
- **Schematic equivalence:** Export `kicad-cli sch export netlist --format kicadxml` before and after each change and compare connection sets (see the persona's Schematic Equivalence test).
- **Net classes and custom rules:** Board Setup → Constraints are an absolute floor. In `.kicad_dru` the first line is `(version 1)`, later matching rules win, so order general to specific; use `A.hasNetclass('X')`. A misspelled net class matches nothing without error; check with Inspect → Constraints Resolution. `clearance` applies only between different nets (`physical_clearance` within one net); `hole_to_hole` and `hole_clearance` ignore nets.
- **DRC and parity:** `kicad-cli pcb drc --schematic-parity --exit-code-violations` after zone refill.
- **Routing:** KiCad has no built-in autorouter (Freerouting is an external plugin); use the interactive router in highlight-collisions or walkaround mode, and treat DRC as the final check because the router may not apply every custom rule.
- **Fabrication outputs:** BOM from the schematic (`kicad-cli sch export bom`), not from the PCB; Gerber with X2 and netlist attributes; Excellon with PTH and NPTH in separate files; IPC-D-356 netlist; check zone fills before plotting.

## Values
| Parameter | Value | Source | Checked |
|---|---|---|---|
| CLI exit code when `--exit-code-violations` finds violations | 5 (0 when clean) | [KiCad 10 CLI manual](https://docs.kicad.org/10.0/fr/cli/cli.html), [KiCad 9 CLI manual](https://docs.kicad.org/9.0/en/cli/cli.html) | 2026-11-21 |
| ERC/DRC report formats | `--format report` or `json` | [KiCad 9 CLI manual](https://docs.kicad.org/9.0/en/cli/cli.html) | 2026-11-21 |
| Custom rule precedence | Later matching rule wins; Board Setup minimums cannot be undercut | [KiCad rule help](https://docs.kicad.org/doxygen/panel__setup__rules__help__md_8h.html) | 2026-11-21 |
| Power symbol pins | One visible pin (KiCad 8+); no hidden power-input pins in normal symbols | [KLC S7.1](https://klc.kicad.org/symbol/s7/s7.1.html), [KLC S4.6](https://klc.kicad.org/symbol/s4/s4.6.html) | 2026-11-21 |

## Procedure
1. Record `kicad-cli version`. Create `out/` and move older outputs to a dated folder so no stale file passes as new.
2. Run, then check each exit code and that each output file exists and is not empty; a missing file means "not run", never "passed":
   ```bash
   kicad-cli sch erc --format json --severity-all --exit-code-violations -o out/erc.json board.kicad_sch
   kicad-cli sch export netlist --format kicadxml -o out/netlist.xml board.kicad_sch
   kicad-cli sch export pdf -o out/schematic.pdf board.kicad_sch
   kicad-cli sch export bom -o out/bom.csv board.kicad_sch
   kicad-cli pcb drc --schematic-parity --format json --severity-all --exit-code-violations -o out/drc.json board.kicad_pcb
   ```
3. Review the schematic PDF page by page: can an engineer who has never seen the circuit follow its function and critical connections from the drawing alone?
4. For each custom rule keep a small test board with one violating and one boundary-passing case; run DRC on it, and confirm the test fails when the rule is temporarily relaxed.
5. Before release, open the Gerbers in GerbView (or the fabricator's viewer), not in the PCB editor.

## Pitfalls
- **Plot on All Layers:** adding Edge.Cuts or User.Drawings there prints the outline on every copper layer, and the fabricator reads it as copper.
- **Old zone fills:** Gerbers plotted without refilling zones ship stale copper; enable "Check zone fills before plotting".
- **Deleting and re-adding symbols:** changes UUIDs and breaks the PCB footprint link; edit symbols in place and review the "Update PCB from Schematic" preview for unexpected deletions.
- **Repeated hierarchical sheets:** one sheet file used several times needs unique references after annotation, and a global label inside it shorts the channels together.
- **Silent rule names:** `A.NetClass == 'X'` can miss nets that carry several net classes in KiCad 9; use `A.hasNetclass('X')`.
