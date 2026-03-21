import os
from typing import TypedDict
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

# Importing our custom tools
from tools import get_stock_data, get_recent_news

# Load environment variables (API Keys)
load_dotenv()

# 1. Define the State
# This dictionary will be passed around and updated by our nodes
class AgentState(TypedDict):
    ticker: str
    financial_data: str
    news_data: str
    report: str
    feedback: str
    revision_count: int
    is_approved: bool

# 1. LLM Pesado para Síntese Analítica (DeepSeek)
llm_analyst = ChatOpenAI(
    model="deepseek/deepseek-chat",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.2, # Um pouco de margem para redigir um texto fluido
)

# 2. LLM Rápido/Barato para Revisão Lógica (Llama 3.1 8B Nitro)
llm_reviewer = ChatOpenAI(
    model="meta-llama/llama-3.1-8b-instruct:nitro",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0, # Zero criatividade, queremos respostas binárias e diretas
)

# 2. Define the Nodes (The Agents)

def researcher_node(state: AgentState):
    """Gathers raw data using our tools."""
    print(f"\n[Researcher] Fetching data for {state['ticker']}...")
    fin_data = get_stock_data(state["ticker"])
    
    # We strip '.SA' or similar suffixes just for the news query to get broader results
    clean_company_name = state["ticker"].split(".")[0]
    news = get_recent_news(clean_company_name)
    
    return {"financial_data": fin_data, "news_data": news, "revision_count": 0}


def analyst_node(state: AgentState):
    """Writes or rewrites the report based on data and feedback."""
    print("\n[Analyst] Drafting the investment report...")
    
    system_prompt = (
        "You are a Senior Equity Analyst. "
        "Write a concise, professional investment memo based ONLY on the provided data. "
        "Format in Markdown. Include sections: Company Overview, Financial Health, Recent News, and Conclusion."
    )
    
    user_prompt = f"""
    Ticker: {state['ticker']}
    Financial Data: {state['financial_data']}
    Recent News: {state['news_data']}
    """
    
    if state.get("feedback"):
        user_prompt += f"\n\nReviewer Feedback to incorporate: {state['feedback']}"
        
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = llm_analyst.invoke(messages)
    return {"report": response.content}


def reviewer_node(state: AgentState):
    """Reviews the report. Approves it or sends back feedback."""
    print("\n[Reviewer] Evaluating the report...")
    
    system_prompt = (
        "You are the CIO. Review the following investment memo. "
        "It must be strictly based on the provided data, contain financial metrics (like P/E and Margins), "
        "and have no hallucinations. "
        "Respond with 'APPROVED' if it is excellent. "
        "If it needs work, respond with 'REJECTED' followed by specific instructions on what to fix."
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["report"])
    ]
    
    response = llm_reviewer.invoke(messages)
    evaluation = response.content
    
    if "APPROVED" in evaluation.upper():
        print("[Reviewer] Report APPROVED.")
        return {"is_approved": True, "feedback": ""}
    else:
        print(f"[Reviewer] Report REJECTED. Feedback: {evaluation}")
        # Increment revision count to avoid infinite loops
        return {"is_approved": False, "feedback": evaluation, "revision_count": state.get("revision_count", 0) + 1}


# 3. Define the Routing Logic
def route_review(state: AgentState):
    """Decides whether to finish or send back to the analyst."""
    if state.get("is_approved") or state.get("revision_count", 0) >= 5:
        return END
    return "analyst"


# 4. Build and Compile the Graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("reviewer", reviewer_node)

# Add edges
workflow.set_entry_point("researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "reviewer")
workflow.add_conditional_edges(
    "reviewer",
    route_review,
    {
        END: END,
        "analyst": "analyst"
    }
)

# Compile
app = workflow.compile()

# Test block
if __name__ == "__main__":
    print("--- Starting Agentic Workflow ---")
    initial_state = {"ticker": "NVDA"}
    
    # Run the graph
    final_state = app.invoke(initial_state)
    
    print("\n================ FINAL REPORT ================\n")
    print(final_state["report"])
    
    # Save the report to a markdown file
    with open("report.md", "w", encoding="utf-8") as f:
        f.write(final_state["report"])
    print("\n[System] Report saved to report.md")