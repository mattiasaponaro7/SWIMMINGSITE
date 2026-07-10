import re
import random
import unicodedata
from difflib import get_close_matches
from pathlib import Path
from urllib.parse import quote

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st



# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Swim Records Explorer",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

px.defaults.template = "plotly_white"


# ============================================================
# FILE PATHS
# ============================================================

TOP_FILE = Path("Swimming_database_REAL.xlsx")
WR_FILE = Path("world_records_swimming.xlsx")


# ============================================================
# COLORS
# ============================================================

NAVY = "#052B44"
BLUE = "#0A6C9F"
AQUA = "#22B8CF"
LIGHT_AQUA = "#E8F8FB"
GOLD = "#D6A937"
GREY = "#D9E2EC"
DARK_GREY = "#52616B"
RED = "#D64545"

COURSE_COLORS = {
    "LC": BLUE,
    "SC": AQUA
}

GENDER_COLORS = {
    "Men": BLUE,
    "Women": "#C65BAA",
    "Mixed": GOLD,
    "Unknown": DARK_GREY
}


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
    <style>
.stApp {
    background-color: #F7FBFD;
    color: #052B44;
}

.main {
    background-color: #F7FBFD;
    color: #052B44;
}

[data-testid="stAppViewContainer"] {
    background-color: #F7FBFD;
    color: #052B44;
}

