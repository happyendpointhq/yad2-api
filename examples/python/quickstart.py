"""List the regions, search apartments for sale in Tel Aviv, then open the first ad.

    python quickstart.py
"""

from client import get, per_sqm, rows

# 1. Real estate search needs a region id (1 to 8). Names come in Hebrew.
for region in rows(get("/regions")):
    print(f"region {region['region_id']}: {region['region_heb']}")

# 2. 3 to 4 room homes for sale in Tel Aviv (region 3, city 5000), with a published price.
#    Organic results come back in two lists, private sellers and agencies. Paid placements
#    (platinum, booster, privateBooster) are separate lists; they are left out here so a
#    promoted ad is not counted twice when you page through.
results = get(
    "/realestate-search",
    deal="forsale",
    region=3,
    city="5000",
    roomsMin=3,
    roomsMax=4,
    priceOnly="true",
)
listings = results.get("private", []) + results.get("agency", [])
paid = sum(len(results.get(k) or []) for k in ("platinum", "booster", "privateBooster"))
print(f"\n{results['pagination']['total']:,} matching ads; first page has "
      f"{len(results.get('private', []))} private and {len(results.get('agency', []))} agency ads, "
      f"plus {paid} paid placements")
for ad in listings[:10]:
    details = ad.get("additionalDetails") or {}
    hood = ((ad.get("address") or {}).get("neighborhood") or {}).get("text", "")
    rate = per_sqm(ad.get("price"), details.get("squareMeter"))
    rate_text = f"{rate:,} ILS/m2" if rate else ""
    # Observed live: priceBeforeTag holds the earlier price on a reduced ad.
    drop = f"  (was {ad['priceBeforeTag']:,})" if ad.get("priceBeforeTag") else ""
    print(f"{ad.get('price') or 0:>12,} ILS  {details.get('roomsCount')} rooms  "
          f"{details.get('squareMeter') or '?':>4} m2  {rate_text:>15}  {hood}  [{ad['adType']}] {ad['token']}{drop}")

# 3. The full ad by its token: floor, condition, amenities, dates.
if listings:
    ad = get("/realestate-details", token=listings[0]["token"])
    details, address = ad.get("additionalDetails") or {}, ad.get("address") or {}
    print(f"\nAd {ad.get('adNumber')}: {(address.get('street') or {}).get('text', '')}, "
          f"floor {(address.get('house') or {}).get('floor')}")
    print(f"Condition: {(details.get('propertyCondition') or {}).get('text')}")
    print(f"Amenities: {', '.join(k for k, v in (ad.get('inProperty') or {}).items() if v)}")
    print(f"Listed {(ad.get('dates') or {}).get('createdAt')}, updated {(ad.get('dates') or {}).get('updatedAt')}")
