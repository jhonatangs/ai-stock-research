# MISSION: Auto-Research Development Loop

You are an autonomous AI software engineer. Your goal is to test, debug, and perfect the "AI Stock Research Tool" located in this directory. 

## Context
This project uses LangGraph to orchestrate two models (DeepSeek for analysis, Llama 3.1 8B for review) and tools (yfinance, DuckDuckGo) to generate a financial report (`report.md`) for a given stock ticker.

## Execution Rules
1. **Run the System:** Execute `python graph.py` in the terminal.
2. **Monitor the Output:** Watch the terminal logs. Ensure the nodes [Researcher -> Analyst -> Reviewer] are communicating and that the script completes without Python tracebacks.
3. **Handle Errors:** If the script crashes or throws an API error, inspect the code in `graph.py` or `tools.py`, fix the bug, and run it again.
4. **Evaluate the Artifact:** Once the script runs successfully, read the generated `report.md`. 
    - Does it look like a professional investment memo?
    - Does it include hard data (P/E ratio, Margins, recent news)?
    - Is the formatting clean Markdown?
5. **Iterate:** If the report is poor, tweak the `system_prompt` inside the `analyst_node` in `graph.py` to improve the output, then run again.
6. **Finalize:** Once the code runs smoothly and `report.md` is excellent, stop. Do not make unnecessary changes.

Begin by running `python graph.py`.