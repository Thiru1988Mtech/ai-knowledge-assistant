import logging
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, ToolMessage

from backend.agent.state import AgentState
from backend.agent.tools import TOOLS, TOOL_MAP
from backend.config import settings

logger = logging.getLogger(__name__)

# 🔁 Prevent infinite loops
MAX_ITERATIONS = 5

# 🧠 LLM (Agent Brain)
llm = ChatOllama(
    model=settings.llm_model,
    base_url=settings.ollama_base_url,
    temperature=0.1,
).bind_tools(TOOLS)


# 🧾 System Prompt (controls agent behaviour)
AGENT_SYSTEM = """
You are an intelligent AI assistant using ReAct reasoning.

Rules:
- Think step by step
- Use tools when needed
- Never guess
- Prefer tool output over assumptions
- Provide a clear final answer
"""


# 🔥 FIX: Normalize tool arguments
def normalize_args(args: dict):
    """
    Fix structured tool arguments from LLM.
    Example:
    {'query': {'type': 'string', 'value': 'RAG'}}
    → {'query': 'RAG'}
    """
    fixed = {}

    for k, v in args.items():
        if isinstance(v, dict) and "value" in v:
            fixed[k] = v["value"]
        else:
            fixed[k] = v

    return fixed


# 🧠 NODE 1: Agent Thinking
def agent_node(state: AgentState):
    iteration = state.get("iteration_count", 0)

    # 🚫 Stop infinite loops
    if iteration >= MAX_ITERATIONS:
        return {
            "final_answer": "Max iterations reached. Please refine your question.",
            "steps": ["[STOP] Max iterations reached"],
            "iteration_count": iteration + 1
        }

    messages = [SystemMessage(content=AGENT_SYSTEM)] + state["messages"]

    response = llm.invoke(messages)

    return {
        "messages": [response],
        "steps": [f"Thought: {response.content[:100]}"],
        "iteration_count": iteration + 1
    }


# 🛠 NODE 2: Tool Execution
def tool_node(state: AgentState):
    last_message = state["messages"][-1]

    tool_outputs = []
    steps = []

    for tool_call in last_message.tool_calls:
        tool_name = tool_call["name"]
        raw_args = tool_call["args"]

        # 🔥 CRITICAL FIX
        args = normalize_args(raw_args)

        try:
            result = TOOL_MAP[tool_name].invoke(args)

            steps.append(f"Action: {tool_name}({args})")
            steps.append(f"Observation: {str(result)[:150]}")

        except Exception as e:
            logger.error(f"Tool error: {e}")
            result = f"Tool error: {e}"

        tool_outputs.append(
            ToolMessage(
                content=str(result),
                tool_call_id=tool_call["id"]
            )
        )

    return {
        "messages": tool_outputs,
        "steps": steps
    }


# 🎯 NODE 3: Final Answer
def final_node(state: AgentState):
    return {
        "final_answer": state["messages"][-1].content
    }


# 🔀 Router (Decision Maker)
def router(state: AgentState):
    last = state["messages"][-1]

    # If tool call exists → go to tool_node
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"

    # Else → finish
    return "end"