[data-testid="stMarkdownContainer"] {
    color: #052B44;
}

    .hero {
        padding: 34px 38px;
        border-radius: 24px;
        background: linear-gradient(135deg, #052B44 0%, #0A6C9F 48%, #22B8CF 100%);
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 10px 30px rgba(5,43,68,0.18);
    }

    .hero h1 {
        font-size: 52px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .hero p {
        font-size: 19px;
        opacity: 0.95;
        max-width: 950px;
        line-height: 1.45;
    }

    .section-title {
        color: #052B44;
        font-size: 28px;
        font-weight: 800;
        margin-top: 12px;
        margin-bottom: 6px;
    }

    .section-subtitle {
        color: #52616B;
        font-size: 16px;
        margin-bottom: 18px;
        line-height: 1.45;
    }

    .kpi-card {
        background-color: white;
        padding: 22px 22px;
        border-radius: 20px;
        border: 1px solid #E4EEF3;
        box-shadow: 0 6px 20px rgba(5,43,68,0.06);
        min-height: 130px;
    }

    .kpi-label {
        font-size: 13px;
        text-transform: uppercase;
        color: #52616B;
        font-weight: 700;
        letter-spacing: 0.06em;
    }

    .kpi-value {
        font-size: 34px;
        color: #052B44;
        font-weight: 850;
        margin-top: 8px;
    }

    .kpi-note {
        font-size: 13px;
        color: #52616B;
        margin-top: 5px;
    }

    .info-box {
        background-color: white;
        color: #052B44;
        border-left: 6px solid #22B8CF;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 16px 0;
        box-shadow: 0 6px 20px rgba(5,43,68,0.05);
}

    .info-box b {
        color: #052B44;
}

    .warning-box {
        background-color: #FFF8E6;
        color: #052B44;
        border-left: 6px solid #D6A937;
        border-radius: 16px;
        padding: 18px 20px;
        margin: 16px 0;
}

    .warning-box b {
        color: #052B44;
}

    .small-caption {
        font-size: 13px;
        color: #52616B;
        line-height: 1.4;
    }

    div[data-testid="stMetricValue"] {
        color: #052B44;
    }

    div[data-testid="stSidebar"] {
        background-color: #EFF8FB;
    }

    /* ============================================================
       TOP NAVIGATION - OLYMPIC SWIMMING POOL
    ============================================================ */

    .block-container {
        padding-top: 1.2rem;
    }

    .pool-nav-shell {
        position: sticky;
        top: 0;
        z-index: 999;
        background: rgba(247, 251, 253, 0.92);
        backdrop-filter: blur(16px);
        border: 1px solid #D8ECF4;
        border-radius: 26px;
        padding: 18px 20px 20px 20px;
        margin-bottom: 28px;
        box-shadow: 0 12px 34px rgba(5,43,68,0.10);
    }

    .pool-nav-top {
        display: flex;
        justify-content: space-between;
        align-items: end;
        gap: 16px;
        margin-bottom: 14px;
    }

    .pool-brand {
        color: #052B44;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.03em;
        line-height: 1.05;
    }

    .pool-subtitle {
        color: #52616B;
        font-size: 13px;
        font-weight: 650;
        text-align: right;
        max-width: 420px;
        line-height: 1.35;
    }

    .pool-grid {
        display: grid;
        grid-template-columns: repeat(8, minmax(86px, 1fr));
        gap: 9px;
    }

    .pool-lane {
        position: relative;
        display: flex;
        flex-direction: column;
        justify-content: end;
        min-height: 104px;
        padding: 12px 10px;
        border-radius: 18px;
        overflow: hidden;
        text-decoration: none !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.72);
        box-shadow:
            inset 3px 0 0 rgba(255,255,255,0.70),
            inset -3px 0 0 rgba(255,255,255,0.70),
            0 8px 18px rgba(5,43,68,0.10);
        background:
            linear-gradient(90deg,
                rgba(255,255,255,0.72) 0px,
                rgba(255,255,255,0.72) 2px,
                transparent 2px,
                transparent calc(100% - 2px),
                rgba(255,255,255,0.72) calc(100% - 2px),
                rgba(255,255,255,0.72) 100%
            ),
            radial-gradient(circle at 18% 22%, rgba(255,255,255,0.35) 0 2px, transparent 3px 15px),
            radial-gradient(circle at 70% 38%, rgba(255,255,255,0.25) 0 2px, transparent 3px 18px),
            linear-gradient(180deg, #6EDAF0 0%, #21A7D0 48%, #087CAD 100%);
        background-size: 100% 100%, 32px 24px, 38px 29px, 100% 100%;
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    }

    .pool-lane::before {
        content: "";
        position: absolute;
        inset: 0;
        z-index: 1;
        background:
            linear-gradient(180deg,
                rgba(5,43,68,0.88) 0%,
                rgba(10,108,159,0.75) 52%,
                rgba(34,184,207,0.58) 100%
            );
        transform: scaleY(0);
        transform-origin: top;
        transition: transform 0.34s ease;
    }

    .pool-lane::after {
        content: "🏊";
        position: absolute;
        top: 6px;
        left: 50%;
        z-index: 3;
        font-size: 25px;
        opacity: 0;
        transform: translateX(-50%) translateY(-35px) rotate(90deg);
        transition:
            transform 0.58s cubic-bezier(.2,.85,.2,1),
            opacity 0.18s ease;
        filter: drop-shadow(0 4px 6px rgba(5,43,68,0.35));
    }

    .pool-lane:hover {
        transform: translateY(-4px);
        border-color: #FFFFFF;
        box-shadow:
            inset 3px 0 0 rgba(255,255,255,0.86),
            inset -3px 0 0 rgba(255,255,255,0.86),
            0 16px 32px rgba(5,43,68,0.20);
    }

    .pool-lane:hover::before {
        transform: scaleY(1);
    }

    .pool-lane:hover::after {
        opacity: 1;
        transform: translateX(-50%) translateY(56px) rotate(90deg);
    }

    .pool-lane.active {
        border: 2px solid #D6A937;
        box-shadow:
            inset 3px 0 0 rgba(255,255,255,0.90),
            inset -3px 0 0 rgba(255,255,255,0.90),
            0 16px 34px rgba(214,169,55,0.28);
    }

    .pool-lane.active::before {
        transform: scaleY(1);
        background:
            linear-gradient(180deg,
                rgba(5,43,68,0.94) 0%,
                rgba(10,108,159,0.84) 55%,
                rgba(214,169,55,0.68) 100%
            );
    }

    .pool-lane.active::after {
        content: "🏊";
        opacity: 1;
        transform: translateX(-50%) translateY(56px) rotate(90deg);
    }

    .lane-number,
    .lane-label,
    .lane-tag {
        position: relative;
        z-index: 2;
        display: block;
        text-shadow: 0 2px 8px rgba(5,43,68,0.34);
    }

    .lane-number {
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        opacity: 0.88;
        margin-bottom: 4px;
    }

    .lane-label {
        font-size: 15px;
        font-weight: 900;
        line-height: 1.05;
    }

    .lane-tag {
        font-size: 10.5px;
        font-weight: 650;
        opacity: 0.86;
        margin-top: 5px;
        line-height: 1.15;
    }

    .current-lane {
        margin-top: 12px;
        color: #52616B;
        font-size: 13px;
        text-align: center;
        font-weight: 600;
    }

    .current-lane b {
        color: #052B44;
    }

    @media (max-width: 1150px) {
        .pool-grid {
            grid-template-columns: repeat(4, minmax(120px, 1fr));
        }

        .pool-lane {
            min-height: 92px;
        }
    }

    @media (max-width: 650px) {
        .pool-nav-top {
            flex-direction: column;
            align-items: flex-start;
        }

        .pool-subtitle {
            text-align: left;
        }

        .pool-grid {
            grid-template-columns: repeat(2, minmax(120px, 1fr));
        }
    }
    
/* ============================================================
   SWIM RECORD TOE - GAME STYLE
============================================================ */

.game-hero {
    padding: 34px 38px;
    border-radius: 28px;
    background:
        radial-gradient(circle at 15% 18%, rgba(255,255,255,0.36) 0 3px, transparent 4px 28px),
        radial-gradient(circle at 72% 35%, rgba(255,255,255,0.26) 0 3px, transparent 4px 30px),
        linear-gradient(135deg, #052B44 0%, #087CAD 48%, #22B8CF 100%);
    color: white;
    margin-bottom: 26px;
    box-shadow: 0 12px 34px rgba(5,43,68,0.18);
}

.game-hero h1 {
    font-size: 48px;
    font-weight: 900;
    margin-bottom: 8px;
}

.game-hero p {
    font-size: 18px;
    max-width: 980px;
    line-height: 1.45;
    opacity: 0.96;
}

.game-rules {
    background: white;
    border-radius: 22px;
    padding: 20px 24px;
    border: 1px solid #D8ECF4;
    box-shadow: 0 8px 24px rgba(5,43,68,0.07);
    margin-bottom: 18px;
    color: #052B44;
}

.game-rules b {
    color: #052B44;
}

.game-turn-card {
    background: linear-gradient(135deg, #FFFFFF 0%, #E8F8FB 100%);
    border: 1px solid #D8ECF4;
    border-radius: 22px;
    padding: 18px 22px;
    box-shadow: 0 8px 24px rgba(5,43,68,0.07);
    color: #052B44;
    font-size: 18px;
    font-weight: 800;
    text-align: center;
}

.game-axis-label {
    background: #052B44;
    color: white;
    border-radius: 16px;
    padding: 12px 10px;
    text-align: center;
    font-weight: 850;
    min-height: 64px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1.15;
    box-shadow: 0 8px 18px rgba(5,43,68,0.12);
}

.game-row-label {
    background: linear-gradient(135deg, #0A6C9F 0%, #22B8CF 100%);
    color: white;
    border-radius: 16px;
    padding: 12px 10px;
    text-align: center;
    font-weight: 850;
    min-height: 72px;
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 1.15;
    box-shadow: 0 8px 18px rgba(5,43,68,0.10);
}

.game-empty-corner {
    background: transparent;
    min-height: 64px;
}

.game-answer-box {
    background-color: white;
    border-left: 7px solid #22B8CF;
    border-radius: 20px;
    padding: 18px 22px;
    margin-top: 22px;
    box-shadow: 0 8px 24px rgba(5,43,68,0.07);
    color: #052B44;
}

.game-answer-box b {
    color: #052B44;
}

/* Streamlit game buttons */
div[data-testid="stButton"] button {
    border-radius: 18px;
    border: 2px solid rgba(10,108,159,0.22);
    background:
        linear-gradient(90deg,
            rgba(255,255,255,0.72) 0px,
            rgba(255,255,255,0.72) 2px,
            transparent 2px,
            transparent calc(100% - 2px),
            rgba(255,255,255,0.72) calc(100% - 2px),
            rgba(255,255,255,0.72) 100%
        ),
        linear-gradient(135deg, #E8F8FB 0%, #BDEFFA 48%, #6EDAF0 100%);
    color: #052B44;
    font-weight: 900;
    min-height: 66px;
    box-shadow: 0 8px 20px rgba(5,43,68,0.09);
    transition: 0.2s ease;
}

div[data-testid="stButton"] button:hover {
    border-color: #0A6C9F;
    transform: translateY(-2px);
    box-shadow: 0 14px 28px rgba(5,43,68,0.16);
}

div[data-testid="stButton"] button:disabled {
    background: #E4EEF3;
    color: #52616B;
    border-color: #D8ECF4;
    box-shadow: none;
}
    
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def clean_text(value):
    """Clean text values, including common mojibake like Â."""
    if pd.isna(value):
        return ""
    value = str(value)
    value = value.replace("Â", "")
    value = value.replace("\xa0", " ")
    value = value.replace("Ã©", "é")
    value = value.replace("Ã¨", "è")
    value = value.replace("Ã¶", "ö")
    value = value.replace("Ã¼", "ü")
    value = value.replace("Ã¡", "á")
    value = value.replace("Ã­", "í")
    value = value.replace("Ã³", "ó")
    value = value.replace("Ã£", "ã")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def snake_case(col):
    """Convert any column name to snake_case."""
    col = str(col)
    col = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", col)
    col = re.sub(r"[^0-9a-zA-Z]+", "_", col)
    col = col.strip("_").lower()
    return col


def format_time(seconds):
    """Format swimming seconds into mm:ss.xx or ss.xx."""
    if pd.isna(seconds):
        return ""
    try:
        seconds = float(seconds)
    except Exception:
        return ""

    if seconds >= 60:
        minutes = int(seconds // 60)
        sec = seconds - minutes * 60
        return f"{minutes}:{sec:05.2f}"
    return f"{seconds:.2f}"


def time_to_seconds(value):
    """Convert different time formats into seconds."""
    if pd.isna(value):
        return np.nan

    if isinstance(value, (int, float, np.integer, np.floating)):
        return float(value)

    s = clean_text(value).replace(",", ".")

    if not s:
        return np.nan

    parts = s.split(":")

    try:
        if len(parts) == 3:
            h = float(parts[0])
            m = float(parts[1])
            sec = float(parts[2])
            return h * 3600 + m * 60 + sec
        if len(parts) == 2:
            m = float(parts[0])
            sec = float(parts[1])
            return m * 60 + sec
        return float(s)
    except Exception:
        return np.nan


def parse_any_date(value):
    """Parse date values, including Excel serial dates and text dates."""
    if pd.isna(value):
        return pd.NaT

    if isinstance(value, pd.Timestamp):
        return value

    if isinstance(value, (int, float, np.integer, np.floating)):
        if value > 20000:
            return pd.to_datetime("1899-12-30") + pd.to_timedelta(float(value), unit="D")
        return pd.NaT

    s = clean_text(value)
    if not s:
        return pd.NaT

    date_1 = pd.to_datetime(s, errors="coerce", dayfirst=True)
    if not pd.isna(date_1):
        return date_1

    return pd.to_datetime(s, errors="coerce")


def normalize_gender(value):
    s = clean_text(value).lower()

    if s in ["m", "men", "male", "man"]:
        return "Men"
    if s in ["f", "women", "woman", "female"]:
        return "Women"
    if "mixed" in s:
        return "Mixed"
    return "Unknown"


def normalize_course(value):
    s = clean_text(value).upper()

    if s in ["LC", "LCM", "LONG COURSE", "LONG COURSE METERS"]:
        return "LC"
    if s in ["SC", "SCM", "SHORT COURSE", "SHORT COURSE METERS"]:
        return "SC"
    if "LCM" in s or "LONG" in s:
        return "LC"
    if "SCM" in s or "SHORT" in s:
        return "SC"
    return "Unknown"


def parse_distance_from_text(text):
    s = clean_text(text)
    match = re.search(r"\b(4x50|4x100|4x200|50|100|200|400|800|1500)\b", s)
    if match:
        return match.group(1)
    return ""


def parse_stroke_from_text(text):
    s = clean_text(text).lower()

    if "freestyle" in s:
        return "Freestyle"
    if "backstroke" in s:
        return "Backstroke"
    if "breaststroke" in s:
        return "Breaststroke"
    if "butterfly" in s:
        return "Butterfly"
    if "medley" in s:
        return "Medley"
    return "Unknown"


def first_existing_column(df, candidates):
    for col in candidates:
        if col in df.columns:
            return col
    return None


def plotly_clean_layout(fig, height=480, title=None):
    if title is not None:
        fig.update_layout(title=title)

    fig.update_layout(
        height=height,
        font=dict(
            family="Arial",
            size=13,
            color=NAVY
        ),
        title=dict(
            font=dict(size=22, color=NAVY),
            x=0.02,
            xanchor="left"
        ),
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=45, r=35, t=85, b=55),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=NAVY, size=12)
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_color=NAVY
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#DDEAF0",
        zeroline=False,
        title_font=dict(color=NAVY, size=14),
        tickfont=dict(color=NAVY, size=12),
        linecolor=NAVY,
        color=NAVY
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#DDEAF0",
        zeroline=False,
        title_font=dict(color=NAVY, size=14),
        tickfont=dict(color=NAVY, size=12),
        linecolor=NAVY,
        color=NAVY
    )

    fig.update_traces(
        textfont=dict(color=NAVY, size=11)
    )

    return fig


def card(label, value, note=""):
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def section(title, subtitle=""):
    st.markdown(f"<div class='section-title'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


def safe_unique(series):
    if series is None:
        return []
    return sorted([x for x in series.dropna().unique().tolist() if clean_text(x) != ""])


def apply_common_filters(df, gender=True, course=True, stroke=True, distance=True, key_prefix=""):
    filtered = df.copy()

    with st.sidebar:
        st.markdown("### Filters")

        if gender and "gender" in filtered.columns:
            genders = safe_unique(filtered["gender"])
            selected_gender = st.multiselect(
                "Gender",
                genders,
                default=genders,
                key=f"{key_prefix}_gender"
            )
            filtered = filtered[filtered["gender"].isin(selected_gender)]

        if course and "course" in filtered.columns:
            courses = safe_unique(filtered["course"])
            selected_course = st.multiselect(
                "Course",
                courses,
                default=courses,
                key=f"{key_prefix}_course"
            )
            filtered = filtered[filtered["course"].isin(selected_course)]

        if stroke and "stroke" in filtered.columns:
            strokes = safe_unique(filtered["stroke"])
            selected_stroke = st.multiselect(
                "Stroke",
                strokes,
                default=strokes,
                key=f"{key_prefix}_stroke"
            )
            filtered = filtered[filtered["stroke"].isin(selected_stroke)]

        if distance and "distance" in filtered.columns:
            distances = safe_unique(filtered["distance"])
            selected_distance = st.multiselect(
                "Distance",
                distances,
                default=distances,
                key=f"{key_prefix}_distance"
            )
            filtered = filtered[filtered["distance"].isin(selected_distance)]

    return filtered

# ============================================================
# GAME FUNCTIONS - SWIM RECORD TOE
# ============================================================

def normalize_answer(value):
    """Normalize swimmer names for robust answer checking."""
    value = clean_text(value).lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9\s]", "", value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def prepare_swim_game_data(df):
    """Prepare world record data for the tic-tac-toe quiz."""
    game_df = df.copy()

    game_df = game_df[game_df["name"].astype(str).str.strip() != ""].copy()
    game_df = game_df[game_df["event_label"].astype(str).str.strip() != ""].copy()

    # Place criterion: location first, meet as fallback.
    game_df["record_place"] = game_df["location"].astype(str).apply(clean_text)

    if "meet" in game_df.columns:
        game_df.loc[game_df["record_place"] == "", "record_place"] = (
            game_df.loc[game_df["record_place"] == "", "meet"]
            .astype(str)
            .apply(clean_text)
        )

    game_df.loc[game_df["record_place"] == "", "record_place"] = "Unknown place"

    # Decade criterion.
    game_df["year_numeric"] = pd.to_numeric(game_df["year"], errors="coerce")
    game_df["decade"] = np.where(
        game_df["year_numeric"].notna(),
        ((game_df["year_numeric"] // 10) * 10).astype("Int64").astype(str) + "s",
        "Unknown decade"
    )

    # Compact event criterion, useful if event_label is too specific.
    game_df["event_family"] = (
        game_df["distance"].astype(str)
        + "m "
        + game_df["stroke"].astype(str)
    )

    # Remove empty/useless criteria.
    for col in ["record_place", "nationality", "decade", "course", "event_label", "event_family"]:
        if col in game_df.columns:
            game_df[col] = game_df[col].astype(str).apply(clean_text)
            game_df = game_df[game_df[col] != ""]
            game_df = game_df[game_df[col] != "Unknown"]

    return game_df


def build_swim_game_grid(game_df, row_col, col_col, attempts=1500):
    """
    Build a 3x3 grid.
    It tries to find rows and columns where every intersection has at least one valid swimmer.
    """
    pair_counts = (
        game_df
        .dropna(subset=[row_col, col_col, "name"])
        .groupby([row_col, col_col])["name"]
        .nunique()
        .reset_index(name="valid_answers")
    )

    if pair_counts.empty:
        return [], [], 0

    # Use the most connected values to avoid impossible boards.
    candidate_rows = (
        pair_counts.groupby(row_col)["valid_answers"]
        .sum()
        .sort_values(ascending=False)
        .head(35)
        .index
        .tolist()
    )

    candidate_cols = (
        pair_counts.groupby(col_col)["valid_answers"]
        .sum()
        .sort_values(ascending=False)
        .head(35)
        .index
        .tolist()
    )

    if len(candidate_rows) < 3 or len(candidate_cols) < 3:
        return [], [], 0

    best_rows = None
    best_cols = None
    best_score = -1

    for _ in range(attempts):
        rows = random.sample(candidate_rows, 3)
        cols = random.sample(candidate_cols, 3)

        score = 0
        for r in rows:
            for c in cols:
                exists = (
                    (pair_counts[row_col] == r)
                    & (pair_counts[col_col] == c)
                ).any()
                if exists:
                    score += 1

        if score > best_score:
            best_rows = rows
            best_cols = cols
            best_score = score

        if score == 9:
            break

    return best_rows, best_cols, best_score


def get_cell_answers(game_df, row_value, col_value, row_col, col_col):
    """Return all valid swimmers for a specific grid cell."""
    cell_df = game_df[
        (game_df[row_col].astype(str) == str(row_value))
        & (game_df[col_col].astype(str) == str(col_value))
    ].copy()

    answers = (
        cell_df["name"]
        .dropna()
        .astype(str)
        .apply(clean_text)
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    return answers


def validate_swim_answer(game_df, answer, row_value, col_value, row_col, col_col):
    """Check whether the submitted swimmer is valid for the selected cell."""
    valid_answers = get_cell_answers(game_df, row_value, col_value, row_col, col_col)

    if not valid_answers:
        return False, None, []

    normalized_map = {
        normalize_answer(name): name
        for name in valid_answers
    }

    user_norm = normalize_answer(answer)

    if user_norm in normalized_map:
        return True, normalized_map[user_norm], valid_answers

    close = get_close_matches(
        user_norm,
        list(normalized_map.keys()),
        n=1,
        cutoff=0.84
    )

    if close:
        return True, normalized_map[close[0]], valid_answers

    return False, None, valid_answers


def check_swim_game_winner(board):
    """Return winner symbol, Draw, or None."""
    lines = []

    lines.extend(board)
    lines.extend([[board[0][j], board[1][j], board[2][j]] for j in range(3)])
    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] != "" and line[0] == line[1] == line[2]:
            return line[0]

    if all(board[i][j] != "" for i in range(3) for j in range(3)):
        return "Draw"

    return None


def reset_swim_record_toe(game_df, row_col, col_col):
    rows, cols, score = build_swim_game_grid(game_df, row_col, col_col)

    st.session_state.swim_toe_rows = rows
    st.session_state.swim_toe_cols = cols
    st.session_state.swim_toe_score = score
    st.session_state.swim_toe_board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.swim_toe_answers = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.swim_toe_turn = "❌"
    st.session_state.swim_toe_winner = None
    st.session_state.swim_toe_selected = None
    st.session_state.swim_toe_used_names = []
    st.session_state.swim_toe_feedback = ""


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_world_records():
    if not WR_FILE.exists():
        return pd.DataFrame()

    df = pd.read_excel(WR_FILE)
    df.columns = [snake_case(c) for c in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(clean_text)

    if "seconds" not in df.columns:
        time_col = first_existing_column(df, ["time", "swim_time", "duration"])
        if time_col:
            df["seconds"] = df[time_col].apply(time_to_seconds)
        else:
            df["seconds"] = np.nan
    else:
        df["seconds"] = pd.to_numeric(df["seconds"], errors="coerce")

    if "time" not in df.columns:
        df["time"] = df["seconds"].apply(format_time)
    else:
        df["time"] = df["time"].fillna(df["seconds"].apply(format_time))

    if "date" in df.columns:
        df["date"] = df["date"].apply(parse_any_date)
    else:
        df["date"] = pd.NaT

    df["year"] = df["date"].dt.year

    if "gender" in df.columns:
        df["gender"] = df["gender"].apply(normalize_gender)
    else:
        df["gender"] = "Unknown"

    if "course" in df.columns:
        df["course"] = df["course"].apply(normalize_course)
    else:
        df["course"] = "Unknown"

    if "distance" in df.columns:
        df["distance"] = df["distance"].astype(str).str.replace(".0", "", regex=False)
    else:
        df["distance"] = df.get("event", "").apply(parse_distance_from_text)

    if "stroke" not in df.columns:
        df["stroke"] = df.get("event", "").apply(parse_stroke_from_text)

    if "name" not in df.columns:
        df["name"] = ""

    if "nationality" not in df.columns:
        df["nationality"] = "Unknown"

    if "meet" not in df.columns:
        df["meet"] = ""

    if "location" not in df.columns:
        df["location"] = ""

    if "is_current" in df.columns:
        df["is_current_bool"] = (
            df["is_current"]
            .astype(str)
            .str.lower()
            .str.strip()
            .isin(["true", "1", "yes", "current"])
        )
    elif "iscurrent" in df.columns:
        df["is_current_bool"] = (
            df["iscurrent"]
            .astype(str)
            .str.lower()
            .str.strip()
            .isin(["true", "1", "yes", "current"])
        )
    else:
        df["is_current_bool"] = False

    df["event_label"] = (
        df["gender"].astype(str)
        + " "
        + df["distance"].astype(str)
        + "m "
        + df["stroke"].astype(str)
        + " ("
        + df["course"].astype(str)
        + ")"
    )

    df = df.sort_values(["event_label", "date", "seconds"], ascending=[True, True, True])

    return df


@st.cache_data
def load_top_performances():
    if not TOP_FILE.exists():
        return pd.DataFrame()

    df = pd.read_excel(TOP_FILE)
    df.columns = [snake_case(c) for c in df.columns]

    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].apply(clean_text)

    desc_col = first_existing_column(df, ["event_description", "event_name", "event"])

    time_col = first_existing_column(df, ["swim_time", "seconds", "time_seconds", "duration"])
    if time_col:
        df["time_seconds"] = df[time_col].apply(time_to_seconds)
    else:
        df["time_seconds"] = np.nan

    date_col = first_existing_column(df, ["swim_date", "date"])
    if date_col:
        df["date"] = df[date_col].apply(parse_any_date)
    else:
        df["date"] = pd.NaT

    df["year"] = df["date"].dt.year

    if "rank_order" in df.columns:
        df["rank"] = pd.to_numeric(df["rank_order"], errors="coerce")
    elif "rank" in df.columns:
        df["rank"] = pd.to_numeric(df["rank"], errors="coerce")
    else:
        df["rank"] = np.nan

    if "athlete_full_name" in df.columns:
        df["athlete"] = df["athlete_full_name"]
    elif "name" in df.columns:
        df["athlete"] = df["name"]
    else:
        df["athlete"] = ""

    if "team_name" not in df.columns:
        df["team_name"] = ""

    if "team_code" not in df.columns:
        df["team_code"] = ""

    if "city" not in df.columns:
        df["city"] = ""

    if "country_code" not in df.columns:
        df["country_code"] = ""

    if "gender" in df.columns:
        df["gender"] = df["gender"].apply(normalize_gender)
    else:
        df["gender"] = df[desc_col].apply(normalize_gender) if desc_col else "Unknown"

    if desc_col:
        df["distance"] = df[desc_col].apply(parse_distance_from_text)
        df["stroke"] = df[desc_col].apply(parse_stroke_from_text)
        df["course"] = df[desc_col].apply(lambda x: "LC" if "LCM" in clean_text(x).upper() else "SC" if "SCM" in clean_text(x).upper() else "Unknown")
        df["event_label"] = df[desc_col]
    else:
        df["distance"] = ""
        df["stroke"] = "Unknown"
        df["course"] = "Unknown"
        df["event_label"] = "Unknown event"

    df["time_label"] = df["time_seconds"].apply(format_time)

    df = df.sort_values(["event_label", "rank", "time_seconds"], ascending=[True, True, True])

    return df


wr = load_world_records()
top = load_top_performances()


# ============================================================
# DATA CHECK
# ============================================================

missing_files = []

if wr.empty:
    missing_files.append(str(WR_FILE))

if top.empty:
    missing_files.append(str(TOP_FILE))

if missing_files:
    st.error(
        "Missing or unreadable file(s): "
        + ", ".join(missing_files)
        + ". Put the Excel files in the same folder as app.py."
    )
    st.stop()


# ============================================================
# TOP NAVIGATION - SWIMMING POOL LANES
# ============================================================

PAGES = [
    "Home",
    "World Record Timeline",
    "All-Time Top 200 Rankings",
    "Athletes Hall of Fame",
    "Nations & Places",
    "Compare Events",
    "Data & Methods",
    "Swim Record Toe"
]

PAGE_LABELS = {
    "Home": "Home",
    "World Record Timeline": "Timeline",
    "All-Time Top 200 Rankings": "Top 200",
    "Athletes Hall of Fame": "Athletes",
    "Nations & Places": "Nations",
    "Compare Events": "Compare",
    "Data & Methods": "Methods",
    "Swim Record Toe": "Game"
}

PAGE_TAGS = {
    "Home": "Start block",
    "World Record Timeline": "Record flow",
    "All-Time Top 200 Rankings": "Elite depth",
    "Athletes Hall of Fame": "Legends",
    "Nations & Places": "Maps & flags",
    "Compare Events": "Race match",
    "Data & Methods": "Behind data",
    "Swim Record Toe": "Quiz lane"
}

# Read selected page from the URL.
# Example: ?page=World%20Record%20Timeline
query_page = st.query_params.get("page", "Home")

if isinstance(query_page, list):
    query_page = query_page[0]

page = query_page if query_page in PAGES else "Home"

# Build the lane buttons as ONE compact HTML string.
# Important: no multi-line indented HTML here, otherwise Streamlit may print it as code.
nav_items = ""

for i, page_name in enumerate(PAGES, start=1):
    active_class = " active" if page == page_name else ""
    page_url = quote(page_name, safe="")

    nav_items += (
        f'<a class="pool-lane{active_class}" href="?page={page_url}">'
        f'<span class="lane-number">Lane {i}</span>'
        f'<span class="lane-label">{PAGE_LABELS[page_name]}</span>'
        f'<span class="lane-tag">{PAGE_TAGS[page_name]}</span>'
        f'</a>'
    )

nav_html = (
    '<div class="pool-nav-shell">'
    '<div class="pool-nav-top">'
    '<div class="pool-brand">🏊 Swim Records Explorer</div>'
    '<div class="pool-subtitle">'
    'Select a lane to dive into swimming records, rankings, athletes and nations.'
    '</div>'
    '</div>'
    f'<div class="pool-grid">{nav_items}</div>'
    f'<div class="current-lane">Current lane: <b>{PAGE_LABELS[page]}</b></div>'
    '</div>'
)

st.markdown(nav_html, unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## 🏊 Filters")
    st.caption("Use this panel only when a page requires filtering.")
    st.markdown("---")
    st.caption("Gold = current record / best performance. Blue = long course. Aqua = short course.")


# ============================================================
# PAGE 1 - HOME
# ============================================================

if page == "Home":

    st.markdown(
        """
        <div class="hero">
            <h1>Swim Records Explorer</h1>
            <p>
            Explore the evolution of world records and the greatest all-time performances in swimming.
            This interactive archive is designed for fans: simple enough to explore, but structured enough
            to reveal athletes, nations, events and historical moments that shaped swimming speed.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        card("World record entries", f"{len(wr):,}", "Historical record progressions")

    with c2:
        card("Top performances", f"{len(top):,}", "Top 200 rankings by event")

    with c3:
        card("Events covered", f"{wr['event_label'].nunique():,}", "Across course, gender and stroke")

    with c4:
        year_min = int(wr["year"].min()) if wr["year"].notna().any() else "-"
        year_max = int(wr["year"].max()) if wr["year"].notna().any() else "-"
        card("Record history", f"{year_min}–{year_max}", "Historical time range")

    st.markdown(
        """
        <div class="info-box">
        <b>Editorial angle:</b> this app does not simply list swimming results.
        It tells the story of speed through two complementary views:
        <br><br>
        <b>World records</b> show how the limit of performance changed over time.  
        <br>
        <b>Top 200 all-time rankings</b> show the depth of elite swimming beyond the single fastest time.
        </div>
        """,
        unsafe_allow_html=True
    )

    section(
        "Overview",
        "A first glance at how world records are distributed across time and how dominant athletes emerge from the database."
    )

    col_a, col_b = st.columns([1.2, 1])

    with col_a:
        wr_year = wr.dropna(subset=["year"]).copy()
        wr_year["year"] = wr_year["year"].astype(int)

        year_counts = (
            wr_year.groupby("year")
            .size()
            .reset_index(name="records")
            .sort_values("year")
        )

        fig = px.bar(
            year_counts,
            x="year",
            y="records",
            text="records",
            color_discrete_sequence=[BLUE],
            title="World records by year"
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(color=NAVY, size=9),
            marker_line_color="white",
            marker_line_width=0.8,
            cliponaxis=False
        )

        fig.update_xaxes(
            title="Year",
            dtick=10
        )

        fig.update_yaxes(
            title="Number of world records"
        )

        fig = plotly_clean_layout(fig, height=460)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="small-caption">
            Each bar shows how many world record entries were set in that year.
            Recent years after 2020 are included when present in the dataset.
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_b:
        athlete_wr = (
            wr[wr["name"] != ""]
            .groupby("name")
            .size()
            .reset_index(name="world_records")
            .sort_values("world_records", ascending=False)
            .head(10)
        )

        fig = px.bar(
            athlete_wr,
            x="world_records",
            y="name",
            orientation="h",
            text="world_records",
            color_discrete_sequence=[GOLD],
            title="Most recurring athletes in world record history"
        )

        fig.update_traces(
            textposition="outside",
            textfont=dict(color=NAVY, size=12),
            marker_line_color="white",
            marker_line_width=0.8,
            cliponaxis=False
        )

        fig.update_layout(
            yaxis=dict(autorange="reversed")
        )

        fig.update_xaxes(
            title="Number of world record entries"
        )

        fig.update_yaxes(
            title=""
        )

        fig = plotly_clean_layout(fig, height=460)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(
            """
            <div class="small-caption">
            This ranking counts record entries, not unique titles or medals.
            The same athlete can appear multiple times across events and years.
            </div>
            """,
            unsafe_allow_html=True
        )

    section(
    "How to read this app",
    "Use the swimming-pool lanes at the top of the page to move across the story: first the record timeline, then current records, then all-time rankings, athletes and nations."
    )

    st.markdown(
        """
        <div class="warning-box">
        <b>Important limitation:</b> the app visualizes elite swimming performances.
        It does not include every official swimming result ever recorded, so conclusions should refer to
        <b>world records</b> and <b>top-200 all-time entries</b>, not to the whole swimming population.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 2 - WORLD RECORD TIMELINE
# ============================================================

elif page == "World Record Timeline":

    section(
        "World Record Timeline",
        "Follow how the fastest official world record in each event changed over time. Lower seconds mean faster performance."
    )

    filtered = apply_common_filters(
        wr,
        gender=True,
        course=True,
        stroke=True,
        distance=True,
        key_prefix="timeline"
    )

    with st.sidebar:
        st.markdown("### Event selection")
        available_events = safe_unique(filtered["event_label"])
        selected_event = st.selectbox(
            "Choose one event",
            available_events,
            index=0 if available_events else None
        )

    data = filtered[filtered["event_label"] == selected_event].copy()
    data = data.sort_values("date")

    if data.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    first_record = data.dropna(subset=["seconds"]).iloc[0]
    last_record = data.dropna(subset=["seconds"]).iloc[-1]
    improvement = first_record["seconds"] - last_record["seconds"]
    improvement_pct = improvement / first_record["seconds"] * 100 if first_record["seconds"] else np.nan

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Selected event", selected_event)

    with c2:
        st.metric("Number of records", len(data))

    with c3:
        st.metric("Total improvement", f"{improvement:.2f} s")

    with c4:
        st.metric("Improvement %", f"{improvement_pct:.1f}%")

    fig = px.line(
        data,
        x="date",
        y="seconds",
        markers=True,
        color="course",
        color_discrete_map=COURSE_COLORS,
        hover_data={
            "name": True,
            "nationality": True,
            "time": True,
            "meet": True,
            "location": True,
            "date": "|%d %b %Y",
            "seconds": ":.2f"
        },
        title=f"Record progression — {selected_event}"
    )

    current_data = data[data["is_current_bool"] == True]

    if not current_data.empty:
        fig.add_trace(
            go.Scatter(
                x=current_data["date"],
                y=current_data["seconds"],
                mode="markers+text",
                marker=dict(size=17, color=GOLD, symbol="star"),
                text=["Current record"] * len(current_data),
                textposition="top center",
                name="Current record",
                hovertext=current_data["name"] + " — " + current_data["time"],
                hoverinfo="text"
            )
        )

    fig.update_yaxes(
        autorange="reversed",
        title="Time in seconds — lower is faster"
    )
    fig.update_xaxes(title="Date")
    fig = plotly_clean_layout(fig, height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="small-caption">
        Design note: the y-axis is reversed because in swimming a lower time represents a better performance.
        The gold marker highlights the current world record.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        data[
            ["date", "time", "seconds", "name", "nationality", "meet", "location", "is_current_bool"]
        ].rename(
            columns={
                "date": "Date",
                "time": "Time",
                "seconds": "Seconds",
                "name": "Athlete",
                "nationality": "Nationality",
                "meet": "Meet",
                "location": "Location",
                "is_current_bool": "Current record"
            }
        ),
        use_container_width=True,
        hide_index=True
    )



# ============================================================
# PAGE 3 - ALL-TIME TOP 200 RANKINGS
# ============================================================

elif page == "All-Time Top 200 Rankings":

    section(
        "All-Time Top 200 Rankings",
        "Go beyond the world record and explore the depth of elite swimming performances."
    )

    filtered = apply_common_filters(
        top,
        gender=True,
        course=True,
        stroke=True,
        distance=True,
        key_prefix="top"
    )

    with st.sidebar:
        st.markdown("### Ranking selection")

        events = safe_unique(filtered["event_label"])
        selected_event = st.selectbox(
            "Choose event",
            events,
            index=0 if events else None,
            key="top_event"
        )

        max_rank = int(filtered["rank"].max()) if filtered["rank"].notna().any() else 200
        rank_limit = st.slider(
            "Show top N",
            min_value=5,
            max_value=min(200, max_rank),
            value=30,
            step=5
        )

    data = filtered[
        (filtered["event_label"] == selected_event)
        & (filtered["rank"] <= rank_limit)
    ].copy()

    if data.empty:
        st.warning("No ranking data available for the selected filters.")
        st.stop()

    data = data.sort_values(["rank", "time_seconds"])

    best_time = data["time_seconds"].min()
    data["gap_from_best"] = data["time_seconds"] - best_time
    data["chart_label"] = (
        "#" + data["rank"].astype(int).astype(str)
        + " — "
        + data["athlete"].astype(str)
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("Event", selected_event)

    with c2:
        st.metric("Best time", format_time(best_time))

    with c3:
        st.metric("Athletes shown", data["athlete"].nunique())

    with c4:
        st.metric("Nations shown", data["team_name"].nunique())

    fig = px.bar(
        data.sort_values("rank"),
        x="gap_from_best",
        y="chart_label",
        orientation="h",
        color="gap_from_best",
        color_continuous_scale=[[0, GOLD], [1, BLUE]],
        hover_data={
            "athlete": True,
            "time_label": True,
            "rank": True,
            "team_name": True,
            "city": True,
            "date": True,
            "gap_from_best": ":.2f"
        },
        title=f"Gap from the best time — {selected_event}"
    )
    fig.update_layout(yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
    fig.update_xaxes(title="Gap from best time, seconds")
    fig.update_yaxes(title="")
    fig = plotly_clean_layout(fig, height=max(520, 22 * len(data)))
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns([1, 1])

    with col_a:
        fig_hist = px.histogram(
            filtered[filtered["event_label"] == selected_event],
            x="time_seconds",
            nbins=30,
            color_discrete_sequence=[AQUA],
            title="Distribution of top-200 times"
        )
        fig_hist.update_xaxes(title="Time in seconds")
        fig_hist.update_yaxes(title="Number of performances")
        fig_hist = plotly_clean_layout(fig_hist, height=420)
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        athlete_counts = (
            filtered[filtered["event_label"] == selected_event]
            .groupby("athlete")
            .size()
            .reset_index(name="entries")
            .sort_values("entries", ascending=False)
            .head(15)
        )

        fig_ath = px.bar(
            athlete_counts,
            x="entries",
            y="athlete",
            orientation="h",
            color_discrete_sequence=[BLUE],
            title="Most recurring athletes in this event top 200"
        )
        fig_ath.update_layout(yaxis=dict(autorange="reversed"))
        fig_ath = plotly_clean_layout(fig_ath, height=420)
        st.plotly_chart(fig_ath, use_container_width=True)

    st.dataframe(
        data[
            [
                "rank", "athlete", "time_label", "time_seconds",
                "team_name", "team_code", "date", "city", "country_code"
            ]
        ].rename(
            columns={
                "rank": "Rank",
                "athlete": "Athlete",
                "time_label": "Time",
                "time_seconds": "Seconds",
                "team_name": "Team",
                "team_code": "Team code",
                "date": "Date",
                "city": "City",
                "country_code": "Country code"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 4 - ATHLETES HALL OF FAME
# ============================================================

elif page == "Athletes Hall of Fame":

    section(
        "Athletes Hall of Fame",
        "Explore the swimmers who appear most often in world record history and all-time rankings."
    )

    wr_names = set(wr["name"].dropna().unique())
    top_names = set(top["athlete"].dropna().unique())
    all_names = sorted([x for x in wr_names.union(top_names) if clean_text(x) != ""])

    with st.sidebar:
        st.markdown("### Athlete selection")
        search = st.text_input("Search athlete", "")
        if search:
            filtered_names = [n for n in all_names if search.lower() in n.lower()]
        else:
            filtered_names = all_names

        selected_athlete = st.selectbox(
            "Choose athlete",
            filtered_names,
            index=0 if filtered_names else None
        )

    if not selected_athlete:
        st.warning("No athlete selected.")
        st.stop()

    athlete_wr = wr[wr["name"] == selected_athlete].copy()
    athlete_top = top[top["athlete"] == selected_athlete].copy()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric("World record entries", len(athlete_wr))

    with c2:
        st.metric("Current world records", int(athlete_wr["is_current_bool"].sum()) if not athlete_wr.empty else 0)

    with c3:
        st.metric("Top-200 entries", len(athlete_top))

    with c4:
        best_rank = int(athlete_top["rank"].min()) if not athlete_top.empty and athlete_top["rank"].notna().any() else "-"
        st.metric("Best top-200 rank", best_rank)

    st.markdown(
        f"""
        <div class="info-box">
        <b>{selected_athlete}</b> profile combines two sources:
        world record progression entries and top-200 all-time ranking appearances.
        </div>
        """,
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns([1.1, 1])

    with col_a:
        if not athlete_wr.empty:
            athlete_wr = athlete_wr.sort_values("date")

            fig = px.scatter(
                athlete_wr,
                x="date",
                y="seconds",
                color="course",
                color_discrete_map=COURSE_COLORS,
                size=np.where(athlete_wr["is_current_bool"], 18, 9),
                hover_data=["event_label", "time", "nationality", "meet", "location"],
                title=f"World record timeline — {selected_athlete}"
            )
            fig.update_yaxes(autorange="reversed", title="Time in seconds — lower is faster")
            fig.update_xaxes(title="Date")
            fig = plotly_clean_layout(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("This athlete has no world record entries in the world record dataset.")

    with col_b:
        if not athlete_top.empty:
            event_counts = (
                athlete_top.groupby("event_label")
                .size()
                .reset_index(name="entries")
                .sort_values("entries", ascending=False)
            )

            fig = px.bar(
                event_counts,
                x="entries",
                y="event_label",
                orientation="h",
                color_discrete_sequence=[GOLD],
                title=f"Top-200 appearances by event"
            )
            fig.update_layout(yaxis=dict(autorange="reversed"))
            fig.update_yaxes(title="")
            fig = plotly_clean_layout(fig, height=500)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("This athlete has no top-200 entries in the all-time ranking dataset.")

    section(
        "Global athlete rankings",
        "These rankings show recurring names, not necessarily a final judgement of absolute greatness."
    )

    col_1, col_2 = st.columns(2)

    with col_1:
        wr_rank = (
            wr.groupby("name")
            .size()
            .reset_index(name="world_record_entries")
            .sort_values("world_record_entries", ascending=False)
            .head(15)
        )

        fig = px.bar(
            wr_rank,
            x="world_record_entries",
            y="name",
            orientation="h",
            color_discrete_sequence=[BLUE],
            title="Most world record entries"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=520)
        st.plotly_chart(fig, use_container_width=True)

    with col_2:
        top_rank = (
            top.groupby("athlete")
            .size()
            .reset_index(name="top_200_entries")
            .sort_values("top_200_entries", ascending=False)
            .head(15)
        )

        fig = px.bar(
            top_rank,
            x="top_200_entries",
            y="athlete",
            orientation="h",
            color_discrete_sequence=[AQUA],
            title="Most top-200 entries"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=520)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Athlete world record entries"):
        if not athlete_wr.empty:
            st.dataframe(
                athlete_wr[
                    ["event_label", "time", "seconds", "date", "nationality", "meet", "location", "is_current_bool"]
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No world record entries.")

    with st.expander("Athlete top-200 entries"):
        if not athlete_top.empty:
            st.dataframe(
                athlete_top[
                    ["event_label", "rank", "time_label", "time_seconds", "team_name", "date", "city"]
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.write("No top-200 entries.")


# ============================================================
# PAGE 5 - NATIONS & PLACES
# ============================================================

elif page == "Nations & Places":

    section(
        "Nations & Places",
        "Discover which nations and locations appear most frequently in swimming record history and all-time rankings."
    )

    filtered_wr = apply_common_filters(
        wr,
        gender=True,
        course=True,
        stroke=True,
        distance=True,
        key_prefix="nation"
    )

    if filtered_wr.empty:
        st.warning("No world record data available for the selected filters.")
        st.stop()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Nations in WR data", filtered_wr["nationality"].nunique())

    with c2:
        st.metric("Record locations", filtered_wr["location"].nunique())

    with c3:
        st.metric("Meets", filtered_wr["meet"].nunique())

    col_a, col_b = st.columns(2)

    with col_a:
        nation_wr = (
            filtered_wr.groupby("nationality")
            .size()
            .reset_index(name="world_record_entries")
            .sort_values("world_record_entries", ascending=False)
            .head(20)
        )

        fig = px.bar(
            nation_wr,
            x="world_record_entries",
            y="nationality",
            orientation="h",
            color_discrete_sequence=[BLUE],
            title="Most represented nationalities in world record history"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=560)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        current_nations = (
            wr[wr["is_current_bool"] == True]
            .groupby("nationality")
            .size()
            .reset_index(name="current_records")
            .sort_values("current_records", ascending=False)
            .head(20)
        )

        fig = px.bar(
            current_nations,
            x="current_records",
            y="nationality",
            orientation="h",
            color_discrete_sequence=[GOLD],
            title="Current world records by nationality"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=560)
        st.plotly_chart(fig, use_container_width=True)

    col_c, col_d = st.columns(2)

    with col_c:
        top_nations = (
            top.groupby("team_name")
            .size()
            .reset_index(name="top_200_entries")
            .sort_values("top_200_entries", ascending=False)
            .head(20)
        )

        fig = px.bar(
            top_nations,
            x="top_200_entries",
            y="team_name",
            orientation="h",
            color_discrete_sequence=[AQUA],
            title="Most represented teams in top-200 rankings"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=560)
        st.plotly_chart(fig, use_container_width=True)

    with col_d:
        locations = (
            filtered_wr[filtered_wr["location"] != ""]
            .groupby("location")
            .size()
            .reset_index(name="records")
            .sort_values("records", ascending=False)
            .head(20)
        )

        fig = px.bar(
            locations,
            x="records",
            y="location",
            orientation="h",
            color_discrete_sequence=[NAVY],
            title="Locations where world records were set"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig = plotly_clean_layout(fig, height=560)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        """
        <div class="small-caption">
        Interpretation note: these charts show representation inside the available datasets.
        They should not be read as a complete medal table or as a full ranking of national swimming systems.
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAGE 6 - COMPARE EVENTS
# ============================================================

elif page == "Compare Events":

    section(
        "Compare Events",
        "Compare how different swimming events evolved: number of record changes, time improvement and record age."
    )

    filtered = apply_common_filters(
        wr,
        gender=True,
        course=True,
        stroke=True,
        distance=True,
        key_prefix="compare"
    )

    if filtered.empty:
        st.warning("No data available for the selected filters.")
        st.stop()

    summary_rows = []

    for event, group in filtered.dropna(subset=["seconds"]).groupby("event_label"):
        group = group.sort_values("date")

        if group.empty:
            continue

        first = group.iloc[0]
        last = group.iloc[-1]
        improvement_s = first["seconds"] - last["seconds"]
        improvement_pct = improvement_s / first["seconds"] * 100 if first["seconds"] else np.nan

        current_rows = group[group["is_current_bool"] == True]
        if not current_rows.empty:
            current_date = current_rows.iloc[-1]["date"]
            current_holder = current_rows.iloc[-1]["name"]
            current_time = current_rows.iloc[-1]["time"]
        else:
            current_date = last["date"]
            current_holder = last["name"]
            current_time = last["time"]

        age_years = (pd.Timestamp.today() - current_date).days / 365.25 if not pd.isna(current_date) else np.nan

        summary_rows.append(
            {
                "event_label": event,
                "records": len(group),
                "first_year": first["year"],
                "latest_year": last["year"],
                "first_seconds": first["seconds"],
                "latest_seconds": last["seconds"],
                "improvement_s": improvement_s,
                "improvement_pct": improvement_pct,
                "current_record_age_years": age_years,
                "current_holder": current_holder,
                "current_time": current_time
            }
        )

    summary = pd.DataFrame(summary_rows)

    if summary.empty:
        st.warning("No comparable event summary available.")
        st.stop()

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Events compared", len(summary))

    with c2:
        st.metric("Average record changes", f"{summary['records'].mean():.1f}")

    with c3:
        oldest = summary.sort_values("current_record_age_years", ascending=False).iloc[0]
        st.metric("Oldest current record", oldest["event_label"])

    col_a, col_b = st.columns(2)

    with col_a:
        fig = px.bar(
            summary.sort_values("records", ascending=False).head(25),
            x="records",
            y="event_label",
            orientation="h",
            color_discrete_sequence=[BLUE],
            title="Events with the most world record changes"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_xaxes(title="Number of historical records")
        fig.update_yaxes(title="")
        fig = plotly_clean_layout(fig, height=620)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        fig = px.bar(
            summary.sort_values("improvement_pct", ascending=False).head(25),
            x="improvement_pct",
            y="event_label",
            orientation="h",
            color_discrete_sequence=[AQUA],
            title="Largest percentage improvement from first to latest record"
        )
        fig.update_layout(yaxis=dict(autorange="reversed"))
        fig.update_xaxes(title="Improvement %")
        fig.update_yaxes(title="")
        fig = plotly_clean_layout(fig, height=620)
        st.plotly_chart(fig, use_container_width=True)

    section(
        "Record age",
        "Some records fall frequently, while others survive for many years."
    )

    fig = px.scatter(
        summary,
        x="records",
        y="current_record_age_years",
        size="improvement_pct",
        color="improvement_pct",
        color_continuous_scale=[[0, BLUE], [1, GOLD]],
        hover_data=[
            "event_label",
            "current_holder",
            "current_time",
            "first_year",
            "latest_year",
            "improvement_pct"
        ],
        title="Record changes vs current record age"
    )
    fig.update_xaxes(title="Number of record changes")
    fig.update_yaxes(title="Current record age, years")
    fig = plotly_clean_layout(fig, height=600)
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        summary.sort_values("records", ascending=False).rename(
            columns={
                "event_label": "Event",
                "records": "Number of records",
                "first_year": "First year",
                "latest_year": "Latest year",
                "improvement_s": "Improvement, seconds",
                "improvement_pct": "Improvement, %",
                "current_record_age_years": "Current record age, years",
                "current_holder": "Current holder",
                "current_time": "Current time"
            }
        ),
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# PAGE 7 - DATA & METHODS
# ============================================================

elif page == "Data & Methods":

    section(
        "Data & Methods",
        "This page explains how the app uses the two datasets and what limitations should be considered."
    )

    st.markdown(
        """
        <div class="info-box">
        <b>Dataset 1 — World records history</b><br>
        Used to visualize the historical progression of world records across gender, course, distance and stroke.
        It contains athlete name, nationality, date, meet, location, time in seconds and whether the record is current.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        pd.DataFrame(
            {
                "Property": [
                    "Rows",
                    "Events",
                    "Athletes",
                    "Nationalities",
                    "Courses",
                    "Years"
                ],
                "Value": [
                    len(wr),
                    wr["event_label"].nunique(),
                    wr["name"].nunique(),
                    wr["nationality"].nunique(),
                    ", ".join(safe_unique(wr["course"])),
                    f"{int(wr['year'].min())}–{int(wr['year'].max())}" if wr["year"].notna().any() else "-"
                ]
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        """
        <div class="info-box">
        <b>Dataset 2 — All-time top 200 performances</b><br>
        Used to explore depth of elite performance beyond a single record.
        It contains ranking order, athlete, team, event description, time, date and competition location.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        pd.DataFrame(
            {
                "Property": [
                    "Rows",
                    "Events",
                    "Athletes",
                    "Teams",
                    "Cities",
                    "Years"
                ],
                "Value": [
                    len(top),
                    top["event_label"].nunique(),
                    top["athlete"].nunique(),
                    top["team_name"].nunique(),
                    top["city"].nunique(),
                    f"{int(top['year'].min())}–{int(top['year'].max())}" if top["year"].notna().any() else "-"
                ]
            }
        ),
        use_container_width=True,
        hide_index=True
    )

    section("Interpretation rules")

    st.markdown(
        """
        <div class="warning-box">
        <b>1. Elite data only.</b><br>
        The app does not represent all swimming races ever performed. It focuses on world records and top-200 all-time performances.
        <br><br>
        <b>2. Same athlete can appear multiple times.</b><br>
        Entries represent performances or record events, not unique athletes.
        <br><br>
        <b>3. Long course and short course are not directly equivalent.</b><br>
        The app allows comparison, but interpretation should consider that LC and SC are different competition contexts.
        <br><br>
        <b>4. Lower time is better.</b><br>
        Timeline charts reverse the y-axis to make performance improvement visually intuitive.
        </div>
        """,
        unsafe_allow_html=True
    )

    with st.expander("World records raw preview"):
        st.dataframe(wr.head(100), use_container_width=True)

    with st.expander("Top performances raw preview"):
        st.dataframe(top.head(100), use_container_width=True)

        
        
# ============================================================
# PAGE 8 - SWIM RECORD TOE
# ============================================================

elif page == "Swim Record Toe":

    st.markdown(
        """
        <div class="game-hero">
            <h1>Swim Record Toe</h1>
            <p>
            A swimming version of tic-tac-toe: choose a square, connect the row and column criteria,
            then type or select the swimmer who really set a world record matching both conditions.
            Claim three lanes in a row to win.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="game-rules">
        <b>How to play:</b><br>
        1. Choose a free square in the pool grid.<br>
        2. Look at the row and column criteria.<br>
        3. Write the swimmer name or choose it from the dropdown.<br>
        4. If the answer exists in the world record dataset, you claim the lane with ❌ or ⭕.
        </div>
        """,
        unsafe_allow_html=True
    )

    game_df = prepare_swim_game_data(wr)

    if game_df.empty:
        st.error("The game cannot start because the world record dataset has no usable swimmer names.")
        st.stop()

    row_options = {
        "Specific event": "event_label",
        "Event family": "event_family",
        "Stroke": "stroke",
        "Gender": "gender"
    }

    col_options = {
        "Record location / pool": "record_place",
        "Nationality": "nationality",
        "Decade": "decade",
        "Course": "course"
    }

    c_setup_1, c_setup_2, c_setup_3 = st.columns([1, 1, 0.7])

    with c_setup_1:
        row_label = st.selectbox(
            "Rows define",
            list(row_options.keys()),
            index=0,
            key="swim_toe_row_label"
        )

    with c_setup_2:
        col_label = st.selectbox(
            "Columns define",
            list(col_options.keys()),
            index=0,
            key="swim_toe_col_label"
        )

    row_col = row_options[row_label]
    col_col = col_options[col_label]

    with c_setup_3:
        st.write("")
        st.write("")
        new_game = st.button("New game", use_container_width=True)

    state_missing = (
        "swim_toe_board" not in st.session_state
        or "swim_toe_rows" not in st.session_state
        or "swim_toe_cols" not in st.session_state
    )

    axes_changed = (
        st.session_state.get("swim_toe_row_col") != row_col
        or st.session_state.get("swim_toe_col_col") != col_col
    )

    if state_missing or axes_changed or new_game:
        st.session_state.swim_toe_row_col = row_col
        st.session_state.swim_toe_col_col = col_col
        reset_swim_record_toe(game_df, row_col, col_col)

    rows = st.session_state.swim_toe_rows
    cols = st.session_state.swim_toe_cols
    board = st.session_state.swim_toe_board

    if not rows or not cols:
        st.warning("Not enough data to build a 3x3 game board with these criteria. Try another row or column setting.")
        st.stop()

    if st.session_state.swim_toe_score < 9:
        st.warning(
            "This board contains one or more very difficult cells. "
            "Try another New game or switch from location to nationality/decade for an easier board."
        )

    c_turn_1, c_turn_2, c_turn_3 = st.columns(3)

    with c_turn_1:
        st.markdown(
            f"""
            <div class="game-turn-card">
            Current turn<br>
            <span style="font-size:34px;">{st.session_state.swim_toe_turn}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_turn_2:
        claimed = sum(
            1 for i in range(3) for j in range(3)
            if st.session_state.swim_toe_board[i][j] != ""
        )
        st.markdown(
            f"""
            <div class="game-turn-card">
            Claimed lanes<br>
            <span style="font-size:34px;">{claimed}/9</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c_turn_3:
        if st.session_state.swim_toe_winner is None:
            status_text = "Race still open"
        elif st.session_state.swim_toe_winner == "Draw":
            status_text = "Draw"
        else:
            status_text = f"{st.session_state.swim_toe_winner} wins"

        st.markdown(
            f"""
            <div class="game-turn-card">
            Status<br>
            <span style="font-size:25px;">{status_text}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("")

    # Header row
    header_cols = st.columns(4)
    header_cols[0].markdown("<div class='game-empty-corner'></div>", unsafe_allow_html=True)

    for j in range(3):
        header_cols[j + 1].markdown(
            f"<div class='game-axis-label'>{cols[j]}</div>",
            unsafe_allow_html=True
        )

    # Game grid
    for i in range(3):
        grid_cols = st.columns(4)

        grid_cols[0].markdown(
            f"<div class='game-row-label'>{rows[i]}</div>",
            unsafe_allow_html=True
        )

        for j in range(3):
            current_mark = board[i][j]
            valid_answers = get_cell_answers(game_df, rows[i], cols[j], row_col, col_col)

            if current_mark != "":
                label = f"{current_mark}\n{st.session_state.swim_toe_answers[i][j]}"
                disabled = True
            elif not valid_answers:
                label = "No data"
                disabled = True
            else:
                label = "Dive in"

                if st.session_state.swim_toe_selected == (i, j):
                    label = "Selected"

                disabled = st.session_state.swim_toe_winner is not None

            if grid_cols[j + 1].button(
                label,
                key=f"swim_toe_cell_{i}_{j}",
                use_container_width=True,
                disabled=disabled
            ):
                st.session_state.swim_toe_selected = (i, j)
                st.session_state.swim_toe_feedback = ""
                st.rerun()

    winner = st.session_state.swim_toe_winner

    if winner is not None:
        if winner == "Draw":
            st.success("The race ends in a draw. No more free lanes.")
        else:
            st.success(f"{winner} wins the pool battle!")

    selected = st.session_state.swim_toe_selected

    if selected is not None and st.session_state.swim_toe_winner is None:

        i, j = selected
        row_value = rows[i]
        col_value = cols[j]

        valid_answers = get_cell_answers(game_df, row_value, col_value, row_col, col_col)

        st.markdown(
            f"""
            <div class="game-answer-box">
            <b>Selected square:</b> {row_value} × {col_value}<br>
            Write the swimmer manually or choose a name from the dropdown.
            </div>
            """,
            unsafe_allow_html=True
        )

        all_swimmers = (
            game_df["name"]
            .dropna()
            .astype(str)
            .apply(clean_text)
            .drop_duplicates()
            .sort_values()
            .tolist()
        )

        c_ans_1, c_ans_2 = st.columns(2)

        with c_ans_1:
            typed_answer = st.text_input(
                "Write swimmer name",
                placeholder="Example: Michael Phelps",
                key=f"typed_answer_{i}_{j}"
            )

        with c_ans_2:
            dropdown_answer = st.selectbox(
                "Or choose swimmer from dropdown",
                [""] + all_swimmers,
                index=0,
                key=f"dropdown_answer_{i}_{j}"
            )

        answer_to_check = typed_answer.strip() if typed_answer.strip() else dropdown_answer.strip()

        c_submit_1, c_submit_2, c_submit_3 = st.columns([1, 1, 1])

        with c_submit_1:
            submit_answer = st.button("Submit answer", use_container_width=True)

        with c_submit_2:
            clear_selection = st.button("Cancel selection", use_container_width=True)

        with c_submit_3:
            reveal_hint = st.button("Small hint", use_container_width=True)

        if clear_selection:
            st.session_state.swim_toe_selected = None
            st.session_state.swim_toe_feedback = ""
            st.rerun()

        if reveal_hint:
            if valid_answers:
                st.info(f"Hint: there are {len(valid_answers)} valid swimmer(s) for this square.")
            else:
                st.warning("No valid swimmer exists for this square in the dataset.")

        if submit_answer:
            if answer_to_check == "":
                st.warning("Write or select a swimmer before submitting.")
            elif normalize_answer(answer_to_check) in st.session_state.swim_toe_used_names:
                st.warning("This swimmer has already been used in this game. Try another name.")
            else:
                is_correct, matched_name, possible_answers = validate_swim_answer(
                    game_df,
                    answer_to_check,
                    row_value,
                    col_value,
                    row_col,
                    col_col
                )

                if is_correct:
                    st.session_state.swim_toe_board[i][j] = st.session_state.swim_toe_turn
                    st.session_state.swim_toe_answers[i][j] = matched_name
                    st.session_state.swim_toe_used_names.append(normalize_answer(matched_name))

                    new_winner = check_swim_game_winner(st.session_state.swim_toe_board)
                    st.session_state.swim_toe_winner = new_winner

                    if new_winner is None:
                        st.session_state.swim_toe_turn = "⭕" if st.session_state.swim_toe_turn == "❌" else "❌"

                    st.session_state.swim_toe_selected = None
                    st.success(f"Correct! {matched_name} claims the lane.")
                    st.rerun()

                else:
                    st.error("Wrong answer for this square. Try again.")

                    with st.expander("Show possible valid answers for this square"):
                        if possible_answers:
                            st.write(", ".join(possible_answers[:20]))
                        else:
                            st.write("No valid answers available in the dataset.")

    st.markdown("---")

    with st.expander("Used swimmers in this game"):
        if st.session_state.swim_toe_used_names:
            shown_used = [
                st.session_state.swim_toe_answers[i][j]
                for i in range(3)
                for j in range(3)
                if st.session_state.swim_toe_answers[i][j] != ""
            ]
            st.write(", ".join(shown_used))
        else:
            st.write("No swimmer used yet.")

    with st.expander("Why this game belongs in the app"):
        st.markdown(
            """
            This game turns passive exploration into active recall.
            After browsing the records, users can test whether they remember the links between
            swimmers, events, places and historical record moments.
            """
        )