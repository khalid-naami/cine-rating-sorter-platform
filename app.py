"""CineScore — Cinema, TV Series, Anime & Animation Rating Sorter Platform.

Comprehensive Multi-Source Rating Intelligence (IMDb, Rotten Tomatoes, Metacritic, MyAnimeList, Letterboxd).
Includes Top 100 Movies, Top 100 TV Series, Top 100 Anime, Top 100 Cartoons,
Top Animated Movies, and All-Time Hall of Fame Legendary Episodes.
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.movies_database import MASTER_MOVIES_DB
from src.series_database import MASTER_SERIES_DB, TOP_SERIES_EPISODES
from src.anime_database import MASTER_ANIME_DB, RAW_TOP_ANIME_MOVIES, TOP_ANIME_EPISODES
from src.cartoons_database import MASTER_CARTOONS_DB, RAW_TOP_ANIMATED_MOVIES, TOP_CARTOON_EPISODES
from src.master_catalog import MasterCatalog, FORMATTED_ANIME_MOVIES, FORMATTED_ANIMATED_MOVIES, HALL_OF_FAME_EPISODES
from src.rating_sorter_engine import RatingSorterEngine
from src.visualizer import (
    create_ratings_scatter_plot,
    create_cinescore_distribution_bar
)

# Page Configuration
st.set_page_config(
    page_title="CineScore — Cinema, Series, Anime & Animation Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cinema Dark Glassmorphism CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f59e0b, #ec4899, #38bdf8, #10b981);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-bottom: 0.8rem;
    }
    .live-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(16, 185, 129, 0.15);
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        color: #34d399;
        font-weight: 600;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.75);
        border: 1px solid rgba(245, 158, 11, 0.25);
        border-radius: 12px;
        padding: 1.1rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.6rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #f59e0b;
    }
    .movie-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1.2rem;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .movie-card:hover {
        border-color: #f59e0b;
        transform: translateY(-2px);
    }
    .cinescore-pill {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: #ffffff;
        font-weight: 800;
        font-size: 1.05rem;
        padding: 4px 12px;
        border-radius: 8px;
        display: inline-block;
    }
    .category-badge {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 8px;
        border-radius: 6px;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-movie { background: rgba(56, 189, 248, 0.2); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.4); }
    .badge-series { background: rgba(236, 72, 153, 0.2); color: #f472b6; border: 1px solid rgba(236, 72, 153, 0.4); }
    .badge-anime { background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4); }
    .badge-cartoon { background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.4); }
    .badge-episode { background: rgba(234, 179, 8, 0.2); color: #facc15; border: 1px solid rgba(234, 179, 8, 0.4); }
    .imdb-pill {
        background: #eab308;
        color: #000000;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .mal-pill {
        background: #2e51a2;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .rt-pill {
        background: #ef4444;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .meta-pill {
        background: #10b981;
        color: #ffffff;
        font-weight: 700;
        font-size: 0.85rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
    }
    .stream-tag {
        background: rgba(56, 189, 248, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(56, 189, 248, 0.3);
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar Configuration
st.sidebar.markdown("## 🌌 Media Universe Selector")
universe_categories = list(MasterCatalog.CATEGORY_MAP.keys())
chosen_category = st.sidebar.selectbox("Choose Media Category:", universe_categories, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Sorter & Filter Engine")

sort_options = [
    "CineScore (0-100)",
    "IMDb Rating (0-10)",
    "MyAnimeList (MAL Score)",
    "Rotten Tomatoes (%)",
    "Metacritic Score (0-100)",
    "Letterboxd (0-5)",
    "Release Year",
    "Box Office ($M)",
    "Runtime (Mins)",
    "Oscar Wins",
    "Seasons Count",
    "Episodes Count"
]
chosen_sort = st.sidebar.selectbox("Sort By:", sort_options, index=0)
sort_direction = st.sidebar.radio("Order:", ["Highest First (Descending ⬇️)", "Lowest First (Ascending ⬆️)"], index=0)
is_ascending = "Ascending" in sort_direction

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Precise Filters")

search_kw = st.sidebar.text_input("Search Title, Director, Creator, Studio:", value="", placeholder="e.g. Nolan, Gilligan, Ghibli, AOT...")

raw_items = MasterCatalog.get_items_by_category(chosen_category)
all_genres = ["All Genres"] + RatingSorterEngine.get_all_genres(raw_items)
chosen_genre = st.sidebar.selectbox("Genre Filter:", all_genres, index=0)

all_directors = ["All Directors / Creators"] + RatingSorterEngine.get_all_directors(raw_items)
chosen_director = st.sidebar.selectbox("Director / Studio / Creator:", all_directors, index=0)

all_services = ["All Platforms"] + RatingSorterEngine.get_all_streaming_services(raw_items)
chosen_service = st.sidebar.selectbox("Streaming Platform:", all_services, index=0)

min_imdb_val = st.sidebar.slider("Minimum IMDb Rating:", min_value=0.0, max_value=9.8, value=0.0, step=0.1)
year_range = st.sidebar.slider("Release Era (Years):", min_value=1930, max_value=2026, value=(1960, 2026))

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Live Telemetry & Auto-Refresh")
auto_refresh_enabled = st.sidebar.toggle("10s Auto-Refresh (Live Sync)", value=True)

refresh_counter = 0
if auto_refresh_enabled:
    refresh_counter = st_autorefresh(interval=10000, limit=None, key="cinescore_universe_refresh")

if st.sidebar.button("🔄 Refresh Catalog & Ratings", key="btn_refresh_universe"):
    st.rerun()

# Apply Engine Sorting & Filtering
filtered_items = RatingSorterEngine.filter_and_sort(
    items=raw_items,
    sort_by=chosen_sort,
    ascending=is_ascending,
    selected_genre=chosen_genre,
    selected_director=chosen_director,
    selected_service=chosen_service,
    min_imdb=min_imdb_val,
    min_year=year_range[0],
    max_year=year_range[1],
    search_query=search_kw
)

# Header Section
st.markdown('<div class="main-title">🎬 CineScore™ Universe — Cinema, Series, Anime & Animation Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Source Universal Analytics &bull; IMDb &bull; Rotten Tomatoes &bull; Metacritic &bull; MyAnimeList &bull; Letterboxd &bull; Hall of Fame Masterpiece Episodes</div>', unsafe_allow_html=True)

# Live Status Badge
now_utc_str = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
stats = MasterCatalog.get_summary_stats()
if auto_refresh_enabled:
    st.markdown(f'<div class="live-badge">🟢 LIVE TELEMETRY ACTIVE &bull; {stats["grand_total"]}+ Titles Indexed Across 7 Universes &bull; Synced: {now_utc_str} &bull; Cycle #{refresh_counter}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="live-badge" style="background:rgba(148,163,184,0.1); border-color:rgba(148,163,184,0.3); color:#94a3b8;">⏸️ LIVE SYNC PAUSED &bull; {stats["grand_total"]}+ Titles Indexed &bull; Synced: {now_utc_str}</div>', unsafe_allow_html=True)

# KPI Cards
top_title = (filtered_items[0].get("title") or filtered_items[0].get("episode_title") or "N/A") if filtered_items else "N/A"
max_imdb = max([m.get("imdb_rating", 0) for m in filtered_items]) if filtered_items else 0
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Matched Titles</div>
        <div class="metric-value">🎯 {len(filtered_items)}</div>
        <div class="metric-sub">{chosen_category}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">#1 Leader</div>
        <div class="metric-value" style="font-size:1.15rem;">🏆 {str(top_title)[:18]}</div>
        <div class="metric-sub">by {chosen_sort.split()[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Peak IMDb Score</div>
        <div class="metric-value">⭐ {max_imdb} / 10</div>
        <div class="metric-sub">Highest in Selection</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Catalog Size</div>
        <div class="metric-value">🌌 {stats['grand_total']}</div>
        <div class="metric-sub">Multi-Platform Database</div>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Hall of Fame Episodes</div>
        <div class="metric-value">👑 {stats['total_legendary_episodes']}</div>
        <div class="metric-sub">Rating 9.6 to 10.0 ⭐</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Interactive Tabs
tabs = st.tabs([
    "🌟 Universal Catalog & Cards",
    "🎬 Top 100 Movies",
    "📺 Top 100 TV Series",
    "🎌 Anime Universe",
    "🎨 Cartoons & Animation",
    "🏆 Hall of Fame Episodes (9.8 - 10.0)",
    "📋 Custom Bulk Sorter",
    "📊 Analytics & Plots",
    "💾 Data Export"
])

def render_media_card(item: dict, rank: int):
    title = item.get("title") or item.get("episode_title") or "Unknown"
    year = item.get("year") or item.get("start_year") or ""
    year_str = f"({year})" if year else ""
    cinescore = item.get("cinescore", round(item.get("imdb_rating", 8.0) * 10, 1))
    imdb = item.get("imdb_rating", "N/A")
    votes = item.get("imdb_votes", "")
    rt = item.get("rotten_tomatoes_pct")
    meta = item.get("metacritic_score")
    mal = item.get("mal_score")
    plot = item.get("plot") or item.get("synopsis") or "No plot synopsis available."
    director = item.get("director") or item.get("studio") or ", ".join(item.get("creators", [])) or "Various Creators"
    m_type = item.get("media_type", "movie")

    # Category Badge
    badge_class = "badge-movie"
    badge_text = "MOVIE"
    if m_type == "tv_series":
        badge_class = "badge-series"
        badge_text = "TV SERIES"
    elif m_type == "anime_series":
        badge_class = "badge-anime"
        badge_text = "ANIME SERIES"
    elif m_type == "anime_movie":
        badge_class = "badge-anime"
        badge_text = "ANIME MOVIE"
    elif m_type == "cartoon_series":
        badge_class = "badge-cartoon"
        badge_text = "CARTOON SERIES"
    elif m_type == "animated_movie":
        badge_class = "badge-cartoon"
        badge_text = "ANIMATED MOVIE"
    elif m_type == "legendary_episode":
        badge_class = "badge-episode"
        badge_text = f"EPISODE: {item.get('series_title', '')}"

    stream_tags = " ".join([f'<span class="stream-tag">{s}</span>' for s in item.get("streaming_services", [])])

    badges_html = f'<span class="imdb-pill">IMDb {imdb} ⭐</span>'
    if mal:
        badges_html += f'<span class="mal-pill">MAL {mal} 🎌</span>'
    if rt:
        badges_html += f'<span class="rt-pill">🍅 {rt}%</span>'
    if meta:
        badges_html += f'<span class="meta-pill">Ⓜ️ {meta}/100</span>'

    top_ep_info = ""
    if "top_episode" in item:
        top_ep_info = f"<div style='font-size:0.85rem; color:#facc15; margin-top:0.4rem;'>👑 <b>Highest Rated Episode:</b> {item['top_episode']}</div>"

    card_html = f"""
    <div class="movie-card">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">
            <div>
                <span style="color:#94a3b8; font-weight:700; font-size:1.05rem; margin-right:8px;">#{rank}</span>
                <span class="category-badge {badge_class}">{badge_text}</span>
                <span style="font-size:1.35rem; font-weight:800; color:#f8fafc;">{title}</span>
                <span style="color:#94a3b8; font-size:0.95rem; margin-left:6px;">{year_str}</span>
            </div>
            <div>
                <span class="cinescore-pill">CineScore: {cinescore}</span>
            </div>
        </div>
        <div style="margin-bottom:0.6rem;">
            {badges_html}
        </div>
        <p style="font-size:0.9rem; color:#cbd5e1; margin:0.4rem 0;">{plot}</p>
        {top_ep_info}
        <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; color:#94a3b8; margin-top:0.5rem; border-top:1px solid rgba(148,163,184,0.15); padding-top:0.5rem;">
            <div>
                <b>Director / Studio / Creators:</b> {director}
            </div>
            <div>
                {stream_tags}
            </div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)


