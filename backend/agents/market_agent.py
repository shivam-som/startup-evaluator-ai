from backend.utils.llm_client import call_llm

def run(state: dict) -> dict:
    idea = state["idea"]
    prompt = f"""
        You are a Market Analyst. Evaluate the startup idea "{idea}" in one concise paragraph. 
        Start with: As a Market Analyst. 
        Summarize 3-4 key insights about market fit, demand, customer base, and competition. 
        Do not use lists or headings — only a single flowing paragraph.
    """

    insights = call_llm(prompt)
    state["market"] = insights

    if "no demand" in insights.lower() or "poor fit" in insights.lower():
        state["terminate"] = True
    return state