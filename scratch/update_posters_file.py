import json

with open('scratch/posters_data_full.json', 'r', encoding='utf-8') as f:
    full_catalog = json.load(f)

header = '''"""Comprehensive Poster Image Catalog and Resolver for CineScore Universe.

Contains direct, high-fidelity poster URLs from official CDNs (TMDb, TVmaze, Apple iTunes, Wikimedia)
covering all 326+ Movies, TV Series, Anime, Cartoons, and Legendary Masterpiece Episodes.
"""

from typing import Dict, Any

# Direct Official Verified Poster URLs (326+ Titles)
POSTERS_CATALOG: Dict[str, str] = '''

footer = '''

# Reliable High-Res Fallbacks based on Media Type
CATEGORY_FALLBACKS: Dict[str, str] = {
    "movie": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=500&q=80",
    "tv_series": "https://images.unsplash.com/photo-1522869635100-9f4c5e86aa37?w=500&q=80",
    "anime_series": "https://images.unsplash.com/photo-1578632767115-351597cf2477?w=500&q=80",
    "anime_movie": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=500&q=80",
    "cartoon_series": "https://images.unsplash.com/photo-1563089145-599997674d42?w=500&q=80",
    "animated_movie": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=500&q=80",
    "legendary_episode": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80"
}

def get_media_poster(item: Dict[str, Any]) -> str:
    """Resolves the best poster image URL for any title or episode."""
    if item.get("poster_url"):
        return item["poster_url"]

    title = item.get("title") or item.get("episode_title") or ""
    series_title = item.get("series_title", "")
    media_type = item.get("media_type", "movie")

    # 1. Exact Title Match
    if title in POSTERS_CATALOG:
        return POSTERS_CATALOG[title]

    # 2. Check Parent Series for Episodes
    if series_title and series_title in POSTERS_CATALOG:
        return POSTERS_CATALOG[series_title]

    # 3. Substring matching
    title_lower = title.lower()
    for cat_title, url in POSTERS_CATALOG.items():
        if cat_title.lower() in title_lower or title_lower in cat_title.lower():
            return url

    # 4. Graceful category-specific HD banner fallback
    return CATEGORY_FALLBACKS.get(media_type, CATEGORY_FALLBACKS["movie"])
'''

with open('src/posters_data.py', 'w', encoding='utf-8') as f:
    f.write(header + json.dumps(full_catalog, indent=4, ensure_ascii=False) + footer)

print(f"Successfully wrote {len(full_catalog)} posters to src/posters_data.py")