# ----------------- TAB 1: Universal Cards -----------------
with tabs[0]:
    st.markdown(f"### 🌟 Universal Ranked Catalog — `{chosen_category}` (Sorted by `{chosen_sort}` {'Asc' if is_ascending else 'Desc'})")
    if not filtered_items:
        st.warning("No media found matching your filter criteria. Broaden your search.")
    else:
        for idx, item in enumerate(filtered_items[:100], 1):
            render_media_card(item, idx)

# ----------------- TAB 2: Top 100 Movies -----------------
with tabs[1]:
    st.markdown("### 🎬 All-Time Top 100 Greatest Cinema Masterpieces")
    df_movies = pd.DataFrame(MASTER_MOVIES_DB)
    st.dataframe(df_movies[[
        "rank_top100", "title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct",
        "metacritic_score", "letterboxd_rating", "director", "oscar_wins", "box_office_million"
    ]].rename(columns={
        "rank_top100": "Rank #", "title": "Title", "year": "Year", "cinescore": "CineScore",
        "imdb_rating": "IMDb ⭐", "rotten_tomatoes_pct": "RT 🍅", "metacritic_score": "Meta Ⓜ️",
        "letterboxd_rating": "Letterboxd", "director": "Director", "oscar_wins": "Oscars", "box_office_million": "Box Office ($M)"
    }), use_container_width=True, hide_index=True)

