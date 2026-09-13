import streamlit as st
import sqlite3
import os
import html
import base64


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Business Insights",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

DATABASE_PATH = os.path.join(DATA_DIR, "business_insights.db")
DATABASE_ZIP_PATH = os.path.join(DATA_DIR, "business_insights.db.zip")


def ensure_database():
    """
    Ensure the SQLite database is available.

    The normal local database is used when present. On deployment,
    if only the compressed database is included, it is extracted
    automatically before SQLite connects to it.
    """
    if os.path.exists(DATABASE_PATH):
        return

    if not os.path.exists(DATABASE_ZIP_PATH):
        raise FileNotFoundError(
            "Database not found. Expected either "
            f"{DATABASE_PATH} or {DATABASE_ZIP_PATH}."
        )

    import zipfile

    with zipfile.ZipFile(DATABASE_ZIP_PATH, "r") as zip_file:
        if "business_insights.db" not in zip_file.namelist():
            raise FileNotFoundError(
                "The database ZIP does not contain business_insights.db."
            )

        zip_file.extract("business_insights.db", DATA_DIR)


ensure_database()

# ============================================================
# HOMEPAGE HERO IMAGE
# ============================================================

HERO_IMAGE_PATH = os.path.join(
    os.path.dirname(__file__),
    "hero_skyline.png"
)

HERO_IMAGE_DATA = ""

if os.path.exists(HERO_IMAGE_PATH):
    with open(HERO_IMAGE_PATH, "rb") as hero_file:
        HERO_IMAGE_DATA = base64.b64encode(
            hero_file.read()
        ).decode("utf-8")

@st.cache_resource
def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )

    # IMPORTANT:
    # Allows business["name"], business["stars"], etc.
    connection.row_factory = sqlite3.Row

    return connection


db = get_connection()


# ============================================================
# GLOBAL STREAMLIT CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL PAGE
    ======================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section.main {
        background-color: #080a0e !important;
        color: #f4f4f4 !important;
    }


    /* ========================================================
       STREAMLIT HEADER
    ======================================================== */

    [data-testid="stHeader"] {
        background-color: #080a0e !important;
        z-index: 1000 !important;
    }

    [data-testid="stDecoration"] {
        background-color: #080a0e !important;
    }


    /* ========================================================
       MAIN CONTENT
    ======================================================== */

    .block-container {
        max-width: 1280px !important;
        padding-top: 4.5rem !important;
        padding-bottom: 4rem !important;
    }


    /* ========================================================
       FORCE SMALL INLINE TEXT TO BE READABLE
       IMPORTANT: THESE OVERRIDE THE INLINE FONT SIZES
    ======================================================== */

    [style*="font-size:8px"] {
        font-size: 11px !important;
    }

    [style*="font-size:9px"] {
        font-size: 12px !important;
    }

    [style*="font-size:10px"] {
        font-size: 13px !important;
    }

    [style*="font-size:11px"] {
        font-size: 14px !important;
    }

    [style*="font-size:12px"] {
        font-size: 14px !important;
    }

    [style*="font-size:13px"] {
        font-size: 15px !important;
    }

    [style*="font-size:14px"] {
        font-size: 15px !important;
    }

    [style*="font-size:15px"] {
        font-size: 16px !important;
    }

    [style*="font-size:16px"] {
        font-size: 17px !important;
    }

    [style*="font-size:17px"] {
        font-size: 18px !important;
    }


    /* ========================================================
       SEARCH INPUT
    ======================================================== */

    div[data-baseweb="input"] {
        background-color: #111419 !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
        border-radius: 10px !important;
        box-shadow: none !important;
    }

    div[data-baseweb="input"] > div {
        background-color: #111419 !important;
        border-radius: 10px !important;
    }

    div[data-baseweb="input"] input {
        background-color: #111419 !important;
        color: #f4f4f4 !important;
        -webkit-text-fill-color: #f4f4f4 !important;
        caret-color: #e52b50 !important;

        font-size: 16px !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #777 !important;
        -webkit-text-fill-color: #777 !important;
        font-size: 16px !important;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #e52b50 !important;
    }


    /* ========================================================
       STREAMLIT LABELS
    ======================================================== */

    label {
        color: #999 !important;
        font-size: 15px !important;
    }


    /* ========================================================
       BUTTONS
    ======================================================== */

    .stButton > button {
        width: 100% !important;
        min-height: 46px !important;

        background: #e52b50 !important;
        color: #ffffff !important;

        border: 1px solid #e52b50 !important;
        border-radius: 9px !important;

        font-size: 14px !important;
        font-weight: 700 !important;

        box-shadow: none !important;
    }

    .stButton > button:hover {
        background: #ff3d64 !important;
        color: #ffffff !important;

        border-color: #ff3d64 !important;

        box-shadow:
            0 0 18px
            rgba(229,43,80,0.20) !important;
    }

    /* ========================================================
       ALERT
    ======================================================== */

    [data-testid="stAlert"] {
        background-color: #111419 !important;
        color: #f4f4f4 !important;

        border: 1px solid rgba(255,255,255,0.08) !important;

        font-size: 14px !important;
    }


    /* ========================================================
       CAPTION
    ======================================================== */

    [data-testid="stCaptionContainer"] {
        color: #777 !important;
        font-size: 13px !important;
    }


    /* ========================================================
       GENERAL STREAMLIT MARKDOWN
    ======================================================== */

    [data-testid="stMarkdownContainer"] {
        color: #f4f4f4;
    }


    /* ========================================================
       SCROLLBAR
    ======================================================== */

    ::-webkit-scrollbar {
        width: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #080a0e;
    }

    ::-webkit-scrollbar-thumb {
        background: #25282e;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #3a3e46;
    }


    /* ========================================================
       MOBILE
    ======================================================== */

    @media (max-width: 700px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        [style*="font-size:9px"] {
            font-size: 11px !important;
        }

        [style*="font-size:10px"] {
            font-size: 12px !important;
        }

        [style*="font-size:11px"] {
            font-size: 13px !important;
        }

    }


    /* ========================================================
       PRINT
    ======================================================== */

    @media print {

        html,
        body,
        .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stMain"] {

            background-color: #080a0e !important;
            color: #f4f4f4 !important;

            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

    }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HTML HELPER
