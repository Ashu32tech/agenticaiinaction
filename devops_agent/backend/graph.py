from backend.agents import run_agents
from backend.mcp_tools import get_pods, get_pod_logs, restart_pod
from backend.rag.retriever import retrieve_context

def run_flow(query):
    state = {"query": query}

    # 🔌 MCP calls
    pods = get_pods("default")
    
    # handle MCP response safely
    if isinstance(pods, dict) and "result" in pods:
        pods = pods["result"]

    pod = pods[0]["name"]

    logs = get_pod_logs(pod)
    
    if isinstance(logs, dict) and "result" in logs:
        logs = logs["result"]

    # 📚 RAG
    context = retrieve_context(logs)

    # 🤖 CrewAI
    root_cause = run_agents(query, logs, context)

    decision = {
        "pod": pod,
        "root_cause": root_cause,
        "action": "restart_pod"
    }

    state.update({
        "pods": pods,
        "logs": logs,
        "context": context,
        "decision": decision
    })

    return state


def execute_action(state):
    pod = state["decision"]["pod"]

    result = restart_pod(pod)

    return result