# ----------------- TAB 3: Top 100 Series -----------------
with tabs[2]:
    st.markdown("### 📺 Top 100 Television Series & Peak Rated Episodes")
    df_series = pd.DataFrame(MASTER_SERIES_DB)
    df_series["creators_str"] = df_series["creators"].apply(lambda c: ", ".join(c) if isinstance(c, list) else str(c))
    st.dataframe(df_series[[
        "rank_top100", "title", "start_year", "end_year", "cinescore", "imdb_rating", "rotten_tomatoes_pct",
        "metacritic_score", "seasons_count", "episodes_count", "creators_str", "top_episode"
    ]].rename(columns={
        "rank_top100": "Rank #", "title": "Series Title", "start_year": "Start", "end_year": "End",
        "cinescore": "CineScore", "imdb_rating": "IMDb ⭐", "rotten_tomatoes_pct": "RT 🍅",
        "metacritic_score": "Meta Ⓜ️", "seasons_count": "Seasons", "episodes_count": "Episodes",
        "creators_str": "Creators", "top_episode": "Highest Rated Episode"
    }), use_container_width=True, hide_index=True)

# ----------------- TAB 4: Anime Universe -----------------
with tabs[3]:
    st.markdown("### 🎌 Anime Universe — Top 100 Series & Masterpiece Anime Movies")
    an_sub1, an_sub2 = st.tabs(["📺 Top Anime Series (with MyAnimeList Scores)", "🎬 Top Anime Feature Films"])
    with an_sub1:
        df_anime = pd.DataFrame(MASTER_ANIME_DB)
        st.dataframe(df_anime[[
            "rank_top100", "title", "japanese_title", "year", "cinescore", "mal_score", "imdb_rating",
            "episodes_count", "studio", "top_episode"
        ]].rename(columns={
            "rank_top100": "Rank #", "title": "Anime Title", "japanese_title": "Original Title",
            "year": "Year", "cinescore": "CineScore", "mal_score": "MyAnimeList ⭐", "imdb_rating": "IMDb ⭐",
            "episodes_count": "Episodes", "studio": "Studio", "top_episode": "Peak Episode"
        }), use_container_width=True, hide_index=True)
    with an_sub2:
        df_an_movies = pd.DataFrame(RAW_TOP_ANIME_MOVIES)
        st.dataframe(df_an_movies[["title", "year", "director", "studio", "mal_score", "imdb_rating", "rotten_tomatoes_pct", "box_office_million"]].rename(columns={
            "title": "Anime Film", "year": "Year", "director": "Director", "studio": "Studio",
            "mal_score": "MAL Score", "imdb_rating": "IMDb ⭐", "rotten_tomatoes_pct": "RT 🍅", "box_office_million": "Box Office ($M)"
        }), use_container_width=True, hide_index=True)

