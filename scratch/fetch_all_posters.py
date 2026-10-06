import os
import sys
import json
import time
import urllib.request
import urllib.parse
from typing import Dict, Optional

# Add project root to path
sys.path.insert(0, os.path.abspath("."))

from src.movies_database import MASTER_MOVIES_DB
from src.series_database import MASTER_SERIES_DB, TOP_SERIES_EPISODES
from src.anime_database import MASTER_ANIME_DB, RAW_TOP_ANIME_MOVIES, TOP_ANIME_EPISODES
from src.cartoons_database import MASTER_CARTOONS_DB, RAW_TOP_ANIMATED_MOVIES, TOP_CARTOON_EPISODES
from src.posters_data import POSTERS_CATALOG

def search_tvmaze(query: str) -> Optional[str]:
    try:
        url = 'https://api.tvmaze.com/singlesearch/shows?' + urllib.parse.urlencode({'q': query})
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            img = data.get('image', {})
            return img.get('medium') or img.get('original')
    except Exception:
        return None

def search_itunes(query: str, entity: str = 'movie') -> Optional[str]:
    try:
        url = 'https://itunes.apple.com/search?' + urllib.parse.urlencode({'term': query, 'entity': entity, 'limit': 1})
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            if data.get('resultCount', 0) > 0:
                artwork = data['results'][0].get('artworkUrl100', '')
                if artwork:
                    return artwork.replace('100x100bb.jpg', '600x600bb.jpg')
    except Exception:
        pass
    return None

def search_itunes_all(query: str) -> Optional[str]:
    try:
        url = 'https://itunes.apple.com/search?' + urllib.parse.urlencode({'term': query, 'limit': 1})
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            if data.get('resultCount', 0) > 0:
                artwork = data['results'][0].get('artworkUrl100', '')
                if artwork:
                    return artwork.replace('100x100bb.jpg', '600x600bb.jpg')
    except Exception:
        pass
    return None

def search_wikipedia(query: str) -> Optional[str]:
    try:
        url = 'https://en.wikipedia.org/api/rest_v1/page/summary/' + urllib.parse.quote(query.replace(' ', '_'))
        req = urllib.request.Request(url, headers={'User-Agent': 'CineScoreApp/2.0 (contact@naami.me)'})
        with urllib.request.urlopen(req, timeout=6) as res:
            data = json.loads(res.read().decode('utf-8'))
            thumb = data.get('thumbnail', {})
            if thumb and thumb.get('source'):
                return thumb.get('source')
    except Exception:
        pass
    return None

def check_url_valid(url: str) -> bool:
    if not url: return False
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
        with urllib.request.urlopen(req, timeout=5) as res:
            return res.status == 200
    except Exception:
        return False

# Collect all titles
titles_with_type = []
for m in MASTER_MOVIES_DB: titles_with_type.append((m['title'], 'movie'))
for s in MASTER_SERIES_DB: titles_with_type.append((s['title'], 'tv_series'))
for a in MASTER_ANIME_DB: titles_with_type.append((a['title'], 'anime_series'))
for c in MASTER_CARTOONS_DB: titles_with_type.append((c['title'], 'cartoon_series'))
for am in RAW_TOP_ANIME_MOVIES: titles_with_type.append((am['title'], 'anime_movie'))
for wm in RAW_TOP_ANIMATED_MOVIES: titles_with_type.append((wm['title'], 'animated_movie'))
for ep in TOP_SERIES_EPISODES + TOP_ANIME_EPISODES + TOP_CARTOON_EPISODES:
    titles_with_type.append((ep['series_title'], 'tv_series'))
    titles_with_type.append((ep['episode_title'], 'legendary_episode'))

new_catalog = dict(POSTERS_CATALOG)
resolved_count = 0
failed_titles = []

print(f"Starting resolution. Existing catalog entries: {len(new_catalog)}")

for title, m_type in titles_with_type:
    if title in new_catalog and new_catalog[title]:
        continue

    print(f"Resolving: {title} ({m_type})...")
    found_url = None

    # Priority 1: TVMaze for TV shows, anime series, cartoons
    if m_type in ('tv_series', 'anime_series', 'cartoon_series'):
        found_url = search_tvmaze(title)
        if not found_url:
            clean_t = title.split('(')[0].split(':')[0].strip()
            found_url = search_tvmaze(clean_t)

    # Priority 2: iTunes
    if not found_url:
        if m_type in ('movie', 'anime_movie', 'animated_movie'):
            found_url = search_itunes(title, entity='movie')
        else:
            found_url = search_itunes(title, entity='tvSeason') or search_itunes(title, entity='all')

    # Priority 3: Wikipedia
    if not found_url:
        found_url = search_wikipedia(title)
        if not found_url:
            clean_t = title.split('(')[0].strip()
            found_url = search_wikipedia(clean_t) or search_wikipedia(f"{clean_t} (film)") or search_wikipedia(f"{clean_t} (TV series)") or search_wikipedia(f"{clean_t} (anime)")

    # Fallback to iTunes broad search
    if not found_url:
        clean_t = title.split('(')[0].strip()
        found_url = search_itunes_all(clean_t)

    if found_url:
        print(f"  -> Found: {found_url[:70]}...")
        new_catalog[title] = found_url
        resolved_count += 1
    else:
        print(f"  -> FAILED to find poster for: {title}")
        failed_titles.append(title)

    time.sleep(0.1)

print(f"\nFinished! Newly resolved: {resolved_count}, Failed: {len(failed_titles)}, Total in catalog: {len(new_catalog)}")

# Save to posters_data_full.json
with open("scratch/posters_data_full.json", "w", encoding="utf-8") as f:
    json.dump(new_catalog, f, indent=4, ensure_ascii=False)

print("Saved to scratch/posters_data_full.json")
