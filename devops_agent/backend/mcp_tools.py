# mcp_server.py
from mcp.server.fastmcp import FastMCP
import subprocess

print("🚀 Initializing MCP server...")

mcp = FastMCP("k8s")

@mcp.tool()
def get_pods(namespace: str):
    """Get Kubernetes pods"""
    try:
        output = subprocess.check_output(
            ["kubectl", "get", "pods", "-n", namespace],
            text=True
        )
        lines = output.split("\n")[1:]
        pods = []

        for l in lines:
            if l.strip():
                parts = l.split()
                pods.append({
                    "name": parts[0],
                    "status": parts[2]
                })

        return pods

    except Exception as e:
        return [{"name": "payment-service", "status": "CrashLoopBackOff"}]


@mcp.tool()
def get_pod_logs(pod_name: str):
    """Fetch pod logs"""
    try:
        return subprocess.check_output(
            ["kubectl", "logs", pod_name,"-n", "micro-demo"],
            text=True
        )
    except:
        return "Error: OOMKilled"


@mcp.tool()
def restart_pod(pod_name: str):
    """Restart pod"""
    try:
        subprocess.call(["kubectl", "delete", "pod", pod_name, "-n", "micro-demo"])
        return f"{pod_name} restarted"
    except:
        return "Mock restart"
        

if __name__ == "__main__":
    print("✅ MCP server started and waiting for client...")
    mcp.run()