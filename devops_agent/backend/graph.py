from backend.agents import run_agents
from backend.mcp_tools import get_pods, get_pod_logs, restart_pod
from backend.rag.retriever import retrieve_context
import time


def run_flow(query):
    state = {"query": query}

    try:
        print("🚀 Starting run_flow")

        pods = get_pods("micro-demo")
        if isinstance(pods, dict) and "result" in pods:
            pods = pods["result"]

        if not pods:
            return {"error": "No pods found"}

        pod = next(
            (p["name"] for p in pods if p.get("status") != "Running"),
            pods[0]["name"]
        )

        print("📦 Selected pod:", pod)

        logs = get_pod_logs(pod)
        if isinstance(logs, dict) and "result" in logs:
            logs = logs["result"]

        logs = extract_key_lines(logs)

        print("📜 Logs extracted")

        # RAG
        context = retrieve_context(logs)

        print("📚 Context ready")

        # CrewAI (can be slow)
        start = time.time()
        root_cause = run_agents(query, logs, context)
        print(f"🧠 CrewAI completed in {time.time() - start:.2f}s")

        decision = {
            "pod": pod,
            "root_cause": root_cause,
            "action": "restart_pod",
            "requires_approval": True
        }

        state.update({
            "pods": pods,
            "logs": logs,
            "context": context,
            "decision": decision
        })

        return state

    except Exception as e:
        print("❌ ERROR:", e)
        return {"error": str(e)}


def extract_key_lines(logs):
    keywords = ["error", "exception", "fail", "oomkilled", "crashloopbackoff"]
    return "\n".join(
        [line for line in logs.split("\n") if any(k in line.lower() for k in keywords)]
    )


def execute_action(state):
    try:
        decision = state.get("decision", {})

        if decision.get("requires_approval"):
            return {"status": "blocked", "message": "Approval required"}

        pod = decision.get("pod")
        if not pod:
            return {"error": "No pod specified"}

        print("⚡ Restarting pod:", pod)

        result = restart_pod(pod)

        return {
            "status": "success",
            "pod": pod,
            "result": result
        }

    except Exception as e:
        return {"error": str(e)}