"""CineScore — Cinema Rating Sorter & Film Intelligence Platform.

Inspired by DidierRLopes/SortMoviesPerRating. Multi-source ratings (IMDb, Rotten Tomatoes,
Metacritic, Letterboxd), bulk user list sorting, director/genre filters, and streaming platforms.
"""

import datetime
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_autorefresh import st_autorefresh

from src.movies_database import MASTER_MOVIES_DB
from src.rating_sorter_engine import RatingSorterEngine
from src.visualizer import (
    create_ratings_scatter_plot,
    create_cinescore_distribution_bar
)

# Page Setup
st.set_page_config(
    page_title="CineScore — Movie Rating Sorter & Film Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cinema Dark Glassmorphism CSS
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #f59e0b, #ec4899, #38bdf8);
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
        padding: 1.2rem;
        text-align: center;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #f8fafc;
        margin: 0.3rem 0;
    }
    .metric-sub {
        font-size: 0.8rem;
        color: #f59e0b;
    }
    .movie-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 12px;
        padding: 1.3rem;
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
        font-size: 1.1rem;
        padding: 4px 12px;
        border-radius: 8px;
        display: inline-block;
    }
    .imdb-pill {
        background: #eab308;
        color: #000000;
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

# Sidebar Controls
st.sidebar.markdown("## 🎯 Sorter & Filter Engine")

# Sort Criterion
sort_options = [
    "CineScore (0-100)",
    "IMDb Rating (0-10)",
    "Rotten Tomatoes (%)",
    "Metacritic Score (0-100)",
    "Letterboxd (0-5)",
    "Release Year",
    "Box Office ($M)",
    "Runtime (Mins)",
    "Oscar Wins"
]
chosen_sort = st.sidebar.selectbox("Sort Movies By:", sort_options, index=0)
sort_direction = st.sidebar.radio("Order:", ["Highest First (Descending ⬇️)", "Lowest First (Ascending ⬆️)"], index=0)
is_ascending = "Ascending" in sort_direction

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Precise Filters")

search_kw = st.sidebar.text_input("Search Title, Director, or Actor:", value="", placeholder="e.g. Nolan, DiCaprio, Dune...")

all_genres = ["All Genres"] + RatingSorterEngine.get_all_genres()
chosen_genre = st.sidebar.selectbox("Genre Filter:", all_genres, index=0)

all_directors = ["All Directors"] + RatingSorterEngine.get_all_directors()
chosen_director = st.sidebar.selectbox("Director Filter:", all_directors, index=0)

all_services = ["All Platforms"] + RatingSorterEngine.get_all_streaming_services()
chosen_service = st.sidebar.selectbox("Streaming Platform:", all_services, index=0)

min_imdb_val = st.sidebar.slider("Minimum IMDb Rating:", min_value=0.0, max_value=9.5, value=0.0, step=0.1)
year_range = st.sidebar.slider("Release Era (Years):", min_value=1950, max_value=2026, value=(1970, 2026))

# 10s Live Auto-Refresh
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔄 Live Telemetry & Auto-Refresh")
auto_refresh_enabled = st.sidebar.toggle("10s Auto-Refresh (Live Sync)", value=True)
refresh_counter = 0
if auto_refresh_enabled:
    refresh_counter = st_autorefresh(interval=10000, limit=None, key="cinescore_auto_refresh_10s")

if st.sidebar.button("🔄 Refresh Catalog & Ratings", key="btn_refresh_cinema"):
    st.rerun()

# Apply Filters & Sorting
filtered_movies = RatingSorterEngine.filter_and_sort(
    movies=MASTER_MOVIES_DB,
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

# Main Header
st.markdown('<div class="main-title">🎬 CineScore™ — Cinema Rating Sorter & Film Intelligence</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Source Rating Intelligence (IMDb &bull; Rotten Tomatoes &bull; Metacritic &bull; Letterboxd) | Custom Bulk List Sorter | Streaming Availability</div>', unsafe_allow_html=True)

# Live Status Badge
now_utc_str = datetime.datetime.utcnow().strftime("%H:%M:%S UTC")
if auto_refresh_enabled:
    st.markdown(f'<div class="live-badge">🟢 LIVE CINEMA TELEMETRY ACTIVE &bull; Auto-Refreshing every 10s &bull; Last Synced: {now_utc_str} &bull; Cycle #{refresh_counter}</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div class="live-badge" style="background:rgba(148,163,184,0.1); border-color:rgba(148,163,184,0.3); color:#94a3b8;">⏸️ LIVE SYNC PAUSED &bull; Last Synced: {now_utc_str}</div>', unsafe_allow_html=True)

# Top KPI Metric Cards
top_film = filtered_movies[0]["title"] if filtered_movies else "N/A"
max_imdb = max([m["imdb_rating"] for m in filtered_movies]) if filtered_movies else 0
max_rt = max([m["rotten_tomatoes_pct"] for m in filtered_movies]) if filtered_movies else 0
tot_oscars = sum([m.get("oscar_wins", 0) for m in filtered_movies])

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Films Matched</div>
        <div class="metric-value">🎥 {len(filtered_movies)}</div>
        <div class="metric-sub">Active Filters</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">#1 Ranked Film</div>
        <div class="metric-value" style="font-size:1.1rem;">🏆 {top_film[:18]}</div>
        <div class="metric-sub">by {chosen_sort.split()[0]}</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Peak IMDb Score</div>
        <div class="metric-value">⭐ {max_imdb} / 10</div>
        <div class="metric-sub">Highest in Selection</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Peak Rotten Tomatoes</div>
        <div class="metric-value">🍅 {max_rt}%</div>
        <div class="metric-sub">Top Critics Score</div>
    </div>
    """, unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Oscar Wins</div>
        <div class="metric-value">🏆 {tot_oscars}</div>
        <div class="metric-sub">Academy Awards</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs (5 Core Modules)
tabs = st.tabs([
    "🎞️ Sorted Cinema Cards & Catalog",
    "⭐ All-Time Top 100 Greatest Movies",
    "📋 Custom Bulk List Sorter (DidierRLopes Style)",
    "📊 Rating Correlation & Analytics",
    "💾 Export & Watchlist Manager"
])

# ----------------- TAB 1: Movie Cards -----------------
with tabs[0]:
    st.markdown(f"### 🎞️ Ranked Cinema Masterpieces — Sorted by `{chosen_sort}` ({'Ascending' if is_ascending else 'Descending'})")

    if not filtered_movies:
        st.warning("No films match the specified filter combination. Please broaden your search criteria.")
    else:
        for idx, m in enumerate(filtered_movies, 1):
            stream_html = " ".join([f'<span class="stream-tag">{s}</span>' for s in m.get("streaming_services", [])])
            genres_html = " &bull; ".join(m.get("genres", []))
            cast_html = ", ".join(m.get("cast", [])[:3])

            st.markdown(f"""
            <div class="movie-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                    <div>
                        <span style="color:#94a3b8; font-weight:700; font-size:1.1rem; margin-right:8px;">#{idx}</span>
                        <span style="font-size:1.4rem; font-weight:800; color:#f8fafc;">{m['title']}</span>
                        <span style="color:#94a3b8; font-size:1.0rem; margin-left:6px;">({m['year']})</span>
                    </div>
                    <div>
                        <span class="cinescore-pill">CineScore: {m['cinescore']}</span>
                    </div>
                </div>
                <div style="margin-bottom:0.7rem;">
                    <span class="imdb-pill">IMDb {m['imdb_rating']} ⭐ ({m['imdb_votes']})</span>
                    <span class="rt-pill">🍅 {m['rotten_tomatoes_pct']}%</span>
                    <span class="meta-pill">Ⓜ️ {m['metacritic_score']}/100</span>
                    <span style="background:#00e054; color:#000000; font-weight:700; font-size:0.85rem; padding:3px 8px; border-radius:4px;">Letterboxd {m['letterboxd_rating']} / 5</span>
                </div>
                <p style="font-size:0.9rem; color:#cbd5e1; margin:0.4rem 0;">{m['plot']}</p>
                <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.85rem; color:#94a3b8; margin-top:0.6rem; border-top:1px solid rgba(148,163,184,0.15); padding-top:0.6rem;">
                    <div>
                        <b>🎬 Director:</b> {m['director']} &bull; <b>🎭 Cast:</b> {cast_html} &bull; <b>⏱️ Runtime:</b> {m['runtime_mins']} min
                    </div>
                    <div>
                        <b>💰 Box Office:</b> ${m['box_office_million']}M &bull; <b>🏆 Oscars:</b> {m['oscar_wins']} wins
                    </div>
                </div>
                <div style="margin-top:0.6rem;">
                    <span style="font-size:0.8rem; color:#94a3b8; margin-right:6px;">Available on:</span> {stream_html}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- TAB 2: Top 100 Hall of Fame -----------------
with tabs[1]:
    st.markdown("### ⭐ All-Time Top 100 Greatest Cinema Masterpieces (IMDb & Critical Consensus)")
    st.markdown("The complete, definitive 100 highest-rated films in cinema history with multi-source ratings, release years, directors, and box office figures.")

    t100_search = st.text_input("🔍 Quick Filter within Top 100:", value="", placeholder="e.g. Godfather, Nolan, Tarantino, Hitchcock...")

    df_top100 = pd.DataFrame(MASTER_MOVIES_DB)
    if t100_search:
        q100 = t100_search.lower().strip()
        df_top100 = df_top100[
            df_top100["title"].str.lower().str.contains(q100) |
            df_top100["director"].str.lower().str.contains(q100) |
            df_top100["genres"].apply(lambda g: any(q100 in str(x).lower() for x in g))
        ]

    df_top100["genres_display"] = df_top100["genres"].apply(lambda g: ", ".join(g) if isinstance(g, list) else str(g))

    st.dataframe(df_top100[[
        "rank_top100", "title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct", 
        "metacritic_score", "letterboxd_rating", "director", "genres_display", "oscar_wins", "box_office_million"
    ]].rename(columns={
        "rank_top100": "All-Time #",
        "title": "Film Title",
        "year": "Year",
        "cinescore": "CineScore™ (0-100)",
        "imdb_rating": "IMDb ⭐",
        "rotten_tomatoes_pct": "Rotten Tomatoes 🍅",
        "metacritic_score": "Metacritic Ⓜ️",
        "letterboxd_rating": "Letterboxd 🟩",
        "director": "Director",
        "genres_display": "Genres",
        "oscar_wins": "Oscars 🏆",
        "box_office_million": "Box Office ($M)"
    }), use_container_width=True, hide_index=True)

# ----------------- TAB 3: Custom Bulk Sorter -----------------
with tabs[2]:
    st.markdown("### 📋 Bulk Movie List Sorter (DidierRLopes / SortMoviesPerRating Tool)")
    st.markdown("Paste any list of raw movie titles below (one per line, with or without years). The engine will automatically match their multi-source ratings and output a ranked table.")

    default_user_sample = """Inception
The Godfather (1972)
Interstellar
Dune: Part Two
Pulp Fiction
Oppenheimer
The Dark Knight
Spirited Away
Fight Club
Whiplash"""

    user_text_input = st.text_area("Paste Movie Titles List:", value=default_user_sample, height=200)

    if st.button("🚀 Sort My Movie List by Rating Now", key="btn_sort_custom"):
        parsed_results = RatingSorterEngine.parse_user_raw_list(user_text_input)

        st.success(f"Successfully matched and sorted {len(parsed_results)} films by CineScore™ & IMDb Rating!")
        
        df_parsed = pd.DataFrame(parsed_results)
        st.dataframe(df_parsed[["title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct", "metacritic_score", "director", "runtime_mins", "box_office_million"]].rename(columns={
            "title": "Movie Title",
            "year": "Year",
            "cinescore": "CineScore™ (0-100)",
            "imdb_rating": "IMDb ⭐",
            "rotten_tomatoes_pct": "Rotten Tomatoes 🍅",
            "metacritic_score": "Metacritic Ⓜ️",
            "director": "Director",
            "runtime_mins": "Runtime (m)",
            "box_office_million": "Box Office ($M)"
        }), use_container_width=True, hide_index=True)

# ----------------- TAB 4: Analytics & Correlation -----------------
with tabs[3]:
    st.markdown("### 📊 Rating Correlation & Box Office Dynamics")
    
    st.plotly_chart(create_ratings_scatter_plot(filtered_movies), use_container_width=True)

    st.markdown("---")
    st.plotly_chart(create_cinescore_distribution_bar(filtered_movies, top_n=10), use_container_width=True)

# ----------------- TAB 5: Export & Watchlist -----------------
with tabs[4]:
    st.markdown("### 💾 Export Sorted Filmography & Watchlist")
    
    df_export = pd.DataFrame(filtered_movies)
    if not df_export.empty:
        csv_data = df_export[["title", "year", "cinescore", "imdb_rating", "rotten_tomatoes_pct", "metacritic_score", "director", "runtime_mins", "box_office_million"]].to_csv(index=False)
        json_data = df_export.to_json(orient="records", indent=2)

        ec1, ec2 = st.columns(2)
        with ec1:
            st.download_button(
                label="📥 Download Sorted Movies as CSV",
                data=csv_data,
                file_name=f"cinescore_sorted_{chosen_sort.lower().replace(' ', '_')}.csv",
                mime="text/csv"
            )
        with ec2:
            st.download_button(
                label="📥 Download Full Dataset as JSON",
                data=json_data,
                file_name="cinescore_dataset.json",
                mime="application/json"
            )

        st.markdown("#### 📝 Markdown Checklist Preview:")
        md_checklist = "\n".join([f"- [ ] **{m['title']}** ({m['year']}) — CineScore: `{m['cinescore']}` | IMDb: ⭐ `{m['imdb_rating']}` | Directed by {m['director']}" for m in filtered_movies])
        st.code(md_checklist, language="markdown")
