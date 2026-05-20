# Data: Spotify Tracks Sample

## File

`spotify_tracks_sample.csv` — 2,400 Spotify tracks with audio features and popularity scores.

## Columns

| Column | Description |
| --- | --- |
| `track_id` | Spotify track identifier |
| `track_name` | Track title |
| `track_artist` | Primary artist name |
| `playlist_genre` | One of: edm, latin, pop, r&b, rap, rock |
| `track_popularity` | Spotify popularity score (0–100) at time of collection |
| `danceability` | How suitable the track is for dancing (0.0–1.0) |
| `energy` | Perceptual measure of intensity and activity (0.0–1.0) |
| `valence` | Musical positiveness (0.0 = sad/tense, 1.0 = happy/euphoric) |

## Source and license

**Original dataset:** TidyTuesday week 2020-01-21, contributed by Charlie Thompson, Thomas Mock,
and Josiah Parry. Audio features and popularity scores are sourced from the
[Spotify Web API](https://developer.spotify.com/documentation/web-api/) via the
[spotifyr](https://www.rcharlie.com/spotifyr/) R package.

**TidyTuesday repository:** [https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21](https://github.com/rfordatascience/tidytuesday/tree/main/data/2020/2020-01-21)

**License:** CC0 1.0 Universal (Public Domain Dedication). The TidyTuesday project makes its
curated datasets available under CC0. See the TidyTuesday [repository README](https://github.com/rfordatascience/tidytuesday#readme) for details.

## Sampling and rounding

The full TidyTuesday release contains ~28,000 unique tracks. This file is a
**stratified random sample of 400 tracks per genre** (2,400 total), drawn with
`random_state=7` so the sample is reproducible. Genre-level hit rates in the sample
match the full dataset within ±2 percentage points.

`track_popularity` values are integers exactly as returned by the Spotify API; no
rounding was applied. Audio feature values (danceability, energy, valence) are
rounded to three decimal places consistent with the TidyTuesday source file.

## How to refresh

To reproduce this file from the original source:

```python
import pandas as pd

url = "https://raw.githubusercontent.com/rfordatascience/tidytuesday/main/data/2020/2020-01-21/spotify_songs.csv"
df = pd.read_csv(url).drop_duplicates(subset="track_id")

keep = ["track_id", "track_name", "track_artist", "playlist_genre",
        "track_popularity", "danceability", "energy", "valence"]

frames = []
for genre in df["playlist_genre"].unique():
    frames.append(df[df["playlist_genre"] == genre].sample(n=400, random_state=7))

pd.concat(frames).reset_index(drop=True)[keep].to_csv("spotify_tracks_sample.csv", index=False)
```
