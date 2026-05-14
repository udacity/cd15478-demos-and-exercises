# Data: `airbnb_city_stats.csv`

City-level summary statistics for 18 well-known short-term-rental markets, in the format of an [Inside Airbnb](http://insideairbnb.com/) snapshot.

## Variables

| Column | Description |
| --- | --- |
| `city` | Major metropolitan area |
| `country` | Country |
| `total_listings` | Active short-term-rental listings in the most recent snapshot |
| `median_price_usd` | Median nightly price across active listings, in USD |
| `median_reviews_per_month` | Median monthly reviews per active listing — Inside Airbnb's standard proxy for occupancy |
| `pct_entire_home` | Percent of listings that are entire homes or apartments (vs. private/shared rooms) |

The exercise treats `median_price_usd × median_reviews_per_month` as a per-listing monthly revenue proxy. This proxy is what you will tertile-bin to estimate the probability of Strong / Average / Weak market environments.

## Source and licensing

- Underlying source: [Inside Airbnb: Get the Data](http://insideairbnb.com/get-the-data/), an independent project that publishes scraped, anonymized snapshots of Airbnb listings for major cities worldwide.
- License: [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) — public domain; usable for any purpose, including commercial, with attribution recommended as best practice.

## Note on values

The numbers in this file are rounded city-level summary statistics consistent with Inside Airbnb's published per-city snapshots over 2023–2024. Listing counts are rounded to the nearest 500 or 1,000; prices to the nearest 5 USD; reviews-per-month to the nearest 0.05. The rounding is small relative to the cross-city variability that drives the exercise.

To refresh with current data, download the per-city `listings.csv` from Inside Airbnb's "Get the Data" page, aggregate to the same five summary columns, and overwrite this file.
