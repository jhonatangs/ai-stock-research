# AI Stock Research Agent (Autonomous Loop)

A stateful, autonomous AI agent designed to research, analyze, and draft institutional-grade investment memos for publicly traded companies.

This project implements an autonomous development and execution loop inspired by the `karpathy/autoresearch` pattern, utilizing an AI terminal agent (Antigravity) to orchestrate the workflow.

## 🧠 Architecture & LLM Routing

To balance deep reasoning capabilities with cost and speed efficiency, this system utilizes a **Multi-Agent Stateful Workflow** (via LangGraph) with strategic **LLM Routing** via OpenRouter:

1. **Researcher Node (Python Tools):** Gathers raw financial data (P/E, margins, debt) using `yfinance` and macroeconomic context using `DuckDuckGo Search`.
2. **Analyst Node (DeepSeek V3):** The "heavy lifter". Synthesizes the raw data into a structured financial report.
3. **Reviewer Node (Llama 3.1 8B Nitro):** The "fast logic gate". Evaluates the report strictly for formatting and required metrics. If the report lacks hard data, it rejects it and loops back to the Analyst.

## ⚙️ How to Run (The Antigravity Loop)

Instead of running a standard linear script, this project is designed to be executed by an autonomous terminal agent.

**1. Clone and Install:**
```bash
git clone [https://github.com/jhonatangs/ai-stock-research.git](https://github.com/jhonatangs/ai-stock-research.git)
cd ai-stock-research
pip install -r requirements.txt
```

**2. Environment Variables:**
Create a `.env` file in the root directory:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

**3. Execute the Autonomous Loop:**
If you have Antigravity (or Claude Code / OpenClaw) installed, simply pass the master prompt to the agent:
```bash
antigravity "read the antigravity_prompt.md file and execute the instructions"
```
*The agent will read the instructions, execute the LangGraph pipeline, monitor the state transitions, and save the final verified output to `report.md`.*

## 💡 Bonus: Product Idea (AI-Native CRM Integration)

**The Portfolio Co-Pilot**
The underlying architecture of this agent (LangGraph + RAG/Web Search + LLM Routing) can be directly integrated into the AI-native CRM. 

Instead of a passive address book, the CRM becomes an active Co-Pilot:
- The system periodically runs this exact graph for every asset held in a client's portfolio.
- If the `Analyst Node` detects a fundamental shift (e.g., a sudden drop in profit margins or a regulatory news catalyst), it triggers an alert.
- A new `Communications Node` cross-references this shift with the client's risk profile and automatically drafts a proactive, personalized email for advisor to review and send.
