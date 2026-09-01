import html
import streamlit as st

from src.pipelines.pipeline import run_research_pipeline
from src.utils.pdf_generator import create_research_pdf


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 50% -20%,
            rgba(92, 65, 255, 0.18),
            transparent 45%
        ),
        #080d19;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}


/* ============================================================
   HERO
   ============================================================ */

.hero {
    text-align: center;
    padding: 2.5rem 2rem 2.2rem 2rem;
    border-radius: 24px;
    border: 1px solid rgba(255,255,255,0.10);

    background:
        linear-gradient(
            135deg,
            rgba(19,29,58,0.98),
            rgba(12,18,38,0.98)
        );

    box-shadow:
        0 20px 60px rgba(0,0,0,0.28);

    margin-bottom: 1.8rem;
}


/* ============================================================
   BIG COLORFUL TITLE
   ============================================================ */

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1.15;
    letter-spacing: -1.5px;
    margin-bottom: 0.7rem;
    color: #ffffff;
}

.hero-title span {
    background:
        linear-gradient(
            90deg,
            #a855f7 0%,
            #6366f1 30%,
            #06b6d4 65%,
            #22c55e 100%
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}


/* ============================================================
   SUBTITLE
   ============================================================ */

.hero-subtitle {
    color: #aeb8d0;
    font-size: 1.08rem;
    letter-spacing: 0.2px;
}


/* ============================================================
   PROMPT
   ============================================================ */

.prompt-heading {
    font-size: 1.08rem;
    font-weight: 750;
    color: #e7ebf7;
    margin-top: 0.8rem;
    margin-bottom: 0.35rem;
}

.prompt-description {
    font-size: 0.86rem;
    color: #8f9bb7;
    margin-bottom: 0.65rem;
}


/* ============================================================
   TEXT AREA
   ============================================================ */

div[data-testid="stTextArea"] {
    margin-bottom: 0.6rem;
}

div[data-testid="stTextArea"] textarea {
    background: #0d1426 !important;

    border: 1px solid rgba(255,255,255,0.12) !important;

    border-radius: 14px !important;

    color: #f4f7ff !important;

    font-size: 1rem !important;

    line-height: 1.5 !important;

    padding: 1rem !important;
}

div[data-testid="stTextArea"] textarea:focus {
    border-color: #6366f1 !important;

    box-shadow:
        0 0 0 1px rgba(99,102,241,0.45) !important;
}


/* ============================================================
   BUTTON
   ============================================================ */

div.stButton > button {
    min-height: 48px;

    border-radius: 12px;

    font-size: 1rem;

    font-weight: 750;

    border: none;
}


/* ============================================================
   PIPELINE TITLE
   ============================================================ */

.section-title {
    font-size: 2.15rem;

    font-weight: 850;

    color: #f5f7ff;

    margin-top: 2rem;

    margin-bottom: 1rem;
}


/* ============================================================
   AGENT CARD
   ============================================================ */

.agent-card {
    border: 1px solid rgba(255,255,255,0.10);

    border-radius: 16px;

    padding: 1.15rem 1.25rem;

    margin: 0.8rem 0;

    background: #11182c;

    transition:
        border-color 0.3s ease,
        box-shadow 0.3s ease;
}

.agent-running {
    border-color: rgba(255,193,7,0.65);

    box-shadow:
        0 0 25px rgba(255,193,7,0.10);
}

.agent-done {
    border-color: rgba(46,204,113,0.45);

    box-shadow:
        0 0 20px rgba(46,204,113,0.05);
}

.agent-failed {
    border-color: rgba(255,82,82,0.55);

    box-shadow:
        0 0 20px rgba(255,82,82,0.06);
}


/* ============================================================
   AGENT HEADER
   ============================================================ */

.agent-header {
    display: flex;

    align-items: center;

    gap: 0.8rem;
}


/* ============================================================
   AGENT ICON
   ============================================================ */

.agent-icon {
    width: 44px;

    height: 44px;

    min-width: 44px;

    display: flex;

    align-items: center;

    justify-content: center;

    border-radius: 12px;

    background: #1a2440;

    font-size: 1.3rem;
}


/* ============================================================
   AGENT TITLE
   ============================================================ */

.agent-title {
    font-size: 1.08rem;

    font-weight: 750;

    color: #f5f7ff;
}


/* ============================================================
   AGENT DESCRIPTION
   ============================================================ */

.agent-description {
    color: #9da8c2;

    font-size: 0.88rem;

    margin-top: 0.15rem;
}


/* ============================================================
   STATUS
   ============================================================ */

.status-running {
    margin-left: auto;

    color: #ffd166;

    font-weight: 750;

    font-size: 0.84rem;

    white-space: nowrap;
}

.status-done {
    margin-left: auto;

    color: #51e28a;

    font-weight: 750;

    font-size: 0.84rem;

    white-space: nowrap;
}

.status-failed {
    margin-left: auto;

    color: #ff7373;

    font-weight: 750;

    font-size: 0.84rem;

    white-space: nowrap;
}

.status-waiting {
    margin-left: auto;

    color: #7f8aa5;

    font-weight: 650;

    font-size: 0.84rem;

    white-space: nowrap;
}


/* ============================================================
   PROMPT DISPLAY
   ============================================================ */

.query-box {
    padding: 1rem 1.1rem;

    border-radius: 13px;

    background: #0e1528;

    border: 1px solid rgba(255,255,255,0.08);

    color: #dce3f4;

    white-space: pre-wrap;

    line-height: 1.5;
}


/* ============================================================
   PDF SECTION
   ============================================================ */

.download-box {
    margin-top: 1.5rem;

    padding: 1.4rem;

    border-radius: 18px;

    border: 1px solid rgba(46,204,113,0.30);

    background:
        linear-gradient(
            135deg,
            #0e1b18,
            #0d1716
        );
}

.download-title {
    color: #f5f7ff;

    font-size: 1.4rem;

    font-weight: 750;

    margin-bottom: 0.35rem;
}

.download-description {
    color: #9da8c2;

    font-size: 0.9rem;

    line-height: 1.5;
}


/* ============================================================
   SIDEBAR
   ============================================================ */

section[data-testid="stSidebar"] {
    background: #070c17;
}

.sidebar-title {
    text-align: center;

    font-size: 1.65rem;

    font-weight: 850;

    color: #ffffff;

    margin-top: 0.8rem;
}

.sidebar-subtitle {
    text-align: center;

    color: #8f9bb7;

    font-size: 0.78rem;

    margin-top: 0.25rem;
}

.sidebar-agent {
    padding: 0.55rem 0;

    color: #dce3f4;

    font-size: 0.95rem;
}

.sidebar-info {
    color: #7f8aa5;

    font-size: 0.78rem;

    line-height: 1.6;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 768px) {

    .hero-title {
        font-size: 2.3rem;
    }

    .hero-subtitle {
        font-size: 0.95rem;
    }

    .section-title {
        font-size: 1.7rem;
    }

    .status-running,
    .status-done,
    .status-failed,
    .status-waiting {
        font-size: 0.72rem;
    }

}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "running" not in st.session_state:
    st.session_state.running = False

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""


# ============================================================
# AGENT DEFINITIONS
# ============================================================

STEPS = {
    "search": {
        "icon": "🔎",
        "title": "Search Agent",
        "description": "Finding recent, reliable and detailed information.",
    },

    "reader": {
        "icon": "📖",
        "title": "Reader Agent",
        "description": "Selecting and scraping the most relevant resource.",
    },

    "writer": {
        "icon": "✍️",
        "title": "Writer",
        "description": "Combining the research and drafting the report.",
    },

    "critic": {
        "icon": "🧐",
        "title": "Critic",
        "description": "Reviewing the generated report.",
    },
}


# ============================================================
# CONVERT AGENT OUTPUT TO TEXT
# ============================================================

def text_content(value):

    if value is None:
        return ""

    if isinstance(value, str):
        return value

    content = getattr(value, "content", None)

    if content is not None:
        return str(content)

    return str(value)


# ============================================================
# RENDER AGENT CARD
# ============================================================

def render_step(
    container,
    key,
    status="waiting",
    output=None,
):

    info = STEPS[key]

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if status == "running":

        css = "agent-card agent-running"

        status_html = (
            '<div class="status-running">'
            '● THIS AGENT IS RUNNING'
            '</div>'
        )

    elif status == "done":

        css = "agent-card agent-done"

        status_html = (
            '<div class="status-done">'
            '✓ COMPLETED'
            '</div>'
        )

    elif status == "failed":

        css = "agent-card agent-failed"

        status_html = (
            '<div class="status-failed">'
            '✕ FAILED'
            '</div>'
        )

    else:

        css = "agent-card"

        status_html = (
            '<div class="status-waiting">'
            'WAITING'
            '</div>'
        )

    # --------------------------------------------------------
    # IMPORTANT:
    # Everything is intentionally kept on one line / without
    # Markdown indentation so Streamlit doesn't create code
    # blocks from nested HTML.
    # --------------------------------------------------------

    card_html = (
        f'<div class="{css}">'
        f'<div class="agent-header">'
        f'<div class="agent-icon">{info["icon"]}</div>'
        f'<div>'
        f'<div class="agent-title">{info["title"]}</div>'
        f'<div class="agent-description">{info["description"]}</div>'
        f'</div>'
        f'{status_html}'
        f'</div>'
        f'</div>'
    )

    container.markdown(
        card_html,
        unsafe_allow_html=True,
    )

    # --------------------------------------------------------
    # OUTPUT
    # --------------------------------------------------------

    if output is not None:

        output_text = text_content(output)

        with container.expander(
            f"📄 View {info['title']} Output",
            expanded=True,
        ):

            st.markdown(output_text)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    sidebar_header = (
        '<div class="sidebar-title">'
        '🔬 Research'
        '</div>'
        '<div class="sidebar-subtitle">'
        'Multi-Agent Pipeline'
        '</div>'
    )

    st.markdown(
        sidebar_header,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown("### Pipeline")

    sidebar_pipeline = (
        '<div class="sidebar-agent">'
        '<b>1.</b> 🔎 Search Agent'
        '</div>'

        '<div class="sidebar-agent">'
        '<b>2.</b> 📖 Reader Agent'
        '</div>'

        '<div class="sidebar-agent">'
        '<b>3.</b> ✍️ Writer'
        '</div>'

        '<div class="sidebar-agent">'
        '<b>4.</b> 🧐 Critic'
        '</div>'
    )

    st.markdown(
        sidebar_pipeline,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    sidebar_info = (
        '<div class="sidebar-info">'
        'Each agent executes sequentially.'
        '<br><br>'
        'The interface displays the live '
        'status and output of every stage.'
        '<br><br>'
        'The final research package can '
        'be downloaded as a PDF.'
        '</div>'
    )

    st.markdown(
        sidebar_info,
        unsafe_allow_html=True,
    )


# ============================================================
# HERO
# ============================================================

hero_html = (
    '<div class="hero">'
    '<div class="hero-title">'
    '🔬 <span>Multi-Agent Research System</span>'
    '</div>'
    '<div class="hero-subtitle">'
    'Intelligent research powered by multiple specialized agents'
    '</div>'
    '</div>'
)

st.markdown(
    hero_html,
    unsafe_allow_html=True,
)


# ============================================================
# RESEARCH PROMPT
# ============================================================

prompt_header = (
    '<div class="prompt-heading">'
    '🔎 Enter your research question or prompt'
    '</div>'
    '<div class="prompt-description">'
    'Give the system any research topic, question, or task. '
    'The agents will process it sequentially.'
    '</div>'
)

st.markdown(
    prompt_header,
    unsafe_allow_html=True,
)


topic = st.text_area(
    "Research Prompt",
    placeholder=(
        "Example:\n"
        "What are the recent advances in multimodal AI "
        "for medical imaging?"
    ),
    height=120,
    label_visibility="collapsed",
    key="research_prompt",
)


# ============================================================
# START BUTTON
# ============================================================

run_button = st.button(
    "🚀  Start Research",
    type="primary",
    use_container_width=True,
    disabled=st.session_state.running,
)


# ============================================================
# PIPELINE TITLE
# ============================================================

section_html = (
    '<div class="section-title">'
    'Research Pipeline'
    '</div>'
)

st.markdown(
    section_html,
    unsafe_allow_html=True,
)


# ============================================================
# PIPELINE PLACEHOLDERS
# ============================================================

step_containers = {}

for key in STEPS:

    step_containers[key] = st.empty()

    render_step(
        step_containers[key],
        key,
        status="waiting",
    )


# ============================================================
# RUN RESEARCH PIPELINE
# ============================================================

if run_button:

    # --------------------------------------------------------
    # CHECK PROMPT
    # --------------------------------------------------------

    if not topic.strip():

        st.warning(
            "⚠️ Please enter a research prompt first."
        )

        st.stop()


    # --------------------------------------------------------
    # SESSION STATE
    # --------------------------------------------------------

    st.session_state.running = True

    st.session_state.result = None

    st.session_state.last_topic = topic.strip()


    # --------------------------------------------------------
    # SHOW CURRENT PROMPT
    # --------------------------------------------------------

    st.markdown(
        "### Current Research Prompt"
    )

    safe_topic = html.escape(
        topic.strip()
    )

    query_html = (
        '<div class="query-box">'
        f'{safe_topic}'
        '</div>'
    )

    st.markdown(
        query_html,
        unsafe_allow_html=True,
    )


    # ========================================================
    # CALLBACK: START
    # ========================================================

    def on_step_start(step_key):

        render_step(
            step_containers[step_key],
            step_key,
            status="running",
        )


    # ========================================================
    # CALLBACK: COMPLETE
    # ========================================================

    def on_step_complete(
        step_key,
        output,
    ):

        render_step(
            step_containers[step_key],
            step_key,
            status="done",
            output=output,
        )


    # ========================================================
    # CALLBACK: ERROR
    # ========================================================

    def on_step_error(
        step_key,
        error,
    ):

        render_step(
            step_containers[step_key],
            step_key,
            status="failed",
            output=f"Error: {error}",
        )


    # ========================================================
    # EXECUTE PIPELINE
    # ========================================================

    try:

        result = run_research_pipeline(
            topic.strip(),
            on_step_start=on_step_start,
            on_step_complete=on_step_complete,
            on_step_error=on_step_error,
        )

        st.session_state.result = result

        st.success(
            "✅ Research pipeline completed successfully."
        )

    except Exception as exc:

        st.error(
            f"❌ Research pipeline failed: {exc}"
        )

    finally:

        st.session_state.running = False


# ============================================================
# PDF DOWNLOAD
# ============================================================

if st.session_state.result:

    download_html = (
        '<div class="download-box">'
        '<div class="download-title">'
        '📄 Final Research Package'
        '</div>'
        '<div class="download-description">'
        'The PDF contains the complete research workflow: '
        'original prompt, Search Agent output, '
        'Reader Agent output, Writer report, '
        'and Critic feedback.'
        '</div>'
        '</div>'
    )

    st.markdown(
        download_html,
        unsafe_allow_html=True,
    )

    try:

        pdf_bytes = create_research_pdf(
            topic=st.session_state.last_topic,
            result=st.session_state.result,
        )

        st.download_button(
            label="⬇️  Download Complete Research as PDF",
            data=pdf_bytes,
            file_name="multi_agent_research_report.pdf",
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

    except Exception as exc:

        st.error(
            f"❌ Could not create PDF: {exc}"
        )