# ----------------- TAB 5: Cartoons & Animation -----------------
with tabs[4]:
    st.markdown("### 🎨 Cartoons & Western Animation — Top Series & Feature Films")
    c_sub1, c_sub2 = st.tabs(["📺 Top 100 Cartoon Series", "🎬 Top 100 Animated Feature Films"])
    with c_sub1:
        df_cartoons = pd.DataFrame(MASTER_CARTOONS_DB)
        df_cartoons["creators_str"] = df_cartoons["creators"].apply(lambda c: ", ".join(c) if isinstance(c, list) else str(c))
        st.dataframe(df_cartoons[[
            "rank_top100", "title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct",
            "seasons_count", "episodes_count", "creators_str", "top_episode"
        ]].rename(columns={
            "rank_top100": "Rank #", "title": "Cartoon Series", "year": "Year", "cinescore": "CineScore",
            "imdb_rating": "IMDb ⭐", "rotten_tomatoes_pct": "RT 🍅", "seasons_count": "Seasons",
            "episodes_count": "Episodes", "creators_str": "Creators", "top_episode": "Peak Episode"
        }), use_container_width=True, hide_index=True)
    with c_sub2:
        df_an_feat = pd.DataFrame(RAW_TOP_ANIMATED_MOVIES)
        st.dataframe(df_an_feat[["title", "year", "studio", "director", "imdb_rating", "rotten_tomatoes_pct", "box_office_million", "oscar_wins"]].rename(columns={
            "title": "Animated Film", "year": "Year", "studio": "Studio", "director": "Director",
            "imdb_rating": "IMDb ⭐", "rotten_tomatoes_pct": "RT 🍅", "box_office_million": "Box Office ($M)", "oscar_wins": "Oscars"
        }), use_container_width=True, hide_index=True)

