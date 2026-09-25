import asyncio
import json

import streamlit as st

from workflow import run_pipeline
from audit import crawl_site, audit_site


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="SEO Intelligence Studio",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# THEME / CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       STREAMLIT THEME VARIABLES
       ======================================================== */

    :root {
        --primary-color: #7657ff;
        --background-color: #080c18;
        --secondary-background-color: #0d1425;
        --text-color: #f5f7ff;
        --font: sans-serif;
        color-scheme: dark;
    }


    /* ========================================================
       GLOBAL PAGE
       ======================================================== */

    html,
    body,
    #root,
    .stApp,
    [data-testid="stAppViewContainer"] {
        background: #080c18 !important;
        color: #f5f7ff !important;
    }

    .stApp {
        min-height: 100vh !important;

        background:
            radial-gradient(
                circle at 85% 0%,
                rgba(118, 87, 255, 0.16),
                transparent 32%
            ),
            radial-gradient(
                circle at 100% 45%,
                rgba(78, 140, 255, 0.08),
                transparent 30%
            ),
            #080c18 !important;
    }


    /* ========================================================
       REMOVE / FIX STREAMLIT TOP HEADER
       ======================================================== */

    header[data-testid="stHeader"] {
        background: #080c18 !important;
        height: 0 !important;
    }

    div[data-testid="stDecoration"] {
        background: #080c18 !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }


    /* ========================================================
       MAIN CONTENT
       ======================================================== */

    .main {
        background: transparent !important;
    }

    section.main > div {
        background: transparent !important;
    }

    .block-container {
        max-width: 1180px !important;

        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }


    /* ========================================================
       GLOBAL TEXT
       ======================================================== */

    .stApp p,
    .stApp span,
    .stApp label,
    .stApp li,
    .stApp small {
        color: #f5f7ff !important;
    }

    [data-testid="stMarkdownContainer"] {
        color: #f5f7ff !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #f5f7ff !important;
    }


    /* ========================================================
       HEADINGS
       ======================================================== */

    h1,
    h2,
    h3,
    h4,
    h5,
    h6 {
        color: #f8fafc !important;
        opacity: 1 !important;
    }

    h1 {
        font-size: 2.5rem !important;
        font-weight: 750 !important;
        letter-spacing: -0.03em !important;
    }

    h2 {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    h3 {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {
        background: #0b1020 !important;
    }

    section[data-testid="stSidebar"] > div {
        background: #0b1020 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #f5f7ff !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #f5f7ff !important;
    }

    section[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #94a3b8 !important;
    }

    section[data-testid="stSidebar"] hr {
        border-color: #202a42 !important;
    }


    /* ========================================================
       RADIO BUTTONS
       ======================================================== */

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"]
    div[role="radiogroup"]
    label p {
        color: #e5e7eb !important;
    }


    /* ========================================================
       CAPTIONS
       ======================================================== */

    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #94a3b8 !important;
    }


    /* ========================================================
       TEXT INPUT
       ======================================================== */

    [data-testid="stTextInput"] label {
        color: #f1f5f9 !important;
        font-weight: 600 !important;
    }

    [data-testid="stTextInput"] label p {
        color: #f1f5f9 !important;
    }

    [data-testid="stTextInput"] div[data-baseweb="input"] {
        background: #11182b !important;
        border-radius: 10px !important;
    }

    [data-testid="stTextInput"] input {
        color: #ffffff !important;
        background: #11182b !important;

        border: 1px solid #35415c !important;
        border-radius: 10px !important;

        caret-color: #ffffff !important;

        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #7f8ba5 !important;
        opacity: 1 !important;

        -webkit-text-fill-color: #7f8ba5 !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #7657ff !important;

        box-shadow:
            0 0 0 2px rgba(118, 87, 255, 0.2) !important;
    }


    /* ========================================================
       TEXT AREA
       ======================================================== */

    [data-testid="stTextArea"] label {
        color: #f1f5f9 !important;
    }

    [data-testid="stTextArea"] textarea {
        color: #ffffff !important;
        background: #11182b !important;

        border: 1px solid #35415c !important;
        border-radius: 10px !important;

        -webkit-text-fill-color: #ffffff !important;
    }

    [data-testid="stTextArea"] textarea::placeholder {
        color: #7f8ba5 !important;
        opacity: 1 !important;

        -webkit-text-fill-color: #7f8ba5 !important;
    }


    /* ========================================================
       SLIDER
       ======================================================== */

    [data-testid="stSlider"] label {
        color: #f1f5f9 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button {
        width: 100% !important;

        min-height: 44px !important;

        border-radius: 10px !important;

        border: 1px solid #35415c !important;

        background: #151e34 !important;

        color: #ffffff !important;

        font-weight: 600 !important;
    }

    .stButton > button p {
        color: #ffffff !important;
    }

    .stButton > button:hover {
        background: #1c2742 !important;

        border-color: #7657ff !important;

        color: #ffffff !important;
    }

    .stButton > button[kind="primary"] {
        background:
            linear-gradient(
                90deg,
                #7657ff,
                #4e8cff
            ) !important;

        border: none !important;

        color: #ffffff !important;

        box-shadow:
            0 8px 24px rgba(118, 87, 255, 0.22) !important;
    }

    .stButton > button[kind="primary"] p {
        color: #ffffff !important;
    }


    /* ========================================================
       DOWNLOAD BUTTON
       ======================================================== */

    [data-testid="stDownloadButton"] button {
        color: #ffffff !important;

        background: #151e34 !important;

        border: 1px solid #35415c !important;

        border-radius: 10px !important;
    }

    [data-testid="stDownloadButton"] button p {
        color: #ffffff !important;
    }


    /* ========================================================
       METRICS
       ======================================================== */

    [data-testid="stMetric"] {
        background: #10172a !important;

        border: 1px solid #202b43 !important;

        border-radius: 12px !important;

        padding: 15px !important;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricLabel"] p {
        color: #94a3b8 !important;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc !important;
    }

    [data-testid="stMetricValue"] div {
        color: #f8fafc !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    [data-baseweb="tab-list"] {
        background: transparent !important;
    }

    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
    }

    button[data-baseweb="tab"] p {
        color: #94a3b8 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    [data-testid="stExpander"] {
        background: #10172a !important;

        border: 1px solid #202b43 !important;

        border-radius: 12px !important;
    }

    [data-testid="stExpander"] summary {
        color: #ffffff !important;
    }

    [data-testid="stExpander"] summary p {
        color: #ffffff !important;
    }


    /* ========================================================
       ALERTS
       ======================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    [data-testid="stAlert"] p {
        color: #f5f7ff !important;
    }


    /* ========================================================
       LINKS
       ======================================================== */

    .stApp a {
        color: #8fa8ff !important;
    }

    .stApp a:hover {
        color: #b9c7ff !important;
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {
        border-color: #202a42 !important;
    }


    /* ========================================================
       SPINNER
       ======================================================== */

    [data-testid="stSpinner"] {
        color: #ffffff !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        h1 {
            font-size: 2rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "seo_results" not in st.session_state:
    st.session_state.seo_results = None

if "audit_results" not in st.session_state:
    st.session_state.audit_results = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("✦ SEO Intelligence")

    st.caption(
        "AI-powered SEO research, content generation "
        "and website auditing."
    )

    st.divider()

    mode = st.radio(
        "Choose workflow",
        [
            "SEO Content Generator",
            "Website Auditor",
        ],
    )

    st.divider()

    st.markdown("### SEO Content Generator")

    st.caption(
        "Research trending topics, write content, "
        "optimize SEO and review the final article."
    )

    st.markdown("### Website Auditor")

    st.caption(
        "Analyze an existing website for SEO, "
        "metadata and content issues."
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title("Research. Audit. Optimize.")

st.write(
    "An AI-powered workspace for SEO research, "
    "content generation and website analysis."
)

st.divider()


# ============================================================
# SEO CONTENT GENERATOR
# ============================================================

if mode == "SEO Content Generator":

    st.subheader("Create an SEO Article")

    topic = st.text_input(
        "Topic",
        placeholder="Example: AI agents for small businesses",
        key="topic",
        autocomplete="off",
    )

    st.caption(
        "Enter your topic and click the button below. "
        "Pressing Enter will not start the AI workflow."
    )

    generate = st.button(
        "✦ Generate SEO Article",
        type="primary",
        key="generate_article",
    )

    if generate:

        if not topic.strip():

            st.warning(
                "Please enter a topic first."
            )

        else:

            with st.spinner(
                "Running research, writing, SEO optimization "
                "and review..."
            ):

                try:

                    result = asyncio.run(
                        run_pipeline(
                            topic.strip()
                        )
                    )

                    st.session_state.seo_results = result

                except Exception as e:

                    st.error(
                        "The SEO workflow failed."
                    )

                    st.exception(e)


    # ========================================================
    # SEO RESULTS
    # ========================================================

    result = st.session_state.seo_results

    if result:

        research = result.get(
            "research",
            {},
        )

        writer = result.get(
            "writer",
            {},
        )

        seo = result.get(
            "seo",
            {},
        )

        reviewer = result.get(
            "reviewer",
            {},
        )

        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Research",
                "Draft",
                "SEO Audit",
                "Final",
                "JSON",
            ]
        )


        # ====================================================
        # RESEARCH
        # ====================================================

        with tab1:

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Primary Keyword",
                    research.get(
                        "primary_keyword",
                        "N/A",
                    ),
                )

            with col2:

                st.metric(
                    "Search Intent",
                    research.get(
                        "search_intent",
                        "N/A",
                    ),
                )

            st.subheader(
                "Recommended Angle"
            )

            st.write(
                research.get(
                    "recommended_angle",
                    "No recommendation available.",
                )
            )

            st.subheader(
                "Secondary Keywords"
            )

            keywords = research.get(
                "secondary_keywords",
                [],
            )

            if keywords:

                for keyword in keywords:

                    st.write(
                        f"• {keyword}"
                    )

            else:

                st.caption(
                    "No secondary keywords returned."
                )

            st.subheader(
                "Content Gaps"
            )

            gaps = research.get(
                "content_gaps",
                [],
            )

            if gaps:

                for gap in gaps:

                    st.write(
                        f"• {gap}"
                    )

            else:

                st.caption(
                    "No content gaps returned."
                )

            st.subheader(
                "Sources"
            )

            sources = research.get(
                "sources",
                [],
            )

            if sources:

                for source in sources:

                    if isinstance(
                        source,
                        dict,
                    ):

                        title = source.get(
                            "title",
                            source.get(
                                "url",
                                "Source",
                            ),
                        )

                        url = source.get(
                            "url"
                        )

                        if url:

                            st.markdown(
                                f"- [{title}]({url})"
                            )

                        else:

                            st.write(
                                f"- {title}"
                            )

                    else:

                        st.write(
                            f"- {source}"
                        )

            else:

                st.caption(
                    "No sources returned."
                )


        # ====================================================
        # DRAFT
        # ====================================================

        with tab2:

            st.subheader(
                writer.get(
                    "title",
                    "Generated Article",
                )
            )

            meta_description = writer.get(
                "meta_description",
                "",
            )

            if meta_description:

                st.caption(
                    meta_description
                )

            st.markdown(
                writer.get(
                    "article_markdown",
                    "No article generated.",
                )
            )


        # ====================================================
        # SEO AUDIT
        # ====================================================

        with tab3:

            score = seo.get(
                "seo_score"
            )

            if score is not None:

                st.metric(
                    "SEO Score",
                    f"{score}/100",
                )

            st.subheader(
                "SEO Issues"
            )

            audit_items = seo.get(
                "audit",
                [],
            )

            if not audit_items:

                st.success(
                    "No SEO issues were returned."
                )

            for item in audit_items:

                severity = str(
                    item.get(
                        "severity",
                        "low",
                    )
                ).upper()

                issue = item.get(
                    "issue",
                    "",
                )

                fix = item.get(
                    "fix",
                    "",
                )

                if severity == "HIGH":

                    icon = "🔴"

                elif severity == "MEDIUM":

                    icon = "🟠"

                else:

                    icon = "🟡"

                st.markdown(
                    f"**{icon} {severity} — {issue}**"
                )

                if fix:

                    st.caption(
                        fix
                    )

                st.divider()

            st.subheader(
                "Optimized Article"
            )

            st.markdown(
                seo.get(
                    "optimized_article_markdown",
                    "No optimized article available.",
                )
            )


        # ====================================================
        # FINAL
        # ====================================================

        with tab4:

            final_score = reviewer.get(
                "final_seo_score"
            )

            if final_score is not None:

                st.metric(
                    "Final SEO Score",
                    f"{final_score}/100",
                )

            final_article = reviewer.get(
                "final_article_markdown",
                "",
            )

            if final_article:

                st.markdown(
                    final_article
                )

                st.download_button(
                    "⬇️ Download Final Article",
                    final_article,
                    "seo_article.md",
                    "text/markdown",
                    key="download_article",
                )

            else:

                st.info(
                    "No final article was returned."
                )


        # ====================================================
        # JSON
        # ====================================================

        with tab5:

            st.json(
                result
            )

            st.download_button(
                "⬇️ Download JSON",
                json.dumps(
                    result,
                    indent=2,
                    ensure_ascii=False,
                ),
                "seo_result.json",
                "application/json",
                key="download_seo_json",
            )


# ============================================================
# WEBSITE AUDITOR
# ============================================================

else:

    st.subheader(
        "Audit an Existing Website"
    )

    url = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        key="website_url",
        autocomplete="url",
    )

    max_pages = st.slider(
        "Maximum pages to crawl",
        min_value=1,
        max_value=25,
        value=5,
        key="max_pages",
    )

    audit_button = st.button(
        "🌐 Start Website Audit",
        type="primary",
        key="start_audit",
    )

    if audit_button:

        if not url.strip():

            st.warning(
                "Please enter a website URL first."
            )

        else:

            with st.spinner(
                "Crawling and analyzing the website..."
            ):

                try:

                    crawl = crawl_site(
                        url.strip(),
                        max_pages=max_pages,
                    )

                    audit = audit_site(
                        crawl
                    )

                    st.session_state.audit_results = {
                        "crawl": crawl,
                        "audit": audit,
                    }

                except Exception as e:

                    st.error(
                        "Website audit failed."
                    )

                    st.exception(e)


    # ========================================================
    # AUDIT RESULTS
    # ========================================================

    result = st.session_state.audit_results

    if result:

        crawl = result.get(
            "crawl",
            {},
        )

        audit = result.get(
            "audit",
            {},
        )

        findings = audit.get(
            "findings",
            [],
        )

        pages = crawl.get(
            "pages",
            [],
        )

        high = sum(
            1
            for item in findings
            if item.get("severity") == "high"
        )

        medium = sum(
            1
            for item in findings
            if item.get("severity") == "medium"
        )

        low = sum(
            1
            for item in findings
            if item.get("severity") == "low"
        )

        st.divider()

        c1, c2, c3, c4 = st.columns(4)

        c1.metric(
            "Pages",
            len(pages),
        )

        c2.metric(
            "High",
            high,
        )

        c3.metric(
            "Medium",
            medium,
        )

        c4.metric(
            "Low",
            low,
        )

        st.subheader(
            "Findings"
        )

        if not findings:

            st.success(
                "No issues were detected."
            )

        for item in findings:

            severity = item.get(
                "severity",
                "low",
            )

            if severity == "high":

                icon = "🔴"

            elif severity == "medium":

                icon = "🟠"

            else:

                icon = "🟡"

            st.markdown(
                f"### {icon} {item.get('issue', 'Issue')}"
            )

            st.caption(
                f"Severity: {severity}"
            )

            if item.get("url"):

                st.write(
                    item["url"]
                )

            st.divider()

        st.subheader(
            "Pages Analyzed"
        )

        for page in pages:

            title = page.get(
                "title",
                "Untitled",
            )

            page_url = page.get(
                "url",
                "",
            )

            with st.expander(
                title
            ):

                if page_url:

                    st.write(
                        page_url
                    )

                st.json(
                    page
                )

        st.download_button(
            "⬇️ Download Audit JSON",
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False,
            ),
            "website_audit.json",
            "application/json",
            key="download_audit_json",
        )