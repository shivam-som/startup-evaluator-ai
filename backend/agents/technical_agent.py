from backend.utils.llm_client import call_llm

def run(state: dict) -> dict:
    if state.get("terminate"):
        return state

    idea = state["idea"]
    prompt = f"""
        You are a Technical Reviewer. Evaluate the feasibility of the startup idea "{idea}" in one concise paragraph. 
        Start with: As a Technical Reviewer. 
        Summarize 3-4 key insights about technical feasibility, integration, scalability, and risks. 
        Do not use lists or headings — only a single flowing paragraph.
    """

    insights = call_llm(prompt)
    state["technical"] = insights

    if "not feasible" in insights.lower():
        state["terminate"] = True
    return state