# ----------------- TAB 6: Hall of Fame Episodes -----------------
with tabs[5]:
    st.markdown("### 🏆 Hall of Fame — The Highest-Rated TV, Anime & Cartoon Episodes in History (9.8 - 10.0 ⭐)")
    st.markdown("Episodes that achieved legendary critical consensus and near-perfect IMDb ratings.")

    df_hof = pd.DataFrame(HALL_OF_FAME_EPISODES)
    st.dataframe(df_hof[[
        "series_title", "episode_title", "category", "season", "episode_number", "imdb_rating", "imdb_votes", "plot"
    ]].rename(columns={
        "series_title": "Show / Franchise", "episode_title": "Legendary Episode Title", "category": "Format",
        "season": "Season", "episode_number": "Episode #", "imdb_rating": "IMDb Score ⭐",
        "imdb_votes": "Votes", "plot": "Episode Synopsis"
    }), use_container_width=True, hide_index=True)

# ----------------- TAB 7: Custom Bulk Sorter -----------------
with tabs[6]:
    st.markdown("### 📋 Bulk Media List Sorter (Supports Movies, Series, Anime & Cartoons)")
    st.markdown("Paste any list of titles below (one per line). The engine will match ratings across the entire media universe.")

    default_sample = """Breaking Bad
Ozymandias
Attack on Titan
Spirited Away
The Dark Knight
Avatar: The Last Airbender
Sozin's Comet
Arcane
Succession
Fullmetal Alchemist: Brotherhood"""

    user_text_input = st.text_area("Paste Media Titles List:", value=default_sample, height=220)

    if st.button("🚀 Sort My List by Multi-Source Ratings", key="btn_sort_universe_custom"):
        parsed_results = RatingSorterEngine.parse_user_raw_list(user_text_input)
        st.success(f"Successfully matched and sorted {len(parsed_results)} items across the universe!")
        df_parsed = pd.DataFrame(parsed_results)
        st.dataframe(df_parsed[["title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct", "director", "plot"]].rename(columns={
            "title": "Title", "year": "Year", "cinescore": "CineScore", "imdb_rating": "IMDb ⭐",
            "rotten_tomatoes_pct": "RT 🍅", "director": "Director / Creators", "plot": "Synopsis"
        }), use_container_width=True, hide_index=True)

# ----------------- TAB 8: Analytics -----------------
with tabs[7]:
    st.markdown("### 📊 Cross-Media Rating Correlations & Distribution")
    plot_items = [item for item in filtered_items if "rotten_tomatoes_pct" in item and "box_office_million" in item]
    if plot_items:
        st.plotly_chart(create_ratings_scatter_plot(plot_items), use_container_width=True)
    st.plotly_chart(create_cinescore_distribution_bar(filtered_items[:15], top_n=15), use_container_width=True)

# ----------------- TAB 9: Export -----------------
with tabs[8]:
    st.markdown("### 💾 Export Universal Data & Watchlists")
    df_exp = pd.DataFrame(filtered_items)
    if not df_exp.empty:
        csv_data = df_exp.to_csv(index=False)
        json_data = df_exp.to_json(orient="records", indent=2)

        ec1, ec2 = st.columns(2)
        with ec1:
            st.download_button(
                label=f"📥 Download {chosen_category} as CSV",
                data=csv_data,
                file_name=f"cinescore_{chosen_category.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
        with ec2:
            st.download_button(
                label="📥 Download Full Dataset as JSON",
                data=json_data,
                file_name="cinescore_universe.json",
                mime="application/json"
            )

        st.markdown("#### 📝 Markdown Watchlist Checklist:")
        checklist_lines = []
        for it in filtered_items[:30]:
            t = it.get("title") or it.get("episode_title") or "Unknown"
            y = it.get("year") or it.get("start_year") or ""
            c_score = it.get("cinescore", 80)
            checklist_lines.append(f"- [ ] **{t}** {f'({y})' if y else ''} — CineScore: `{c_score}` | IMDb: ⭐ `{it.get('imdb_rating')}`")
        st.code("\n".join(checklist_lines), language="markdown")
