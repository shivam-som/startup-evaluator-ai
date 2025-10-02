from backend.utils.llm_client import call_llm

def run(state: dict) -> dict:
    if state.get("terminate"):
        state["recommendation"] = "🚫 Startup idea appears non-viable based on earlier evaluation."
        return state

    market = state.get("market", "")
    technical = state.get("technical", "")
    business = state.get("business", "")

    prompt = f"""
        You are a Startup Advisor. Based on the evaluation summaries below, provide one concise recommendation. 
        Start with: As a Startup Advisor. 
        Recommendation should be one of: Strongly Recommended, Recommended with Improvements, or Not Recommended. 
        Then add 2-3 sentences of reasoning in the same paragraph. 
        Do not use lists or headings — only a single flowing paragraph.

        Market Analysis:
        {market}

        Technical Feasibility:
        {technical}

        Business Strategy:
        {business}
    """

    recommendation = call_llm(prompt)
    state["recommendation"] = recommendation
    return state
