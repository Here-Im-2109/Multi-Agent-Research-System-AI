from src.agents.agents import (
    build_search_agent,
    build_reader_agent,
    writer_chain,
    critic_chain,
)


def _notify(callback, *args):
    """Safely call a UI callback if one was supplied."""
    if callback is not None:
        callback(*args)


def run_research_pipeline(
    topic: str,
    on_step_start=None,
    on_step_complete=None,
    on_step_error=None,
) -> dict:
    """
    Run the four-stage research pipeline.

    The optional callbacks allow Streamlit (or another UI) to display
    each agent's live status without putting Streamlit code inside the
    research logic.
    """

    state = {}

    # ================================================================
    # STEP 1 - SEARCH AGENT
    # ================================================================
    _notify(on_step_start, "search")

    try:
        search_agent = build_search_agent()

        search_result = search_agent.invoke(
            {
                "messages": [
                    (
                        "user",
                        f"Find recent, reliable and detailed information about: {topic}",
                    )
                ]
            }
        )

        state["search_results"] = search_result["messages"][-1].content

        _notify(
            on_step_complete,
            "search",
            state["search_results"],
        )

    except Exception as exc:
        _notify(on_step_error, "search", exc)
        raise

    # ================================================================
    # STEP 2 - READER AGENT
    # ================================================================
    _notify(on_step_start, "reader")

    try:
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

        state["scraped_content"] = reader_result["messages"][-1].content

        _notify(
            on_step_complete,
            "reader",
            state["scraped_content"],
        )

    except Exception as exc:
        _notify(on_step_error, "reader", exc)
        raise

    # ================================================================
    # STEP 3 - WRITER
    # ================================================================
    _notify(on_step_start, "writer")

    try:
        research_combined = (
            f"SEARCH RESULTS :\n{state['search_results']}\n\n"
            f"DETAILED SCRAPED CONTENT :\n{state['scraped_content']}"
        )

        state["report"] = writer_chain.invoke(
            {
                "topic": topic,
                "research": research_combined,
            }
        )

        _notify(
            on_step_complete,
            "writer",
            state["report"],
        )

    except Exception as exc:
        _notify(on_step_error, "writer", exc)
        raise

    # ================================================================
    # STEP 4 - CRITIC
    # ================================================================
    _notify(on_step_start, "critic")

    try:
        state["feedback"] = critic_chain.invoke(
            {
                "report": state["report"],
            }
        )

        _notify(
            on_step_complete,
            "critic",
            state["feedback"],
        )

    except Exception as exc:
        _notify(on_step_error, "critic", exc)
        raise

    return state
