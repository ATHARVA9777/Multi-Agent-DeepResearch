"""
Streamlit UI for the Multi-Agent Research Pipeline.

Run with:
    streamlit run app.py

Expects `pipeline.py` (with `run_research_pipeline`) and `agents.py`
to be in the same folder as this file.
"""

import streamlit as st
from pipeline import run_research_pipeline

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🔎",
    layout="wide",
)

# ---------- Session State ----------
if "state" not in st.session_state:
    st.session_state.state = None
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ---------- Sidebar ----------
with st.sidebar:
    st.header("⚙️ About")
    st.markdown(
        """
        This app runs a 4-step multi-agent research pipeline:

        1. **Search Agent** – finds recent, relevant sources
        2. **Reader Agent** – scrapes the best URL for detail
        3. **Writer Chain** – drafts a full report
        4. **Critic Chain** – reviews and gives feedback

        Enter a topic and click **Run Research** to start.
        """
    )
    if st.session_state.state:
        st.divider()
        if st.button("🗑️ Clear results", use_container_width=True):
            st.session_state.state = None
            st.session_state.topic = ""
            st.rerun()

# ---------- Header ----------
st.title("🔎 Multi-Agent Research System")
st.caption("Search → Read → Write → Critique, all in one pipeline.")

# ---------- Input Form ----------
with st.form("research_form"):
    topic = st.text_input(
        "Research topic",
        placeholder="e.g. Latest advancements in solid-state batteries",
        value=st.session_state.topic,
    )
    submitted = st.form_submit_button("🚀 Run Research", use_container_width=True)

# ---------- Run Pipeline ----------
if submitted:
    if not topic.strip():
        st.warning("Please enter a topic before running the pipeline.")
    else:
        st.session_state.topic = topic
        state = {}

        progress = st.progress(0, text="Starting pipeline...")
        status_box = st.empty()

        try:
            # --- Step 1: Search ---
            status_box.info("Step 1/4 — 🔍 Search agent is gathering sources...")
            progress.progress(10, text="Searching...")

            from agents import build_search_agent, build_reader_agent, writer_chain, critic_chain

            search_agent = build_search_agent()
            search_result = search_agent.invoke(
                {"messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]}
            )
            state["search_results"] = str(search_result["messages"][-1].content)
            progress.progress(30, text="Search complete.")

            # --- Step 2: Reader ---
            status_box.info("Step 2/4 — 📖 Reader agent is scraping the best source...")
            reader_agent = build_reader_agent()
            reader_result = reader_agent.invoke(
                {
                    "messages": [
                        (
                            "user",
                            f"Based on the following search results about '{topic}', "
                            f"pick the most relevant URL and scrape it for deeper content.\n\n"
                            f"Search Results:\n{state['search_results'][:800]}",
                        )
                    ]
                }
            )
            state["scraped_content"] = str(reader_result["messages"][-1].content)
            progress.progress(55, text="Reading complete.")

            # --- Step 3: Writer ---
            status_box.info("Step 3/4 — ✍️ Writer is drafting the report...")
            research_combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["report"] = writer_chain.invoke({"topic": topic, "research": research_combined})
            progress.progress(80, text="Draft complete.")

            # --- Step 4: Critic ---
            status_box.info("Step 4/4 — 🧐 Critic is reviewing the report...")
            state["feedback"] = critic_chain.invoke({"report": state["report"]})
            progress.progress(100, text="Done!")

            status_box.success("✅ Pipeline finished successfully!")
            st.session_state.state = state

        except Exception as e:
            status_box.empty()
            progress.empty()
            st.error(f"❌ Pipeline failed: {e}")
            st.exception(e)

# ---------- Display Results ----------
state = st.session_state.state
if state:
    st.divider()
    st.subheader(f"Results for: *{st.session_state.topic}*")

    tab_report, tab_feedback, tab_search, tab_scraped = st.tabs(
        ["📄 Final Report", "🧐 Critic Feedback", "🔍 Search Results", "📖 Scraped Content"]
    )

    with tab_report:
        report_text = state.get("report", "")
        st.markdown(
            report_text if isinstance(report_text, str) else str(report_text)
        )
        st.download_button(
            "⬇️ Download report as .md",
            data=str(report_text),
            file_name=f"{st.session_state.topic.replace(' ', '_')}_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    with tab_feedback:
        feedback_text = state.get("feedback", "")
        st.markdown(feedback_text if isinstance(feedback_text, str) else str(feedback_text))

    with tab_search:
        with st.expander("Raw search results", expanded=True):
            st.text(state.get("search_results", ""))

    with tab_scraped:
        with st.expander("Raw scraped content", expanded=True):
            st.text(state.get("scraped_content", ""))
else:
    st.info("👆 Enter a topic above and click **Run Research** to get started.")    