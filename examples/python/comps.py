"""Compare a listing's asking price with registered sale prices around it.

    python comps.py crz4qhiy

Asking prices come from the ad (/realestate-details). The comparables come from
/realestate-nearby-deals: completed deals registered with the Israel Tax Authority, with
the price actually paid. Both are compared per square metre.
"""

import sys
from statistics import median

from client import get, per_sqm, sale_date

token = sys.argv[1] if len(sys.argv) > 1 else "crz4qhiy"

ad = get("/realestate-details", token=token)
details = ad.get("additionalDetails") or {}
asking = per_sqm(ad.get("price"), details.get("squareMeter"))
print(f"Ad {token}: {ad.get('price') or 0:,} ILS, {details.get('squareMeter')} m2, "
      f"{details.get('roomsCount')} rooms -> {asking or '?'} ILS/m2 asking")

deals = get("/realestate-nearby-deals", token=token).get("completed") or []
rates = []
for deal in deals:
    rate = per_sqm(deal.get("price"), deal.get("buildingMR"))
    if rate:
        rates.append(rate)
    print(f"  {sale_date(deal)}  {deal.get('price') or 0:>11,} ILS  {deal.get('rooms')} rooms  "
          f"{deal.get('buildingMR')} m2  {rate or '':>7} ILS/m2  {deal.get('propertyType')}  {deal.get('address')}")

if asking and rates:
    paid = median(rates)
    print(f"\nmedian paid {paid:,.0f} ILS/m2 over {len(rates)} deals; "
          f"asking is {(asking - paid) / paid:+.0%} against it")
    # Comparables can be years old and of another property type; check saleDay and
    # propertyType before you trust the gap.
else:
    print("\nNot enough data for a per-m2 comparison.")
