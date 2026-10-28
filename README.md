# Yad2 API and Scraper

The Yad2 API returns Israel's largest classifieds site as JSON: real estate for sale and
rent (with rooms, size, floor, amenities and price drops), new construction projects,
government-registered sale prices, cars and other vehicles, and second-hand marketplace
listings. Yad2 has no public developer API, so this REST API is the way to use its data in
your own code without building and maintaining a Yad2 scraper.

Built and maintained by [Happy Endpoint](https://happyendpoint.com/library/yad2-api?utm_source=github&utm_medium=readme&utm_campaign=yad2-api).

- Subscribe and test every endpoint on RapidAPI: https://rapidapi.com/happyendpoint/api/yad21
- Product page: https://happyendpoint.com/library/yad2-api?utm_source=github&utm_medium=readme&utm_campaign=yad2-api

---

## At a glance

| | |
|---|---|
| Base URL | `https://yad21.p.rapidapi.com` |
| Auth | `x-rapidapi-key` and `x-rapidapi-host` headers |
| Endpoints | 25, all `GET` |
| Coverage | All of Israel: 8 regions, 1,454 cities and their neighborhoods |
| Verticals | Real estate (for sale, rent, commercial), vehicles, marketplace |
| Currency and units | Israeli new shekels (ILS), square metres |
| Format | JSON, every response wrapped in `{"success": true, "data": ...}` |

---

## What data you get

**Real estate**
- Search for sale, rent or commercial property by region, city, neighborhood, property type, price, rooms, size and floor, with filters for balcony, elevator, parking, air conditioning, furniture, renovation, accessibility, a safe room (mamad), new from a contractor and pets
- Map search inside a bounding box, and map clusters for zoomed-out views
- Full ads by token or by Yad2 URL: rooms, size, balconies, floor, condition, amenities, entry date, coordinates, photos, created and updated dates
- New construction projects (Yad1) and projects near a listing, plus agency promotions

**Registered sale prices**
- Recent completed deals near any listing, with address, rooms, size, floor, build year, price paid and sale date, plus area statistics
- The latest registered deals across Israel

**Vehicles and marketplace**
- Cars, motorcycles, scooters, trucks and watercraft by manufacturer, model, year, price, mileage, hand (number of previous owners), gearbox and engine type
- Full vehicle ads, the manufacturer and model catalogue, dealer ads
- Second-hand marketplace listings and details

**Reference data**
- Regions, cities, neighborhoods, categories, location autocomplete and search filter options

---

## Quick start

### 1. Get an API key

Subscribe on [RapidAPI](https://rapidapi.com/happyendpoint/api/yad21). Copy `.env.example`
to `.env` and paste your key.

### 2. Make a request

Real estate search requires a `region` (1 to 8, from `/regions`). City ids come from
`/cities` or `/locations-autocomplete`; Tel Aviv-Yafo is `5000`.

```bash
curl "https://yad21.p.rapidapi.com/realestate-search?deal=forsale&region=3&city=5000&roomsMin=3&roomsMax=4" \
  -H "x-rapidapi-host: yad21.p.rapidapi.com" \
  -H "x-rapidapi-key: YOUR_RAPIDAPI_KEY"
```

### Python

```bash
pip install -r requirements.txt
cd examples/python
python quickstart.py
```

```python
from client import get

results = get("/realestate-search", deal="forsale", region=3, city="5000", roomsMin=3, roomsMax=4)
for ad in results["private"] + results["agency"]:
    print(ad["price"], ad["additionalDetails"]["roomsCount"], ad["token"])
```

### JavaScript

```bash
RAPIDAPI_KEY=your_key node examples/javascript/quickstart.mjs
```

---

## Example response

One organic row from `GET /realestate-search?deal=forsale&region=3&city=5000`, trimmed.
Values are from a live call on 20 October 2026. The full responses are in
[`samples/`](samples/).

```json
{
  "success": true,
  "data": {
    "private": [
      {
        "token": "loicf65f",
        "adType": "private",
        "price": 6650000,
        "priceBeforeTag": 6890000,
        "address": {
          "region": { "id": 3, "text": "תל אביב והסביבה" },
          "city": { "id": 5000, "text": "תל אביב יפו" },
          "neighborhood": { "text": "איזור שדה דב" },
          "house": { "floor": 2 }
        },
        "additionalDetails": {
          "property": { "text": "דירה" },
          "roomsCount": 4,
          "squareMeter": 123
        }
      }
    ],
    "agency": ["..."],
    "platinum": ["..."],
    "booster": ["..."],
    "pagination": { "total": 5560, "totalPages": 264 }
  }
}
```

---

## Endpoints

Base URL: `https://yad21.p.rapidapi.com`

### Real estate

| Endpoint | Returns |
|---|---|
| `GET /realestate-search` | Listings for sale, rent or commercial, with all filters |
| `GET /realestate-map` | Listings inside a bounding box |
| `GET /realestate-map-clusters` | Listing clusters for a map view |
| `GET /realestate-details` | The full ad by token |
| `GET /realestate-details-by-url` | The full ad from a Yad2 URL |
| `GET /realestate-search-options` | Filter option lists, such as property type ids |
| `GET /realestate-agency-promos` | Agency banner cards for a search |
| `GET /realestate-yad1-projects` | New construction projects (Yad1) |
| `GET /realestate-yad1-nearby` | New projects near a listing |

### Registered sale prices

| Endpoint | Returns |
|---|---|
| `GET /realestate-nearby-deals` | Completed deals near a listing, with statistics |
| `GET /latest-deals` | The latest completed deals across Israel |

### Vehicles

| Endpoint | Returns |
|---|---|
| `GET /vehicles-search` | Vehicle ads with make, model, year, price, mileage and hand filters |
| `GET /vehicles-details` | The full vehicle ad by token |
| `GET /vehicles-details-by-url` | The full vehicle ad from a Yad2 URL |
| `GET /vehicles-catalog` | Manufacturers and models for a vertical |
| `GET /vehicles-models` | Models for a manufacturer |
| `GET /vehicles-agency-ads` | Other ads from the same dealer |

### Marketplace and reference data

| Endpoint | Returns |
|---|---|
| `GET /marketplace-listings` | Second-hand marketplace listings |
| `GET /marketplace-details` | One marketplace listing |
| `GET /locations-autocomplete` | Cities, areas and neighborhoods matching typed text |
| `GET /regions` | The 8 regions real estate search requires |
| `GET /cities` | Every city with its id |
| `GET /neighborhoods` | Neighborhoods of a city |
| `GET /categories` | Yad2 categories |
| `GET /status` | Service health |

---

## Things to know about the data

These come from building against the API and running it live.

- **Organic and paid results come in separate lists.** `/realestate-search` returns
  `private` (private sellers) and `agency` as the organic results, and paid placements in
  `platinum`, `booster` and `privateBooster`. On our live Tel Aviv search the first page
  had 20 private, 20 agency, 3 platinum and 1 booster ad. Use the two organic lists when
  you page through a market, or a promoted ad can be counted on every page.
- **Agency ads say `commercial`.** Rows in the `agency` list carry `adType: "commercial"`,
  not `"agency"`. Private rows carry `"private"`.
- **Rooms come in halves.** Israeli listings count the living room as a room and use half
  rooms: `3.5` and `5.5` are normal values, and `roomsMin` accepts them.
- **A price drop leaves a trace.** Live rows and details can carry `priceBeforeTag`, which
  on the ads we saw was the earlier, higher price (6,890,000 ILS before 6,650,000 ILS). The
  documentation does not describe it, so treat it as observed behaviour. `quickstart.py`
  prints it.
- **Registered deals are what was paid, and they lag.** `/latest-deals` and
  `/realestate-nearby-deals` come from completed deals registered with the Israel Tax
  Authority. On 20 October 2026 the newest deal in `/latest-deals` was dated 17 September
  2026, and the newest deal near our Tel Aviv listing 2 August 2026. Expect weeks of lag.
- **Deal dates and sizes use their own fields.** Deals give `saleDay` as `DD.MM.YY`
  (`"04.06.26"` is 4 June 2026) and the size as `buildingMR`, square metres. Ads use
  `squareMeter`. `client.sale_date()` parses the date.
- **Check the comparables before you trust a gap.** Near one Tel Aviv listing, five of the
  seven nearby deals were units in one new tower and the other two in another building, all
  sold before completion. One was 16.8 million ILS for 188 m2 on the 41st floor (89,586 ILS
  per m2), against 50,000 to 63,000 ILS per m2 for the rest. Take the
  median, and look at `propertyType` and `saleDay`. The `statistics` block (live: 173
  deals, average 6.96 million ILS) covers a wider pool than the `completed` rows returned.
- **Region is required.** Real estate search, map and project endpoints need `region`
  (1 to 8). Region ids are not in name order; read them from `/regions`.
- **Hebrew first.** Place names, property types and conditions come in Hebrew (`text`);
  some objects add `textEng` (`"apartment"`, `"Petrol"`). Keep ids for joins and filters.
- **Rents are monthly.** On our live rental search, 2 to 3 room flats in Tel Aviv were
  3,000 to 12,500 ILS, which are monthly rents.

---

## Examples in this repo

| File | What it does |
|---|---|
| [`examples/python/quickstart.py`](examples/python/quickstart.py) | Regions, a filtered Tel Aviv search with price per m2 and price drops, one full ad |
| [`examples/python/comps.py`](examples/python/comps.py) | Compares a listing's asking price per m2 with registered sale prices around it |
| [`examples/python/latest_deals_to_csv.py`](examples/python/latest_deals_to_csv.py) | Saves the latest registered sales in Israel to CSV with price per m2 |
| [`examples/javascript/quickstart.mjs`](examples/javascript/quickstart.mjs) | A Tel Aviv rental search in Node 18+, no dependencies |
| [`samples/`](samples/) | Example responses for six endpoints |

---

## API or your own Yad2 scraper

Yad2 scrapers on GitHub break when the site changes its pages, its internal endpoints or
its bot protection, and most cover one vertical. This API returns real estate, registered
deals, vehicles and the marketplace as documented JSON with a stable contract. If you need
a one-off file or a recurring export rather than API calls,
[contact us](https://happyendpoint.com/contact?utm_source=github&utm_medium=readme&utm_campaign=yad2-api).

---

## Use it from Claude, Cursor or any MCP client

RapidAPI exposes every endpoint as an MCP tool, so an AI assistant can query Yad2 without
code:

```json
{
  "mcpServers": {
    "yad2": {
      "command": "npx",
      "args": [
        "mcp-remote",
        "https://mcp.rapidapi.com",
        "--header",
        "x-api-host: yad21.p.rapidapi.com",
        "--header",
        "x-api-key: YOUR_RAPIDAPI_KEY"
      ]
    }
  }
}
```

| Client | Config path |
|---|---|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `~/.cursor/mcp.json` |
| Claude Code | `.mcp.json` in your project root |

---

## FAQ

### Is there a Yad2 API?

Yad2 does not publish a public developer API. This API, built and maintained by Happy
Endpoint and independent of Yad2, provides that access as REST and JSON.

### Is there a free Yad2 API?

Yes. The [RapidAPI listing](https://rapidapi.com/happyendpoint/api/yad21) has a free plan,
and every endpoint can be tried on it.

### Is there a Yad2 scraper in Python?

[`examples/python/`](examples/python/) has a small client and three ready-to-run scripts.
They call this API instead of parsing Yad2 pages, so they keep working when the site
changes.

### Can I get actual sale prices, not only asking prices?

Yes. `/realestate-nearby-deals` returns registered deals near any listing, and
`/latest-deals` the newest across Israel, each with the price paid and the sale date.
[`comps.py`](examples/python/comps.py) compares the two.

### Can I search Yad2 cars?

Yes. `/vehicles-search` covers cars, motorcycles, scooters, trucks and watercraft, with
manufacturer and model ids from `/vehicles-catalog` and `/vehicles-models`.

### Can I get the data in English?

Most text is Hebrew, as on the site. Some fields add `textEng`, and every entity has a
numeric id you can map to your own labels.

### Do you cover other property markets?

Yes, including the UAE, Saudi Arabia, Spain, the UK and the US. See the
[API library](https://happyendpoint.com/library?utm_source=github&utm_medium=readme&utm_campaign=yad2-api).

---

## Related repos

- [awesome-real-estate-apis](https://github.com/happyendpointhq/awesome-real-estate-apis) - real estate APIs and data sources by country, including free and official ones
- [uae-real-estate-api](https://github.com/happyendpointhq/uae-real-estate-api) - asking versus paid prices in Dubai, the same idea as `comps.py`
- [aqar-api](https://github.com/happyendpointhq/aqar-api) - Saudi Arabia listings and district prices
- [rent-com-api](https://github.com/happyendpointhq/rent-com-api) - US rentals, with a watchlist and CSV export
- [fotocasa-api](https://github.com/happyendpointhq/fotocasa-api) - Spanish listings for sale and rent, with a search-to-CSV export

---

## Disclaimer

Happy Endpoint is an independent provider. This project is **not affiliated
with, endorsed by, sponsored by, or connected to** any of the websites,
platforms, retailers, or marketplaces referenced here or reachable through the
underlying APIs.

All product names, brands, trademarks, and registered trademarks are the
property of their respective owners. Any reference to them is descriptive only,
to identify the subject matter of the data, and does not imply any association
or endorsement.

Users are responsible for ensuring their use of any data complies with
applicable laws and the terms of service of the relevant source.

---

## About Happy Endpoint

[Happy Endpoint](https://happyendpoint.com) builds and maintains real-time data
APIs for property portals, retailers, and marketplaces. All APIs are available on
RapidAPI with a free tier.

- Catalogue: [happyendpoint.com/library](https://happyendpoint.com/library)
- Datasets: [happyendpoint.com/datasets](https://happyendpoint.com/datasets)
- Documentation: [docs.happyendpoint.com](https://docs.happyendpoint.com)
- Contact: happyendpointhq@gmail.com

## Licence

MIT. See [LICENSE](LICENSE).
