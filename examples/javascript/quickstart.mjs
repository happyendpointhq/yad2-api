// Yad2 API quickstart. Node 18+ (built-in fetch), no dependencies.
//   RAPIDAPI_KEY=... node quickstart.mjs

const HOST = 'yad21.p.rapidapi.com';

async function get(path, params = {}) {
  const url = new URL(`https://${HOST}${path}`);
  for (const [key, value] of Object.entries(params)) {
    if (value != null) url.searchParams.set(key, value);
  }
  const res = await fetch(url, {
    headers: { 'x-rapidapi-host': HOST, 'x-rapidapi-key': process.env.RAPIDAPI_KEY },
  });
  if (!res.ok) throw new Error(`Yad2 API ${res.status}: ${await res.text()}`);
  return (await res.json()).data;
}

// Apartments for rent in Tel Aviv (region 3, city 5000), 2 to 3 rooms.
const results = await get('/realestate-search', {
  deal: 'rent',
  region: 3,
  city: '5000',
  roomsMin: 2,
  roomsMax: 3,
});
const ads = [...(results.private ?? []), ...(results.agency ?? [])];
console.log(`${results.pagination.total} ads`);
for (const ad of ads.slice(0, 10)) {
  const d = ad.additionalDetails ?? {};
  const hood = ad.address?.neighborhood?.text ?? '';
  // Rents are monthly (live: 3,000 to 12,500 ILS for 2 to 3 rooms in Tel Aviv).
  console.log(`${String(ad.price ?? '-').padStart(8)} ILS  ${d.roomsCount} rooms  ${d.squareMeter ?? '?'} m2  ${hood}`);
}
