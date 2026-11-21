---
profile: "Sourcing: Türkiye"
type: "sourcing"
applies_to: "hardware_design.md"
last_verified: "2026-11-21"
extends: "sourcing_base.md"
---

# Sourcing: Türkiye Profile

## Scope
Part sourcing from suppliers that deliver within Türkiye, priced in TRY. Procedure and workbook come from [sourcing_base.md](sourcing_base.md); this file adds currency, tax, the supplier list, and observed site behavior. Site behavior changes without notice: re-check it when a result looks inconsistent.

## Bindings
- **Currency and tax:** Compare unit prices in TRY with KDV included. Convert foreign-currency prices (assembler catalog) with the exchange rate on the Assumptions sheet and write where the rate came from.
- **Supplier classes:** Prefer authorized distributors for critical parts (MCU, power IC, reference, sensor). For retail and hobby shops, note in the Note column when originality or the exact grade (dielectric, tolerance) cannot be confirmed from the page.
- **Search method per site:** Search by manufacturer part number first; for passives on retail sites search by value and package (`10k 0603`, `100nF smd`). Mark a site with no result as "no offer" instead of skipping it silently.
- **No in-stock source in Türkiye:** Report the line to the user before ordering with lead time or from abroad, and propose an in-stock equivalent first.

## Values
| Parameter | Value | Source | Checked |
|---|---|---|---|
| Currency | TRY | — (region definition) | 2026-11-21 |
| KDV standard rate | 20 % (check the product's GİB rate if unsure) | [Kintsugi Türkiye VAT guide 2026](https://trykintsugi.com/sales-tax-guides/middle-east/turkey) | 2026-11-21 |
| Özdisan Elektronik | Authorized distributor (200+ brands, offices in İstanbul, Ankara, İzmir, Bursa); user observed prices shown without KDV, "Stok 0" ships on order, "Talep üzerine" has no price | [Özdisan about us](https://www.ozdisan.com/en/about-us); behavior: user-supplied 2026-11-09 | 2026-11-21 |
| Farnell via SAMM Teknoloji | Farnell's logistics partner in Türkiye; quoted delivery 7–10 working days from UK stock, 18–21 from US stock | [SAMM / Farnell](https://www.samm.com/?p=3029) | 2026-11-21 |
| direnc.net | Retail electronics and maker shop; many items "Stokta Yok"; minimum purchase quantities on resistors | [direnc.net](https://www.direnc.net/yeni-urunler); minimum quantities: user-supplied 2026-11-09 | 2026-11-21 |
| e-komponent | Retail; user observed "SEPETE EKLE" = in stock, "STOK YOK / GELİNCE HABER VER" = no stock, prices with KDV, some items from foreign stock | user-supplied 2026-11-09 | 2026-11-21 |
| Robotistan, Karaköy Elektronik | Retail and hobby shops on the user's start list | user-supplied 2026-11-09 | 2026-11-21 |
| Price baseline | LCSC / assembler catalog price converted to TRY | [sourcing_base.md](sourcing_base.md) | 2026-11-21 |

## Procedure
1. Start from the supplier rows above and extend the list by web search (manufacturer distributor pages for Türkiye, other authorized distributors); add every new supplier to the Supplier Summary sheet.
2. Follow [sourcing_base.md](sourcing_base.md) steps 1–4, reading each offer on the supplier's own product page.
3. In the Assumptions sheet record board count, KDV rate, USD/TRY rate and its source, and the data date.
4. Report totals (in stock in Türkiye, including lead time, LCSC equivalent) and the lines with no source in Türkiye.

## Pitfalls
- **KDV mixed in comparisons:** Özdisan shows prices without KDV while retail shops show prices with KDV; normalize first.
- **Foreign stock shown as local:** some retail listings ship from abroad; record the lead time.
- **Retail grade uncertainty:** hobby listings often omit dielectric or tolerance; treat such an offer as `Lower grade` until the page or the manufacturer part number proves otherwise.
