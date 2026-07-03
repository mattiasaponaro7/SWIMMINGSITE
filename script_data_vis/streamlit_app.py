# %%
import re
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SwimStats Pro",
    page_icon="🏊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 180, 216, 0.18), transparent 34%),
            radial-gradient(circle at bottom right, rgba(3, 4, 94, 0.22), transparent 32%),
            linear-gradient(135deg, #f5fbff 0%, #e9f7ff 45%, #ffffff 100%);
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #061a40 0%, #003566 55%, #0077b6 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    .main-title {
        font-size: 56px;
        font-weight: 800;
        line-height: 1.02;
        color: #061a40;
        margin-bottom: 8px;
    }

    .subtitle {
        font-size: 18px;
        color: #415a77;
        max-width: 850px;
        line-height: 1.5;
        margin-bottom: 24px;
    }

    .section-title {
        font-size: 34px;
        font-weight: 800;
        color: #061a40;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.82);
        border: 1px solid rgba(0, 119, 182, 0.18);
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 18px 45px rgba(0, 53, 102, 0.10);
    }

    .metric-number {
        font-size: 34px;
        font-weight: 800;
        color: #0077b6;
    }

    .metric-label {
        font-size: 14px;
        color: #415a77;
        margin-top: 4px;
        font-weight: 600;
    }

    .pool-wrapper {
        margin-top: 26px;
        background:
            linear-gradient(90deg, rgba(255,255,255,0.16) 0%, rgba(255,255,255,0.05) 100%),
            linear-gradient(180deg, #0077b6 0%, #0096c7 50%, #00b4d8 100%);
        border-radius: 30px;
        padding: 22px;
        box-shadow: 0 28px 70px rgba(0, 53, 102, 0.28);
        border: 5px solid rgba(255, 255, 255, 0.75);
        position: relative;
        overflow: hidden;
    }

    .pool-wrapper:before {
        content: "";
        position: absolute;
        inset: 0;
        background-image:
            linear-gradient(90deg, rgba(255,255,255,0.16) 1px, transparent 1px),
            linear-gradient(180deg, rgba(255,255,255,0.09) 1px, transparent 1px);
        background-size: 52px 52px;
        pointer-events: none;
    }

    .lane-link {
        text-decoration: none !important;
    }

    .lane {
        position: relative;
        z-index: 2;
        display: flex;
        align-items: center;
        justify-content: space-between;
        min-height: 72px;
        margin: 10px 0;
        padding: 0 24px;
        border-radius: 18px;
        background:
            linear-gradient(90deg, rgba(3, 4, 94, 0.35), rgba(0, 119, 182, 0.28)),
            repeating-linear-gradient(
                90deg,
                rgba(255,255,255,0.16) 0px,
                rgba(255,255,255,0.16) 18px,
                transparent 18px,
                transparent 36px
            );
        border-top: 3px solid rgba(255,255,255,0.72);
        border-bottom: 3px solid rgba(255,255,255,0.72);
        color: white;
        transition: all 0.25s ease;
        box-shadow: inset 0 0 24px rgba(255,255,255,0.10);
    }

    .lane:hover {
        transform: translateX(10px) scale(1.012);
        background:
            linear-gradient(90deg, rgba(144, 224, 239, 0.85), rgba(0, 180, 216, 0.78)),
            repeating-linear-gradient(
                90deg,
                rgba(255,255,255,0.25) 0px,
                rgba(255,255,255,0.25) 18px,
                transparent 18px,
                transparent 36px
            );
        box-shadow:
            0 0 28px rgba(72, 202, 228, 0.95),
            inset 0 0 30px rgba(255,255,255,0.35);
        cursor: pointer;
    }

    .lane-left {
        display: flex;
        align-items: center;
        gap: 18px;
    }

    .lane-number {
        width: 42px;
        height: 42px;
        border-radius: 50%;
        background: rgba(255,255,255,0.92);
        color: #0077b6;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        font-size: 18px;
    }

    .lane-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: 0.2px;
        color: white;
    }

    .lane-subtitle {
        font-size: 13px;
        opacity: 0.92;
        color: white;
    }

    .lane-arrow {
        font-size: 24px;
        font-weight: 800;
        color: white;
    }

    .small-card {
        background: rgba(255,255,255,0.84);
        border: 1px solid rgba(0, 119, 182, 0.16);
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 14px 35px rgba(0, 53, 102, 0.08);
    }

    .record-card {
        background: linear-gradient(135deg, #ffffff 0%, #eaf8ff 100%);
        border-left: 7px solid #00b4d8;
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 14px;
        box-shadow: 0 12px 30px rgba(0, 53, 102, 0.10);
    }

    .record-title {
        font-size: 20px;
        font-weight: 800;
        color: #061a40;
    }

    .record-sub {
        color: #415a77;
        margin-top: 4px;
        font-size: 14px;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
    }

    .footer-note {
        color: #5c677d;
        font-size: 13px;
        margin-top: 25px;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DATA LOADING
# ============================================================

DATA_PATH = Path("Swimming database .xlsx")


def parse_time_to_seconds(value):
    """
    Converts different swimming time formats into seconds.
    Examples:
    - 46.86 -> 46.86
    - "1:44.65" -> 104.65
    - "0:0:46:86" -> 46.86
    """
    if pd.isna(value):
        return None

    value = str(value).strip()

    try:
        return float(value)
    except ValueError:
        pass

    parts = value.split(":")

    try:
        if len(parts) == 4:
            h, m, s, ff = parts
            return int(h) * 3600 + int(m) * 60 + int(s) + int(ff) / 100

        if len(parts) == 3:
            h, m, s = parts
            return int(h) * 3600 + int(m) * 60 + float(s)

        if len(parts) == 2:
            m, s = parts
            return int(m) * 60 + float(s)

    except ValueError:
        return None

    return None


def extract_distance(event_description):
    if pd.isna(event_description):
        return None

    match = re.search(r"\b(\d{2,4})\b", str(event_description))
    if match:
        return int(match.group(1))

    return None


def extract_stroke(event_description):
    if pd.isna(event_description):
        return "Other"

    text = str(event_description).lower()

    if "freestyle" in text:
        return "Freestyle"
    if "backstroke" in text:
        return "Backstroke"
    if "breaststroke" in text:
        return "Breaststroke"
    if "butterfly" in text:
        return "Butterfly"
    if "medley" in text:
        return "Medley"
    if "relay" in text:
        return "Relay"

    return "Other"


def extract_course(event_description):
    if pd.isna(event_description):
        return None

    text = str(event_description).upper()

    if "LCM" in text:
        return "LCM"
    if "SCM" in text:
        return "SCM"

    return None


def clean_gender(value):
    if pd.isna(value):
        return None

    value = str(value).strip().upper()

    if value in ["M", "MALE", "MEN"]:
        return "Men"
    if value in ["F", "FEMALE", "WOMEN"]:
        return "Women"

    return value


@st.cache_data
def load_data(uploaded_file=None):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel(DATA_PATH)

    df.columns = [c.strip() for c in df.columns]

    df["Seconds"] = df["Swim time"].apply(parse_time_to_seconds)

    if df["Seconds"].isna().sum() > 0 and "Duration (hh:mm:ss:ff)" in df.columns:
        df["Seconds"] = df["Seconds"].fillna(
            df["Duration (hh:mm:ss:ff)"].apply(parse_time_to_seconds)
        )

    df["Gender Clean"] = df["Gender"].apply(clean_gender)
    df["Distance"] = df["Event description"].apply(extract_distance)
    df["Stroke"] = df["Event description"].apply(extract_stroke)
    df["Course"] = df["Event description"].apply(extract_course)

    df["Swim date"] = pd.to_datetime(df["Swim date"], errors="coerce")
    df["Athlete birth date"] = pd.to_datetime(df["Athlete birth date"], errors="coerce")

    df = df.sort_values(["Event description", "Seconds", "Rank_Order"], ascending=True)

    return df


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("## 🏊 SwimStats Pro")
st.sidebar.markdown("Top swimming performances database")

uploaded_file = st.sidebar.file_uploader(
    "Upload your swimming Excel file",
    type=["xlsx", "xls"]
)

try:
    df = load_data(uploaded_file)
except FileNotFoundError:
    st.error(
        "Non trovo il file Excel. Metti `Swimming database .xlsx` nella stessa cartella di questo `app.py`, "
        "oppure caricalo dalla sidebar."
    )
    st.stop()

pages = [
    "Dashboard",
    "Top 200 Results",
    "Compare Athletes",
    "Events & WRs",
    "Reaction Test"
]

query_page = st.query_params.get("page", "Dashboard")
if query_page not in pages:
    query_page = "Dashboard"

page = st.sidebar.radio(
    "Navigation",
    pages,
    index=pages.index(query_page)
)

st.query_params["page"] = page


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def show_metric_card(number, label):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-number">{number}</div>
            <div class="metric-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def apply_filters(data, selected_gender, selected_stroke, selected_distance, selected_event):
    filtered = data.copy()

    if selected_gender != "All":
        filtered = filtered[filtered["Gender Clean"] == selected_gender]

    if selected_stroke != "All":
        filtered = filtered[filtered["Stroke"] == selected_stroke]

    if selected_distance != "All":
        filtered = filtered[filtered["Distance"] == selected_distance]

    if selected_event != "All":
        filtered = filtered[filtered["Event description"] == selected_event]

    return filtered


def display_results_table(data, max_rows=200):
    cols = [
        "Rank_Order",
        "Athlete Full Name",
        "Gender Clean",
        "Event description",
        "Swim time",
        "Seconds",
        "Swim date",
        "Event Name",
        "City",
        "Country Code",
        "Team Code"
    ]

    available_cols = [c for c in cols if c in data.columns]

    table = data[available_cols].head(max_rows).copy()

    rename_map = {
        "Rank_Order": "Rank",
        "Athlete Full Name": "Athlete",
        "Gender Clean": "Gender",
        "Event description": "Event",
        "Swim time": "Time",
        "Seconds": "Seconds",
        "Swim date": "Date",
        "Event Name": "Competition",
        "Country Code": "Country",
        "Team Code": "Team"
    }

    table = table.rename(columns=rename_map)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )


def lane_href(page_name, stroke=None, gender=None):
    params = f"?page={page_name.replace(' ', '+')}"
    if stroke:
        params += f"&stroke={stroke}"
    if gender:
        params += f"&gender={gender}"
    return params


# ============================================================
# PAGE 1: DASHBOARD
# ============================================================

if page == "Dashboard":

    st.markdown('<div class="main-title">SwimStats Pro</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subtitle">
        Explore the best swimming performances through a visual interface inspired by swimming lanes.
        Each lane represents a race category: move the mouse over the lane to highlight it, then click to explore the top results.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        show_metric_card(f"{len(df):,}", "Total performances")

    with col2:
        show_metric_card(df["Athlete Full Name"].nunique(), "Unique athletes")

    with col3:
        show_metric_card(df["Event description"].nunique(), "Swimming events")

    with col4:
        show_metric_card(df["Country Code"].nunique(), "Countries")

    st.markdown("### Choose your lane")

    lanes = [
        ("1", "Freestyle", "Sprint and endurance freestyle events", "Freestyle"),
        ("2", "Backstroke", "Top backstroke performances", "Backstroke"),
        ("3", "Breaststroke", "Top breaststroke performances", "Breaststroke"),
        ("4", "Butterfly", "Top butterfly performances", "Butterfly"),
        ("5", "Medley", "Individual medley events", "Medley"),
        ("6", "Men", "Explore male swimming rankings", None),
        ("7", "Women", "Explore female swimming rankings", None),
        ("8", "All Events", "Full Top 200 swimming database", None),
    ]

    st.markdown('<div class="pool-wrapper">', unsafe_allow_html=True)

    for lane_number, title, subtitle, stroke in lanes:
        if title == "Men":
            href = lane_href("Top 200 Results", gender="Men")
        elif title == "Women":
            href = lane_href("Top 200 Results", gender="Women")
        elif title == "All Events":
            href = lane_href("Top 200 Results")
        else:
            href = lane_href("Top 200 Results", stroke=stroke)

        st.markdown(
            f"""
            <a class="lane-link" href="{href}">
                <div class="lane">
                    <div class="lane-left">
                        <div class="lane-number">{lane_number}</div>
                        <div>
                            <div class="lane-title">{title}</div>
                            <div class="lane-subtitle">{subtitle}</div>
                        </div>
                    </div>
                    <div class="lane-arrow">→</div>
                </div>
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Database overview")

    col_a, col_b = st.columns(2)

    with col_a:
        event_counts = (
            df.groupby("Stroke")
            .size()
            .reset_index(name="Number of results")
            .sort_values("Number of results", ascending=False)
        )

        fig = px.bar(
            event_counts,
            x="Stroke",
            y="Number of results",
            title="Results by stroke"
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        gender_counts = (
            df.groupby("Gender Clean")
            .size()
            .reset_index(name="Number of results")
        )

        fig = px.pie(
            gender_counts,
            names="Gender Clean",
            values="Number of results",
            title="Results by gender",
            hole=0.45
        )
        fig.update_layout(height=420)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 2: TOP 200 RESULTS
# ============================================================

elif page == "Top 200 Results":

    st.markdown('<div class="section-title">Top 200 Results</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subtitle">
        Filter the database by gender, stroke, distance and event. The table shows the best performances ordered by time.
        </div>
        """,
        unsafe_allow_html=True
    )

    query_stroke = st.query_params.get("stroke", "All")
    query_gender = st.query_params.get("gender", "All")

    genders = ["All"] + sorted(df["Gender Clean"].dropna().unique().tolist())
    strokes = ["All"] + sorted(df["Stroke"].dropna().unique().tolist())
    distances = ["All"] + sorted(df["Distance"].dropna().unique().tolist())

    if query_gender not in genders:
        query_gender = "All"

    if query_stroke not in strokes:
        query_stroke = "All"

    filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

    with filter_col1:
        selected_gender = st.selectbox(
            "Gender",
            genders,
            index=genders.index(query_gender)
        )

    with filter_col2:
        selected_stroke = st.selectbox(
            "Stroke",
            strokes,
            index=strokes.index(query_stroke)
        )

    with filter_col3:
        selected_distance = st.selectbox(
            "Distance",
            distances
        )

    temp = df.copy()

    if selected_gender != "All":
        temp = temp[temp["Gender Clean"] == selected_gender]

    if selected_stroke != "All":
        temp = temp[temp["Stroke"] == selected_stroke]

    if selected_distance != "All":
        temp = temp[temp["Distance"] == selected_distance]

    events = ["All"] + sorted(temp["Event description"].dropna().unique().tolist())

    with filter_col4:
        selected_event = st.selectbox(
            "Specific event",
            events
        )

    filtered = apply_filters(
        df,
        selected_gender,
        selected_stroke,
        selected_distance,
        selected_event
    )

    filtered = filtered.sort_values(["Seconds", "Rank_Order"], ascending=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric_card(f"{len(filtered):,}", "Filtered performances")

    with col2:
        show_metric_card(filtered["Athlete Full Name"].nunique(), "Athletes")

    with col3:
        if len(filtered) > 0:
            best_time = filtered.iloc[0]["Swim time"]
        else:
            best_time = "-"
        show_metric_card(best_time, "Best time")

    st.markdown("### Ranking table")
    display_results_table(filtered, max_rows=200)

    st.markdown("### Time distribution")

    if len(filtered) > 1:
        fig = px.scatter(
            filtered.head(200),
            x="Rank_Order",
            y="Seconds",
            hover_name="Athlete Full Name",
            hover_data=[
                "Swim time",
                "Event description",
                "Event Name",
                "City",
                "Country Code"
            ],
            title="Top 200 performances by rank"
        )
        fig.update_layout(height=460)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Select a broader filter to visualize the distribution.")


# ============================================================
# PAGE 3: COMPARE ATHLETES
# ============================================================

elif page == "Compare Athletes":

    st.markdown('<div class="section-title">Compare Athletes</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subtitle">
        Compare two swimmers across the same event or across all available performances.
        </div>
        """,
        unsafe_allow_html=True
    )

    athletes = sorted(df["Athlete Full Name"].dropna().unique().tolist())

    col1, col2 = st.columns(2)

    with col1:
        athlete_1 = st.selectbox("First athlete", athletes, index=0)

    with col2:
        athlete_2 = st.selectbox("Second athlete", athletes, index=min(1, len(athletes) - 1))

    both_df = df[df["Athlete Full Name"].isin([athlete_1, athlete_2])].copy()

    common_events = (
        both_df.groupby("Event description")["Athlete Full Name"]
        .nunique()
        .reset_index()
    )

    common_events = common_events[common_events["Athlete Full Name"] == 2]["Event description"].tolist()

    event_options = ["All common events"] + sorted(common_events)

    selected_compare_event = st.selectbox(
        "Compare on event",
        event_options
    )

    if selected_compare_event != "All common events":
        both_df = both_df[both_df["Event description"] == selected_compare_event]
    else:
        both_df = both_df[both_df["Event description"].isin(common_events)]

    if len(both_df) == 0:
        st.warning("No common event found for these two athletes.")
    else:
        best_by_athlete = (
            both_df.sort_values("Seconds")
            .groupby(["Athlete Full Name", "Event description"], as_index=False)
            .first()
        )

        st.markdown("### Best performances comparison")

        st.dataframe(
            best_by_athlete[
                [
                    "Athlete Full Name",
                    "Event description",
                    "Swim time",
                    "Seconds",
                    "Event Name",
                    "City",
                    "Country Code"
                ]
            ].rename(
                columns={
                    "Athlete Full Name": "Athlete",
                    "Event description": "Event",
                    "Swim time": "Time",
                    "Event Name": "Competition",
                    "Country Code": "Country"
                }
            ),
            use_container_width=True,
            hide_index=True
        )

        fig = px.bar(
            best_by_athlete,
            x="Event description",
            y="Seconds",
            color="Athlete Full Name",
            barmode="group",
            title="Best time comparison by event"
        )
        fig.update_layout(height=520, xaxis_title="Event", yaxis_title="Seconds")
        st.plotly_chart(fig, use_container_width=True)

        progression = both_df.dropna(subset=["Swim date"]).sort_values("Swim date")

        if len(progression) > 1:
            st.markdown("### Performance timeline")

            fig = px.line(
                progression,
                x="Swim date",
                y="Seconds",
                color="Athlete Full Name",
                markers=True,
                hover_data=["Swim time", "Event description", "Event Name", "City"],
                title="Time progression"
            )
            fig.update_layout(height=480, yaxis_title="Seconds")
            st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 4: EVENTS & WORLD RECORDS
# ============================================================

elif page == "Events & WRs":

    st.markdown('<div class="section-title">Events & Records</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subtitle">
        A summary of the best performance available in the database for each swimming event.
        </div>
        """,
        unsafe_allow_html=True
    )

    records = (
        df.sort_values(["Event description", "Seconds"], ascending=True)
        .groupby("Event description", as_index=False)
        .first()
        .sort_values(["Gender Clean", "Distance", "Stroke"])
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        show_metric_card(records["Event description"].nunique(), "Events")

    with col2:
        show_metric_card(records["Athlete Full Name"].nunique(), "Record holders")

    with col3:
        show_metric_card(records["Country Code"].nunique(), "Countries represented")

    st.markdown("### Event record cards")

    selected_record_stroke = st.selectbox(
        "Filter by stroke",
        ["All"] + sorted(records["Stroke"].dropna().unique().tolist())
    )

    selected_record_gender = st.selectbox(
        "Filter by gender",
        ["All"] + sorted(records["Gender Clean"].dropna().unique().tolist())
    )

    record_view = records.copy()

    if selected_record_stroke != "All":
        record_view = record_view[record_view["Stroke"] == selected_record_stroke]

    if selected_record_gender != "All":
        record_view = record_view[record_view["Gender Clean"] == selected_record_gender]

    for _, row in record_view.iterrows():
        date_text = "-"
        if pd.notna(row["Swim date"]):
            date_text = row["Swim date"].strftime("%d %b %Y")

        st.markdown(
            f"""
            <div class="record-card">
                <div class="record-title">{row['Event description']} · {row['Swim time']}</div>
                <div class="record-sub">
                    <b>{row['Athlete Full Name']}</b> · {row['Country Code']} · {row['Event Name']} · {row['City']} · {date_text}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("### Countries with most event-best performances")

    country_records = (
        records.groupby("Country Code")
        .size()
        .reset_index(name="Records")
        .sort_values("Records", ascending=False)
        .head(15)
    )

    fig = px.bar(
        country_records,
        x="Country Code",
        y="Records",
        title="Number of event-best performances by country"
    )
    fig.update_layout(height=430)
    st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE 5: REACTION TEST
# ============================================================

elif page == "Reaction Test":

    st.markdown('<div class="section-title">Reaction Test</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subtitle">
        A small interactive section inspired by swimming starts. In a full web version this could become a real reaction-time game.
        In Streamlit, we keep it as a simple prototype section.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="small-card">
            <h3 style="color:#061a40;">Start Reaction Prototype</h3>
            <p style="color:#415a77;">
            This page can be used later to create a small reaction-time game, useful to connect swimming rankings with start performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("### Example reaction benchmarks")

    reaction_data = pd.DataFrame(
        {
            "Level": ["Elite start", "Good start", "Average start", "Slow start"],
            "Reaction time range": ["0.60–0.70 s", "0.70–0.80 s", "0.80–0.95 s", ">0.95 s"],
            "Interpretation": [
                "Very fast response from the block",
                "Competitive reaction",
                "Acceptable but improvable",
                "Potential loss at the start"
            ]
        }
    )

    st.dataframe(reaction_data, use_container_width=True, hide_index=True)

    st.info(
        "For now this is only a visual/prototype page. Later we can add a real click-based reaction timer."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-note">
    SwimStats Pro · Streamlit version · Dataset loaded from Excel
    </div>
    """,
    unsafe_allow_html=True
)