# ============================================================

def show_html(content):

    st.html(content)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


if "business_type" not in st.session_state:

    st.session_state.business_type = None


if "business_id" not in st.session_state:

    st.session_state.business_id = None


# ============================================================
# SCROLL TO TOP WHEN PAGE CHANGES
# ============================================================

if "previous_page" not in st.session_state:
    st.session_state.previous_page = st.session_state.page

page_changed = (
    st.session_state.previous_page != st.session_state.page
)

st.session_state.previous_page = st.session_state.page

if page_changed:
    st.html(
        """
        <script>
            window.parent.scrollTo(0, 0);
            document.documentElement.scrollTop = 0;
            document.body.scrollTop = 0;
        </script>
        """
    )


# ============================================================
# DATABASE FUNCTIONS
# ============================================================

def get_businesses(category, search_text=""):

    if search_text.strip():

        rows = db.execute(
            """
            SELECT
                business_id,
                name,
                city,
                state,
                business_category,
                stars,
                review_count
            FROM businesses

            WHERE business_category = ?
              AND name LIKE ?

            ORDER BY
                review_count DESC,
                name ASC

            LIMIT 30
            """,
            (
                category,
                "%" + search_text.strip() + "%"
            )
        ).fetchall()

    else:

        rows = db.execute(
            """
            SELECT
                business_id,
                name,
                city,
                state,
                business_category,
                stars,
                review_count
            FROM businesses

            WHERE business_category = ?

            ORDER BY
                review_count DESC

            LIMIT 30
            """,
            (category,)
        ).fetchall()

    return rows


def get_business(business_id):

    return db.execute(
        """
        SELECT *
        FROM businesses
        WHERE business_id = ?
        """,
        (business_id,)
    ).fetchone()


def get_aspects(business_id):

    return db.execute(
        """
        SELECT
            aspect,
            aspect_mentions,
            positive_mentions,
            neutral_mentions,
            negative_mentions,
            positive_percentage,
            neutral_percentage,
            negative_percentage

        FROM business_aspects

        WHERE business_id = ?

        ORDER BY aspect_mentions DESC
        """,
        (business_id,)
    ).fetchall()


def get_opportunity_data(category_filter="All"):

    query = """
        SELECT
            city,
            state,
            business_category,
            COUNT(*) AS business_count,
            AVG(stars) AS average_rating,
            SUM(total_reviews) AS total_reviews,
            AVG(business_health_score) AS average_health_score,
            AVG(negative_percentage) AS average_negative_percentage
        FROM businesses
        WHERE business_category IN (
            'Restaurant', 'Grocery', 'Healthcare', 'Auto Repair'
        )
    """

    params = []

    if category_filter != "All":
        query += " AND business_category = ? "
        params.append(category_filter)

    query += """
        GROUP BY city, state, business_category
        ORDER BY total_reviews DESC
    """

    rows = db.execute(query, params).fetchall()

    if not rows:
        return []

    # Same scoring logic used in the Spark opportunity analysis:
    # demand is based on log review volume and competition on business count.
    import math

    max_demand = max(
        math.log1p(row["total_reviews"] or 0)
        for row in rows
    ) or 1

    max_competition = max(
        row["business_count"] or 0
        for row in rows
    ) or 1

    opportunities = []

    for row in rows:

        demand = math.log1p(row["total_reviews"] or 0)
        demand_normalized = (demand / max_demand) * 100

        competition_normalized = (
            (row["business_count"] or 0) / max_competition
        ) * 100

        opportunity_score = (
            demand_normalized * 0.60
            + (100 - competition_normalized) * 0.40
        )

        opportunities.append({
            "city": row["city"] or "Unknown",
            "state": row["state"] or "",
            "business_category": row["business_category"],
            "business_count": row["business_count"] or 0,
            "average_rating": row["average_rating"] or 0,
            "total_reviews": row["total_reviews"] or 0,
            "average_health_score": row["average_health_score"] or 0,
            "average_negative_percentage": row["average_negative_percentage"] or 0,
            "opportunity_score": opportunity_score
        })

    return sorted(
        opportunities,
        key=lambda x: x["opportunity_score"],
        reverse=True
    )


# ============================================================
# NAVIGATION BAR
# ============================================================

