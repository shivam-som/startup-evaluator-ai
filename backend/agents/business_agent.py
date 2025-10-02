from backend.utils.llm_client import call_llm

def run(state: dict) -> dict:
    if state.get("terminate"): return state
    idea = state["idea"]
    prompt = f"""
        You are a Business Strategist. Evaluate the startup idea "{idea}" in one concise paragraph. 
        Start with: As a Business Strategist. 
        Summarize 3-4 key insights about business model, pricing, go-to-market, and risks. 
        Do not use lists or headings — only a single flowing paragraph.
    """

    insights = call_llm(prompt)
    state["business"] = insights.strip()
    return state
