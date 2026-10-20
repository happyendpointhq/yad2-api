"""Save the latest registered property sales in Israel to CSV, with price per m2.

    python latest_deals_to_csv.py --out deals.csv

/latest-deals returns recent completed deals reported to the Israel Tax Authority: the
price actually paid, not an asking price. Hebrew text is kept as is; the file is written
with a byte order mark so Excel shows it correctly.
"""

import argparse
import csv

from client import get, per_sqm, sale_date

COLUMNS = ["sale_date", "price_ils", "sqm", "ils_per_sqm", "rooms", "floor", "number_of_floors",
           "build_year", "property_type", "address"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="latest-deals.csv")
    args = parser.parse_args()

    deals = get("/latest-deals")
    with open(args.out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS)
        writer.writeheader()
        for deal in deals:
            writer.writerow({
                "sale_date": sale_date(deal),
                "price_ils": deal.get("price"),
                "sqm": deal.get("buildingMR"),
                "ils_per_sqm": per_sqm(deal.get("price"), deal.get("buildingMR")),
                "rooms": deal.get("rooms"),
                "floor": deal.get("floor"),
                "number_of_floors": deal.get("numberOfFloors"),
                "build_year": deal.get("buildYear"),
                "property_type": deal.get("propertyType"),
                "address": deal.get("address"),
            })
    print(f"Wrote {len(deals)} deals to {args.out}")


if __name__ == "__main__":
    main()