show_html(
    """
    <div style="
        display:flex;
        justify-content:space-between;
        align-items:center;

        padding:10px 0 22px 0;

        border-bottom:
            1px solid rgba(255,255,255,0.08);
    ">

        <div style="
            color:#ffffff;
            font-size:19px;
            font-weight:800;
            letter-spacing:-0.5px;
        ">

            BUSINESS
            <span style="color:#e52b50;">
                INSIGHTS
            </span>

        </div>


        <div style="
            color:#666;
            font-size:9px;
            letter-spacing:1px;
        ">

            DATA-DRIVEN DECISIONS FOR A BETTER TOMORROW

        </div>

    </div>
    """
)


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    if HERO_IMAGE_DATA:

        show_html(
            f"""
            <div style="
                position:relative;
                overflow:hidden;

                min-height:365px;

                margin-top:18px;

                border-radius:18px;

                background:#05080c;
            ">

                <!-- HERO IMAGE -->
                <img
                    src="data:image/png;base64,{HERO_IMAGE_DATA}"
                    style="
                        position:absolute;
                        top:0;
                        right:0;

                        width:100%;
                        height:100%;

                        object-fit:cover;
                        object-position:center;

                        z-index:0;

                        opacity:0.85;
                    "
                >


                <!-- DARK OVERLAY -->
                <div style="
                    position:absolute;
                    inset:0;

                    background:
                        linear-gradient(
                            90deg,
                            rgba(5,8,12,0.98) 0%,
                            rgba(5,8,12,0.92) 28%,
                            rgba(5,8,12,0.60) 58%,
                            rgba(5,8,12,0.25) 100%
                        );

                    z-index:1;
                "></div>


                <!-- HERO CONTENT -->
                <div style="
                    position:relative;

                    z-index:2;

                    padding:
                        58px
                        42px
                        48px
                        0;

                    max-width:900px;
                ">

                    <div style="
                        color:#e52b50;

                        font-size:12px;

                        font-weight:800;

                        letter-spacing:2.5px;

                        margin-left:0;
                    ">

                        INTELLIGENT BUSINESS DISCOVERY

                    </div>


                    <div style="
                        color:#f4f4f4;

                        font-size:64px;

                        font-weight:800;

                        line-height:0.98;

                        letter-spacing:-4px;

                        margin-top:14px;
                    ">

                        Discover<br>

                        Business

                        <span style="
                            color:#e52b50;
                        ">

                            Potential.

                        </span>

                    </div>


                    <div style="
                        max-width:760px;

                        color:#c0cad7;

                        font-size:15px;

                        line-height:1.65;

                        margin-top:23px;
                    ">

                        Explore real business intelligence using Yelp Big Data.
                        Analyze customer sentiment, ratings, review activity,
                        business health and risk to make informed decisions.

                    </div>

                </div>


                <!-- TAGLINE -->
                <div style="
                    position:absolute;

                    right:48px;

                    top:58px;

                    z-index:3;

                    color:#ffffff;

                    font-family:cursive;

                    font-size:18px;

                    line-height:1.15;

                    transform:rotate(-5deg);

                    text-align:left;
                ">

                    Better Businesses<br>

                    Stronger Communities


                    <div style="
                        width:120px;

                        height:2px;

                        background:#e52b50;

                        margin:
                            8px 0 0 35px;

                        transform:rotate(-3deg);
                    "></div>

                </div>

            </div>
            """
        )

    else:

        # Fallback if hero_skyline.png is missing

        show_html(
            """
            <div style="
                min-height:365px;

                margin-top:18px;

                border-radius:18px;

                background:#05080c;

                padding:58px 42px 48px 0;
            ">

                <div style="
                    color:#e52b50;

                    font-size:12px;

                    font-weight:800;

                    letter-spacing:2.5px;
                ">

                    INTELLIGENT BUSINESS DISCOVERY

                </div>


                <div style="
                    color:#f4f4f4;

                    font-size:64px;

                    font-weight:800;

                    line-height:0.98;

                    letter-spacing:-4px;

                    margin-top:14px;
                ">

                    Discover<br>

                    Business

                    <span style="
                        color:#e52b50;
                    ">

                        Potential.

                    </span>

                </div>


                <div style="
                    max-width:760px;

                    color:#c0cad7;

                    font-size:15px;

                    line-height:1.65;

                    margin-top:23px;
                ">

                    Explore real business intelligence using Yelp Big Data.
                    Analyze customer sentiment, ratings, review activity,
                    business health and risk to make informed decisions.

                </div>

            </div>
            """
        )

    # --------------------------------------------------------
    # DATASET STATISTICS
    # --------------------------------------------------------

    columns = st.columns(4)


    stats = [
        ("150,346", "BUSINESS RECORDS"),
        ("6.99M", "REVIEW RECORDS"),
        ("4", "FOCUS INDUSTRIES"),
        ("100+", "CITIES")
    ]


    for column, (number, label) in zip(
        columns,
        stats
    ):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:15px;

                    padding:23px;

                    min-height:105px;
                ">

                    <div style="
                        color:#f4f4f4;
                        font-size:29px;
                        font-weight:750;
                    ">

                        {number}

                    </div>


                    <div style="
                        color:#666;
                        font-size:8px;
                        letter-spacing:1.3px;
                        margin-top:7px;
                    ">

                        {label}

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # SELECT BUSINESS TYPE
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:65px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                SELECT BUSINESS TYPE

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                letter-spacing:-1px;
                margin-top:8px;
            ">

                What type of business would you like to explore?

            </div>


            <div style="
                color:#777;
                font-size:12px;
                margin-top:8px;
            ">

                Choose a business category to begin your analysis journey.

            </div>

        </div>
        """
    )


    industries = [

        (
            "🍴",
            "Restaurant",
            "Cafes, dining, food and restaurant businesses."
        ),

        (
            "🛒",
            "Grocery",
            "Supermarkets, grocery stores and food retail."
        ),

        (
            "♥",
            "Healthcare",
            "Hospitals, clinics and medical businesses."
        ),

        (
            "⚒",
            "Auto Repair",
            "Car repair, maintenance and automotive services."
        )

    ]


    columns = st.columns(4)


    for column, (icon, name, description) in zip(
        columns,
        industries
    ):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:16px;

                    padding:25px;

                    min-height:145px;
                ">

                    <div style="
                        font-size:25px;
                        margin-bottom:17px;
                    ">

                        {icon}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:17px;
                        font-weight:700;
                    ">

                        {name}

                    </div>


                    <div style="
                        color:#666;
                        font-size:10px;
                        line-height:1.6;
                        margin-top:7px;
                    ">

                        {description}

                    </div>

                </div>
                """
            )


            if st.button(
                f"Explore {name}",
                key=f"industry_{name}"
            ):

                st.session_state.business_type = name

                st.session_state.page = "select"

                st.rerun()


    # --------------------------------------------------------
    # OPPORTUNITY DISCOVERY
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:65px;
            margin-bottom:22px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">
                MARKET OPPORTUNITY
            </div>

            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">
                Find Promising Business Markets
            </div>

            <div style="
                color:#777;
                font-size:12px;
                margin-top:8px;
            ">
                Discover city and industry combinations with strong customer demand and lower competition.
            </div>

        </div>
        """
    )

    opportunity_columns = st.columns([4, 1])

    with opportunity_columns[0]:
        show_html(
            """
            <div style="
                background:#111419;
                border:1px solid rgba(255,255,255,0.08);
                border-radius:15px;
                padding:22px;
                color:#777;
                font-size:11px;
                line-height:1.7;
            ">
                The opportunity score combines normalized review demand (60%) and inverse competition (40%) to rank market opportunities.
            </div>
            """
        )

    with opportunity_columns[1]:
        if st.button("Explore Opportunities", key="home_opportunities"):
            st.session_state.page = "opportunity"
            st.rerun()


    # --------------------------------------------------------
    # HOW IT WORKS
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:65px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                HOW IT WORKS

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                From Big Data to Business Insights

            </div>

        </div>
        """
    )


    steps = [

        (
            "01",
            "Choose Business Type",
            "Select one of our focus industries."
        ),

        (
            "02",
            "Find a Business",
            "Search and select a specific business."
        ),

        (
            "03",
            "Get Insights",
            "View detailed business intelligence."
        ),

        (
            "04",
            "Explore Opportunities",
            "Use business health, risk and market analysis."
        )

    ]


    columns = st.columns(4)


    for column, (number, title, description) in zip(
        columns,
        steps
    ):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:16px;

                    padding:25px;

                    min-height:135px;
                ">

                    <div style="
                        color:#e52b50;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:2px;
                    ">

                        {number}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:15px;
                        font-weight:700;
                        margin-top:12px;
                    ">

                        {title}

                    </div>


                    <div style="
                        color:#666;
                        font-size:10px;
                        line-height:1.6;
                        margin-top:7px;
                    ">

                        {description}

                    </div>

                </div>
                """
            )


# ============================================================
# OPPORTUNITY DISCOVERY
# ============================================================

elif st.session_state.page == "opportunity":

    if st.button("← Back to Home", key="opportunity_back"):
        st.session_state.page = "home"
        st.rerun()

    show_html(
        """
        <div style="margin-top:50px; margin-bottom:30px;">

            <div style="color:#e52b50; font-size:9px; font-weight:700; letter-spacing:2px;">
                MARKET OPPORTUNITY ANALYSIS
            </div>

            <div style="color:#f4f4f4; font-size:42px; font-weight:800; letter-spacing:-2px; margin-top:10px;">
                Where Is the Opportunity?
            </div>

            <div style="color:#777; font-size:12px; line-height:1.7; margin-top:8px; max-width:760px;">
                City and industry combinations are ranked using customer review demand and business competition from the Yelp dataset.
            </div>

        </div>
        """
    )

    selected_category = st.selectbox(
        "Industry",
        ["All", "Restaurant", "Grocery", "Healthcare", "Auto Repair"],
        key="opportunity_category"
    )

    opportunities = get_opportunity_data(selected_category)

    if opportunities:

        top = opportunities[:10]

        show_html(
            f"""
            <div style="margin-top:35px; margin-bottom:22px;">
                <div style="color:#e52b50; font-size:9px; font-weight:700; letter-spacing:2px;">
                    TOP MARKETS
                </div>
                <div style="color:#f4f4f4; font-size:29px; font-weight:750; margin-top:8px;">
                    Highest Opportunity Markets
                </div>
                <div style="color:#777; font-size:12px; margin-top:8px;">
                    Showing the top {len(top)} city-industry combinations by opportunity score.
                </div>
            </div>
            """
        )

        for index, item in enumerate(top, 1):

            location = f"{item['city']}, {item['state']}" if item['state'] else item['city']

            show_html(
                f"""
                <div style="
                    background:#111419;
                    border:1px solid rgba(255,255,255,0.08);
                    border-radius:16px;
                    padding:23px;
                    margin-bottom:14px;
                ">

                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div style="color:#666; font-size:8px; font-weight:700; letter-spacing:1.4px;">
                                #{index} · {html.escape(item['business_category'])}
                            </div>
                            <div style="color:#f4f4f4; font-size:19px; font-weight:700; margin-top:8px;">
                                {html.escape(location)}
                            </div>
                        </div>

                        <div style="text-align:right;">
                            <div style="color:#e52b50; font-size:27px; font-weight:800;">
                                {item['opportunity_score']:.1f}
                            </div>
                            <div style="color:#666; font-size:8px; letter-spacing:1px; margin-top:3px;">
                                OPPORTUNITY SCORE
                            </div>
                        </div>
                    </div>

                    <div style="display:flex; gap:28px; margin-top:18px; flex-wrap:wrap;">
                        <div><span style="color:#666; font-size:9px;">BUSINESSES</span><br><span style="color:#f4f4f4; font-size:14px;">{item['business_count']:,}</span></div>
                        <div><span style="color:#666; font-size:9px;">AVG RATING</span><br><span style="color:#f4f4f4; font-size:14px;">{item['average_rating']:.2f} / 5</span></div>
                        <div><span style="color:#666; font-size:9px;">REVIEWS</span><br><span style="color:#f4f4f4; font-size:14px;">{item['total_reviews']:,}</span></div>
                        <div><span style="color:#666; font-size:9px;">AVG HEALTH</span><br><span style="color:#f4f4f4; font-size:14px;">{item['average_health_score']:.1f}</span></div>
                        <div><span style="color:#666; font-size:9px;">NEGATIVE FEEDBACK</span><br><span style="color:#f4f4f4; font-size:14px;">{item['average_negative_percentage']:.1f}%</span></div>
                    </div>

                </div>
                """
            )

        st.caption(
            "Opportunity score is calculated from review demand (60%) and inverse business competition (40%). It is a market-ranking indicator, not a guarantee of business success."
        )

    else:
        st.info("No opportunity data is available for the selected industry.")


# ============================================================
# BUSINESS SELECTION
# ============================================================

elif st.session_state.page == "select":

    category = st.session_state.business_type


    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    if st.button("← Back to Home"):

        st.session_state.page = "home"

        st.rerun()


    # --------------------------------------------------------
    # PAGE HEADER
    # --------------------------------------------------------

    show_html(
        f"""
        <div style="
            margin-top:50px;
            margin-bottom:30px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                STEP 2 OF 3

            </div>


            <div style="
                color:#f4f4f4;
                font-size:42px;
                font-weight:800;
                letter-spacing:-2px;
                margin-top:10px;
            ">

                Find a Business

            </div>


            <div style="
                color:#777;
                font-size:12px;
                line-height:1.7;
                margin-top:8px;
            ">

                Search and select a
                {html.escape(category.lower())}
                to analyze its performance,
                customer feedback and business health.

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SEARCH
    # --------------------------------------------------------

    search_text = st.text_input(
        "Business name",
        placeholder="Search for a business...",
        key="business_search"
    )


    businesses = get_businesses(
        category,
        search_text
    )


    # --------------------------------------------------------
    # RESULTS
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            color:#e52b50;
            font-size:9px;
            font-weight:700;
            letter-spacing:2px;
            margin:25px 0 12px 0;
        ">

            BUSINESS RESULTS

        </div>
        """
    )


    if not businesses:

        st.info(
            "No businesses found. Try another search."
        )

    else:

        for business in businesses:

            name = html.escape(
                business["name"] or ""
            )

            city = html.escape(
                business["city"] or ""
            )

            state = html.escape(
                business["state"] or ""
            )


            columns = st.columns(
                [5, 1, 1]
            )


            with columns[0]:

                show_html(
                    f"""
                    <div style="
                        background:#111419;

                        border:
                            1px solid
                            rgba(255,255,255,0.08);

                        border-radius:15px;

                        padding:20px;

                        min-height:100px;
                    ">

                        <div style="
                            color:#666;
                            font-size:8px;
                            letter-spacing:1.4px;
                            font-weight:700;
                        ">

                            {business["business_category"]}

                        </div>


                        <div style="
                            color:#f4f4f4;
                            font-size:19px;
                            font-weight:700;
                            margin-top:9px;
                        ">

                            {name}

                        </div>


                        <div style="
                            color:#666;
                            font-size:10px;
                            margin-top:6px;
                        ">

                            {city},
                            {state}
                            ·
                            {business["review_count"]:,}
                            reviews

                        </div>

                    </div>
                    """
                )


            with columns[1]:

                show_html(
                    f"""
                    <div style="
                        text-align:center;
                        padding-top:35px;
                        color:#aaa;
                        font-size:14px;
                    ">

                        ★ {business["stars"]:.1f}

                    </div>
                    """
                )


            with columns[2]:

                if st.button(
                    "Select",
                    key="select_" + business["business_id"]
                ):

                    st.session_state.business_id = (
                        business["business_id"]
                    )

                    st.session_state.page = "result"

                    st.rerun()


# ============================================================
# BUSINESS RESULT
# ============================================================

elif st.session_state.page == "result":

    business = get_business(
        st.session_state.business_id
    )


    if business is None:

        st.error("Business not found.")

        if st.button("Return Home"):

            st.session_state.page = "home"

            st.rerun()

        st.stop()


    # --------------------------------------------------------
    # BACK
    # --------------------------------------------------------

    if st.button("← Analyze Another Business"):

        st.session_state.page = "select"

        st.rerun()


    # --------------------------------------------------------
    # BUSINESS HEADER
    # --------------------------------------------------------

    show_html(
        f"""
        <div style="
            margin-top:45px;
            margin-bottom:30px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                STEP 3 OF 3

            </div>


            <div style="
                color:#f4f4f4;
                font-size:48px;
                font-weight:800;
                letter-spacing:-3px;
                margin-top:10px;
            ">

                {html.escape(business["name"])}

            </div>


            <div style="
                color:#888;
                font-size:13px;
                margin-top:10px;
            ">

                {html.escape(business["business_category"])}

                &nbsp;•&nbsp;

                {html.escape(business["city"] or "")},

                {html.escape(business["state"] or "")}

            </div>


            <div style="
                color:#666;
                font-size:11px;
                margin-top:7px;
            ">

                {html.escape(
                    business["address"] or
                    "Address unavailable"
                )}

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # HEALTH STATUS
    # --------------------------------------------------------

    if business["health_status"] == "Healthy":

        health_color = "#59d99e"

        health_background = (
            "rgba(89,217,158,0.10)"
        )

    elif business["health_status"] == "Moderate":

        health_color = "#e5c05b"

        health_background = (
            "rgba(229,192,91,0.10)"
        )

    else:

        health_color = "#e52b50"

        health_background = (
            "rgba(229,43,80,0.10)"
        )


    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    show_html(
        f"""
        <div style="
            background:
                linear-gradient(
                    135deg,
                    rgba(229,43,80,0.12),
                    rgba(255,255,255,0.025)
                );

            border:
                1px solid
                rgba(255,255,255,0.08);

            border-radius:20px;

            padding:35px;
        ">

            <div style="
                color:#777;
                font-size:9px;
                letter-spacing:1.4px;
            ">

                OVERALL HEALTH SCORE

            </div>


            <div style="
                color:#f4f4f4;
                font-size:62px;
                font-weight:800;
                letter-spacing:-4px;
                margin-top:7px;
            ">

                {business["business_health_score"]:.1f}

                <span style="
                    color:#666;
                    font-size:18px;
                    letter-spacing:0;
                ">

                    /100

                </span>

            </div>


            <div style="
                display:inline-block;

                padding:7px 13px;

                border-radius:20px;

                font-size:9px;

                font-weight:700;

                margin-top:10px;

                color:{health_color};

                background:{health_background};
            ">

                {business["health_status"]}

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # SCORE BREAKDOWN
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                SCORE BREAKDOWN

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                How the Health Score Is Calculated

            </div>


            <div style="
                color:#777;
                font-size:12px;
                margin-top:8px;
            ">

                The score combines rating,
                review activity and operating status.

            </div>

        </div>
        """
    )


    factors = [

        (
            "Rating",
            business["rating_score"] * 0.50,
            50,
            "Customer rating · 50% weight"
        ),

        (
            "Review Activity",
            business["review_score_normalized"] * 0.30,
            30,
            "Review volume · 30% weight"
        ),

        (
            "Operating Status",
            business["open_score"] * 0.20,
            20,
            "Current operating status · 20% weight"
        )

    ]


    columns = st.columns(3)


    for column, (
        name,
        score,
        maximum,
        description
    ) in zip(columns, factors):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:15px;

                    padding:23px;

                    min-height:125px;
                ">

                    <div style="
                        color:#666;
                        font-size:8px;
                        font-weight:700;
                        letter-spacing:1.4px;
                    ">

                        {name.upper()}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:27px;
                        font-weight:750;
                        margin-top:12px;
                    ">

                        {score:.1f}

                        <span style="
                            color:#666;
                            font-size:11px;
                        ">

                            / {maximum}

                        </span>

                    </div>


                    <div style="
                        color:#666;
                        font-size:10px;
                        line-height:1.5;
                        margin-top:6px;
                    ">

                        {description}

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # PERFORMANCE
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                PERFORMANCE

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                Key Business Metrics

            </div>

        </div>
        """
    )


    metrics = [

        (
            "RATING",
            f"{business['stars']:.1f} / 5",
            "Average Yelp rating."
        ),

        (
            "REVIEW ACTIVITY",
            f"{business['review_count']:,}",
            f"{business['total_reviews']:,} reviews analyzed."
        ),

        (
            "POSITIVE %",
            f"{business['positive_percentage']:.1f}%",
            "Reviews classified as positive."
        ),

        (
            "NEGATIVE %",
            f"{business['negative_percentage']:.1f}%",
            "Reviews classified as negative."
        )

    ]


    columns = st.columns(4)


    for column, (
        label,
        value,
        description
    ) in zip(columns, metrics):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:15px;

                    padding:23px;

                    min-height:125px;
                ">

                    <div style="
                        color:#666;
                        font-size:8px;
                        font-weight:700;
                        letter-spacing:1.4px;
                    ">

                        {label}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:27px;
                        font-weight:750;
                        margin-top:12px;
                    ">

                        {value}

                    </div>


                    <div style="
                        color:#666;
                        font-size:10px;
                        line-height:1.5;
                        margin-top:6px;
                    ">

                        {description}

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # RISK
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                EARLY WARNING

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                Business Risk Analysis

            </div>

        </div>
        """
    )


    if business["risk_status"] == "Low Risk":

        risk_color = "#59d99e"

        risk_background = (
            "rgba(89,217,158,0.10)"
        )

    elif business["risk_status"] == "Medium Risk":

        risk_color = "#e5c05b"

        risk_background = (
            "rgba(229,192,91,0.10)"
        )

    else:

        risk_color = "#e52b50"

        risk_background = (
            "rgba(229,43,80,0.10)"
        )


    show_html(
        f"""
        <div style="
            background:#111419;

            border:
                1px solid
                rgba(255,255,255,0.08);

            border-radius:16px;

            padding:25px;
        ">

            <div style="
                color:#666;
                font-size:8px;
                font-weight:700;
                letter-spacing:1.4px;
            ">

                RISK SCORE

            </div>


            <div style="
                color:#f4f4f4;
                font-size:30px;
                font-weight:750;
                margin-top:10px;
            ">

                {business["risk_score"]:.1f}

                <span style="
                    color:#666;
                    font-size:12px;
                ">

                    /100

                </span>

            </div>


            <div style="
                display:inline-block;

                padding:7px 13px;

                border-radius:20px;

                font-size:9px;

                font-weight:700;

                margin-top:10px;

                color:{risk_color};

                background:{risk_background};
            ">

                {business["risk_status"]}

            </div>


            <div style="
                color:#666;
                font-size:10px;
                line-height:1.6;
                margin-top:12px;
            ">

                The available business indicators are used
                to estimate potential business decline risk.

            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # REVIEW SENTIMENT
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                CUSTOMER FEEDBACK

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                Review Sentiment

            </div>

        </div>
        """
    )


    total_reviews = business["total_reviews"]


    if total_reviews > 0:

        neutral_percentage = (
            business["neutral_reviews"]
            / total_reviews
        ) * 100

    else:

        neutral_percentage = 0


    sentiments = [

        (
            "POSITIVE",
            business["positive_reviews"],
            business["positive_percentage"]
        ),

        (
            "NEUTRAL",
            business["neutral_reviews"],
            neutral_percentage
        ),

        (
            "NEGATIVE",
            business["negative_reviews"],
            business["negative_percentage"]
        )

    ]


    columns = st.columns(3)


    for column, (
        label,
        count,
        percentage
    ) in zip(columns, sentiments):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:15px;

                    padding:23px;

                    min-height:125px;
                ">

                    <div style="
                        color:#666;
                        font-size:8px;
                        font-weight:700;
                        letter-spacing:1.4px;
                    ">

                        {label}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:27px;
                        font-weight:750;
                        margin-top:12px;
                    ">

                        {count:,}

                    </div>


                    <div style="
                        color:#666;
                        font-size:10px;
                        margin-top:6px;
                    ">

                        {percentage:.1f}%
                        of analyzed reviews.

                    </div>

                </div>
                """
            )


    # ========================================================
    # RESTAURANT ASPECT ANALYSIS
    # ========================================================

    if business["business_category"] in ["Restaurant", "Grocery", "Healthcare", "Auto Repair"]:

        aspects = get_aspects(
            business["business_id"]
        )


        if aspects:

            show_html(
                f"""
                <div style="
                    margin-top:60px;
                    margin-bottom:25px;
                ">

                    <div style="
                        color:#e52b50;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:2px;
                    ">

                        CUSTOMER EXPERIENCE

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:29px;
                        font-weight:750;
                        margin-top:8px;
                    ">

                        {html.escape(business["business_category"])} Experience Analysis

                    </div>


                    <div style="
                        color:#777;
                        font-size:12px;
                        line-height:1.7;
                        margin-top:8px;
                    ">

                        Customer feedback has been grouped into
                        important {html.escape(business["business_category"].lower())}
                        experience areas using Spark-based aspect analysis.

                    </div>

                </div>
                """
            )


            # ------------------------------------------------
            # ASPECT CARDS
            # ------------------------------------------------

            for start in range(
                0,
                len(aspects),
                2
            ):

                row = aspects[
                    start:start + 2
                ]


                columns = st.columns(2)


                for column, aspect in zip(
                    columns,
                    row
                ):

                    with column:

                        aspect_name = html.escape(
                            aspect["aspect"]
                        )


                        show_html(
                            f"""
                            <div style="
                                background:#111419;

                                border:
                                    1px solid
                                    rgba(255,255,255,0.08);

                                border-radius:16px;

                                padding:23px;

                                margin-bottom:18px;
                            ">

                                <div style="
                                    display:flex;
                                    justify-content:space-between;
                                ">

                                    <div>

                                        <div style="
                                            color:#f4f4f4;
                                            font-size:17px;
                                            font-weight:700;
                                        ">

                                            {aspect_name}

                                        </div>


                                        <div style="
                                            color:#666;
                                            font-size:10px;
                                            margin-top:5px;
                                        ">

                                            {aspect["aspect_mentions"]:,}
                                            mentions analyzed

                                        </div>

                                    </div>


                                    <div style="
                                        color:#f4f4f4;
                                        font-size:22px;
                                        font-weight:750;
                                    ">

                                        {aspect["positive_percentage"]:.1f}%

                                    </div>

                                </div>


                                <!-- POSITIVE -->

                                <div style="
                                    color:#777;
                                    font-size:9px;
                                    margin-top:15px;
                                    margin-bottom:4px;
                                ">

                                    Positive

                                </div>


                                <div style="
                                    width:100%;
                                    height:6px;
                                    background:#25282e;
                                    border-radius:10px;
                                    overflow:hidden;
                                ">

                                    <div style="
                                        width:
                                        {aspect["positive_percentage"]}%;

                                        height:100%;

                                        background:#59d99e;
                                    ">
                                    </div>

                                </div>


                                <!-- NEUTRAL -->

                                <div style="
                                    color:#777;
                                    font-size:9px;
                                    margin-top:13px;
                                    margin-bottom:4px;
                                ">

                                    Neutral

                                </div>


                                <div style="
                                    width:100%;
                                    height:6px;
                                    background:#25282e;
                                    border-radius:10px;
                                    overflow:hidden;
                                ">

                                    <div style="
                                        width:
                                        {aspect["neutral_percentage"]}%;

                                        height:100%;

                                        background:#777;
                                    ">
                                    </div>

                                </div>


                                <!-- NEGATIVE -->

                                <div style="
                                    color:#777;
                                    font-size:9px;
                                    margin-top:13px;
                                    margin-bottom:4px;
                                ">

                                    Negative

                                </div>


                                <div style="
                                    width:100%;
                                    height:6px;
                                    background:#25282e;
                                    border-radius:10px;
                                    overflow:hidden;
                                ">

                                    <div style="
                                        width:
                                        {aspect["negative_percentage"]}%;

                                        height:100%;

                                        background:#e52b50;
                                    ">
                                    </div>

                                </div>


                                <div style="
                                    color:#666;
                                    font-size:10px;
                                    margin-top:10px;
                                ">

                                    Positive
                                    {aspect["positive_percentage"]:.1f}%

                                    ·

                                    Neutral
                                    {aspect["neutral_percentage"]:.1f}%

                                    ·

                                    Negative
                                    {aspect["negative_percentage"]:.1f}%

                                </div>

                            </div>
                            """
                        )


            # ------------------------------------------------
            # RESTAURANT INSIGHTS
            # ------------------------------------------------

            strongest = max(
                aspects,
                key=lambda x:
                    x["positive_percentage"]
            )


            concern = max(
                aspects,
                key=lambda x:
                    x["negative_percentage"]
            )


            discussed = max(
                aspects,
                key=lambda x:
                    x["aspect_mentions"]
            )


            show_html(
                """
                <div style="
                    margin-top:60px;
                    margin-bottom:25px;
                ">

                    <div style="
                        color:#e52b50;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:2px;
                    ">

                        BUSINESS INTELLIGENCE

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:29px;
                        font-weight:750;
                        margin-top:8px;
                    ">

                        Restaurant Insights

                    </div>


                    <div style="
                        color:#777;
                        font-size:12px;
                        margin-top:8px;
                    ">

                        Automatically generated observations
                        from customer experience data.

                    </div>

                </div>
                """
            )


            insights = [

                (
                    "STRENGTH",
                    "Strongest Customer Area",
                    strongest["aspect"],
                    (
                        f"{strongest['aspect']} has the highest "
                        f"positive customer perception at "
                        f"{strongest['positive_percentage']:.1f}%."
                    )
                ),

                (
                    "CUSTOMER CONCERN",
                    "Area Requiring Attention",
                    concern["aspect"],
                    (
                        f"{concern['aspect']} has the highest "
                        f"negative feedback at "
                        f"{concern['negative_percentage']:.1f}%."
                    )
                ),

                (
                    "FEEDBACK ACTIVITY",
                    "Most Discussed Area",
                    discussed["aspect"],
                    (
                        f"{discussed['aspect']} appears most frequently "
                        f"in customer feedback, with "
                        f"{discussed['aspect_mentions']:,} "
                        f"analyzed mentions."
                    )
                )

            ]


            columns = st.columns(3)


            for column, insight in zip(
                columns,
                insights
            ):

                with column:

                    show_html(
                        f"""
                        <div style="
                            background:#111419;

                            border:
                                1px solid
                                rgba(255,255,255,0.08);

                            border-radius:16px;

                            padding:24px;

                            min-height:150px;
                        ">

                            <div style="
                                color:#e52b50;
                                font-size:9px;
                                font-weight:700;
                                letter-spacing:1.4px;
                            ">

                                {insight[0]}

                            </div>


                            <div style="
                                color:#f4f4f4;
                                font-size:16px;
                                font-weight:700;
                                margin-top:9px;
                            ">

                                {insight[1]}

                            </div>


                            <div style="
                                color:#e52b50;
                                font-size:12px;
                                font-weight:600;
                                margin-top:5px;
                            ">

                                {html.escape(
                                    insight[2]
                                )}

                            </div>


                            <div style="
                                color:#777;
                                font-size:11px;
                                line-height:1.7;
                                margin-top:9px;
                            ">

                                {html.escape(
                                    insight[3]
                                )}

                            </div>

                        </div>
                        """
                    )


            # ------------------------------------------------
            # RECOMMENDATION
            # ------------------------------------------------

            average_positive = sum(
                x["positive_percentage"]
                for x in aspects
            ) / len(aspects)


            average_negative = sum(
                x["negative_percentage"]
                for x in aspects
            ) / len(aspects)


            if (
                average_positive >= 80
                and average_negative < 10
            ):

                recommendation = (
                    "Customer perception is broadly positive "
                    "across the analyzed restaurant experience "
                    "areas. Maintaining current service and "
                    "quality levels should remain a priority."
                )

            elif average_negative >= 20:

                recommendation = (
                    "Several customer experience areas show "
                    "elevated negative feedback. The "
                    "highest-concern area should be investigated "
                    "and monitored closely."
                )

            else:

                recommendation = (
                    "Customer perception is generally positive, "
                    "but some experience areas should be "
                    "monitored to identify opportunities "
                    "for improvement."
                )


            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:16px;

                    padding:24px;

                    margin-top:18px;
                ">

                    <div style="
                        color:#e52b50;
                        font-size:9px;
                        font-weight:700;
                        letter-spacing:1.4px;
                    ">

                        RECOMMENDATION

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:16px;
                        font-weight:700;
                        margin-top:9px;
                    ">

                        Business Recommendation

                    </div>


                    <div style="
                        color:#777;
                        font-size:11px;
                        line-height:1.7;
                        margin-top:9px;
                    ">

                        {html.escape(
                            recommendation
                        )}

                    </div>

                </div>
                """
            )


            st.caption(
                "Aspect sentiment is based on Yelp star ratings "
                "associated with reviews containing relevant "
                "aspect terms. It is an analytical indicator "
                "rather than direct text-level sentiment."
            )


    # --------------------------------------------------------
    # BUSINESS PROFILE
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:25px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                BUSINESS PROFILE

            </div>


            <div style="
                color:#f4f4f4;
                font-size:29px;
                font-weight:750;
                margin-top:8px;
            ">

                Operating Information

            </div>

        </div>
        """
    )


    operating_status = (

        "Currently Operating"

        if business["is_open"] == 1

        else "Not Currently Operating"

    )


    profile = [

        (
            "OPERATING STATUS",
            operating_status
        ),

        (
            "BUSINESS TYPE",
            business["business_category"]
        ),

        (
            "LOCATION",
            f"{business['city']}, {business['state']}"
        ),

        (
            "ADDRESS",
            business["address"] or "Not available"
        )

    ]


    columns = st.columns(4)


    for column, (label, value) in zip(
        columns,
        profile
    ):

        with column:

            show_html(
                f"""
                <div style="
                    background:#111419;

                    border:
                        1px solid
                        rgba(255,255,255,0.08);

                    border-radius:15px;

                    padding:23px;

                    min-height:110px;
                ">

                    <div style="
                        color:#666;
                        font-size:8px;
                        font-weight:700;
                        letter-spacing:1.4px;
                    ">

                        {label}

                    </div>


                    <div style="
                        color:#f4f4f4;
                        font-size:15px;
                        font-weight:650;
                        line-height:1.5;
                        margin-top:12px;
                    ">

                        {html.escape(
                            str(value)
                        )}

                    </div>

                </div>
                """
            )


    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    show_html(
        """
        <div style="
            margin-top:60px;
            margin-bottom:15px;
        ">

            <div style="
                color:#e52b50;
                font-size:9px;
                font-weight:700;
                letter-spacing:2px;
            ">

                ANALYSIS PIPELINE

            </div>

        </div>


        <div style="
            background:#111419;

            border:
                1px solid
                rgba(255,255,255,0.08);

            border-radius:16px;

            padding:24px;

            color:#777;

            font-size:11px;

            line-height:2;
        ">

            Yelp Open Dataset
            →
            Hadoop / HDFS
            →
            Apache Spark
            →
            Data Processing
            →
            Business Analytics
            →

            <span style="
                color:#e52b50;
                font-weight:700;
            ">

                Business Insights

            </span>

        </div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

show_html(
    """
    <div style="
        text-align:center;

        color:#555;

        font-size:9px;

        letter-spacing:1px;

        border-top:
            1px solid
            rgba(255,255,255,0.07);

        padding-top:25px;

        margin-top:80px;
    ">

        BUSINESS INSIGHTS
        · POWERED BY YELP BIG DATA
        · APACHE SPARK
        · NLP
        · MACHINE LEARNING

    </div>
    """
)
