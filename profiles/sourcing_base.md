---
profile: "Sourcing base (any region)"
type: "sourcing"
applies_to: "hardware_design.md"
last_verified: "2026-11-21"
---

# Sourcing Base (Any Region) Profile

## Scope
Region-independent part sourcing and the procurement workbook. A regional profile (`sourcing_<region>.md`) extends this file and adds currency, tax, supplier list, and site behavior. The assembler's parts catalog from the fab profile (for example LCSC for JLCPCB) is the price and stock baseline.

## Bindings
- **Technical fit first (persona Cost & Sourcing Optimization):** Only candidates that meet the datasheet requirements, derating, temperature grade, tolerance, dielectric, and footprint enter the comparison. Classify every offer: `Exact`, `Equivalent`, `Lower grade`, `Not suitable`. `Lower grade` and `Not suitable` are never selected, whatever the price.
- **Selection order among suitable offers:** (1) in stock at one or more suppliers of the region, preferably ≥ 10× the need; (2) lowest line total after MOQ and order multiple, tax included; (3) Active lifecycle; (4) pin-compatible second source; (5) the assembler's Basic part when the board is assembled.
- **Verification on the supplier's own page:** Read stock and price by opening the supplier's product page. Search-engine snippets, caches, old lists, and memory are not accepted. Record per offer: page URL and read date, product name and manufacturer part number on the page, stock status and quantity, price with tax status, quantity the price covers, MOQ, order multiple, fit class.
- **Missing stock:** Lines with no in-stock source in the region are counted and reported to the user before any order with lead time or from abroad; look for an in-stock equivalent first.
- **Freshness:** Stock and prices hold on their read date only. Re-check the selected lines right before ordering, and add a dated update row to the Assumptions sheet each time.

## Values
| Parameter | Value | Source | Checked |
|---|---|---|---|
| Preferred stock margin | ≥ 10× the order need (minimum: the need) | user-supplied (PCB design guide v3.1, TED-01) | 2026-11-21 |
| Offer fit classes | Exact / Equivalent / Lower grade / Not suitable | user-supplied (PCB design guide v3.1, TED-07) | 2026-11-21 |
| Stock status classes | In stock / On order / On request / No stock | user-supplied (PCB design guide v3.1, TED-07) | 2026-11-21 |
| Workbook function requirement | `MINIFS` needs Excel 2019 / 365; write it as `_xlfn.MINIFS` from openpyxl | user-supplied (PCB design guide v3.1, Annex F) | 2026-11-21 |

## Procedure
1. Export the BOM from the schematic. One order line per item; merge BOM lines that share one part under one quote key.
2. For each line, search every supplier in the regional profile plus the assembler catalog; extend the supplier list by web search (authorized distributors, the manufacturer's distributor page for the region, local shops) and add new suppliers to the Supplier Summary sheet.
3. Fill the workbook below. Totals, cheapest-source choice, and status labels are formulas, never typed values, so changing board count, exchange rate, or an offer updates everything.
4. Report the in-stock total, the total including lead-time sources, the assembler-catalog equivalent, and the lines without an in-stock source.

**Procurement workbook** (`<project>-<revision>_procurement_<YYYY-MM-DD>.xlsx`). Sheet order: Purchase, Supplier Summary, Parts List, Supplier Quotes, Assumptions, Assembler Part Class (only for assembled boards). Header row bold on a dark fill; input cells (Assumptions values) visibly marked; everything else is a formula.

| Sheet | Columns | Key formulas |
|---|---|---|
| Assumptions | Name, Value, Note: board count, tax rate, exchange rate with its source, data date; then method notes and dated update rows | — |
| Parts List | Quote key, Group (`Machine assembly` / `Hand assembly` / `DNP` / `Not used`), References, Qty per board, Value and grade, Package, MPN, Assembler code, Assembler stock, Assembler unit price (foreign currency), Assembler unit price (local), Order (Yes/No), Total qty, Best local source, Best local unit price | Total qty = `IF(Order="Yes", Qty per board × board count, 0)`; best source and price looked up from Purchase by quote key |
| Supplier Quotes | Quote key, Supplier, Product on site, Fit, Stock status, Stock qty, Price on site, Tax status, Qty per price, MOQ, Order multiple, Unit price (local, tax incl.), Need, Order qty, Line total, Usable in stock, Usable incl. lead time, Link, Note, Match key, Match key (lead time) | Unit = price × (1 + tax) when tax excluded, ÷ qty per price; Need = `SUMIFS` of Total qty by quote key; Order qty = `CEILING(MAX(Need, MOQ), multiple)`; Usable in stock = fit Exact/Equivalent and In stock and stock ≥ need; Match key = quote key & rounded line total |
| Purchase | Quote key, Part, Assembler code, Need, Lowest in-stock total, Source (in stock), Unit, Lowest total incl. lead time, Source (incl. lead time), Assembler equivalent, Status, Links, Assembly group | Lowest total = `MINIFS` over Supplier Quotes where usable; source found back by `MATCH` on the match key; footer: totals, count of "No in-stock source", count of "No source" |
| Supplier Summary | Supplier, Offers, Exact/Equivalent in stock, On order, Lower grade/Not suitable, Lines selected | `COUNTIF` / `COUNTIFS` over Supplier Quotes and Purchase |
| Assembler Part Class | Reference, Current part, Current code, Class (Basic/Extended), Proposal, Basic equivalent, Proposed code, Proposed class, Impact | Goal: move Extended parts to Basic without breaking technical fit; parts that cannot move go to hand assembly and local sourcing |

## Pitfalls
- **Price for a lower grade:** a cheaper capacitor with worse dielectric, voltage, or tolerance looks like a saving and fails in the field.
- **Single-batch stock:** stock visible at one supplier in one lot can vanish before the order; note it and keep a second source.
- **Mixed tax bases:** some suppliers show prices without tax and others with tax; normalize before comparing.
- **Typed totals:** a total typed by hand goes stale when the board count or rate changes; use formulas.
