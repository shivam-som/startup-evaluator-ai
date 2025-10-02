from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from backend.agents import market_agent, technical_agent, business_agent, final_agent, recommendation_agent

class EvalState(TypedDict, total=False):
    idea: str
    market: Optional[str]
    technical: Optional[str]
    business: Optional[str]
    report: Optional[str]
    recommendation: Optional[str]
    terminate: Optional[bool]

graph = StateGraph(EvalState)

graph.add_node("market", market_agent.run)
graph.add_node("technical", technical_agent.run)
graph.add_node("business", business_agent.run)
graph.add_node("recommendation", recommendation_agent.run)
graph.add_node("final", final_agent.run)

graph.add_edge("market", "technical")
graph.add_edge("technical", "business")
graph.add_edge("business", "recommendation")

graph.set_entry_point("market")
graph.set_finish_point("final")

workflow = graph.compile()
