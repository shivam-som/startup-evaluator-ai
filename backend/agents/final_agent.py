from backend.utils.llm_client import call_llm

def run(state: dict) -> dict:
    if state.get("terminate"):
        state["report"] = "🚫 Startup idea appears non-viable based on earlier evaluation."
        return state

    market = state.get("market", "")
    technical = state.get("technical", "")
    business = state.get("business", "")
    recommendation = state.get("recommendation", "")

    prompt = f"""
        Create a structured Startup Evaluation Report using the following sections:

        Market Analysis:
        {market}

        Technical Feasibility:
        {technical}

        Business Strategy:
        {business}

        Recommendations:
        {recommendation}

        End with a clear recommendation.
    """
    
    report = call_llm(prompt)
    state["report"] = report
    return state
