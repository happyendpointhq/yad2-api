# Sample responses

Example `200` responses for six Yad2 API endpoints. Field names and values are unchanged
except that long lists are cut to their first few items and seller fields are removed
(`customer`, and `searchText`, which embeds the seller's first name).

Five of them are **live responses captured on 20 October 2026**, not the documentation's
examples: the live search also returns paid placement lists (`platinum`, `booster`) and
fields such as `priceBeforeTag` and `tags`, and the documented nearby-deals example has
empty `statistics`, while the live one is filled in. `vehicles-search.json` is the
example from the public documentation.

| File | Request |
|---|---|
| `regions.json` | `GET /regions` (live) |
| `realestate-search.json` | `GET /realestate-search?deal=forsale&region=3&city=5000&roomsMin=3&roomsMax=4&priceOnly=true` (live) |
| `realestate-details.json` | `GET /realestate-details?token=loicf65f` (live) |
| `realestate-nearby-deals.json` | `GET /realestate-nearby-deals?token=loicf65f` (live) |
| `latest-deals.json` | `GET /latest-deals` (live) |
| `vehicles-search.json` | `GET /vehicles-search` (the documentation example) |

They are useful for writing parsers and tests before you subscribe. Live data changes
daily, so do not hard-code these values.
