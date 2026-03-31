from agents import Agent, Runner
from dotenv import load_dotenv
import subprocess

# Load environment variables (OPENAI_API_KEY etc.)
load_dotenv(override=True)

# -----------------------------------
# Planner Agent
# -----------------------------------

planner = Agent(
    name="PlannerAgent",
    instructions="""
You are a senior production engineer.

Analyze the incident and propose a remediation plan.

Rules:
- Only suggest actions
- Do NOT execute anything
- Provide clear operational steps
"""
)

# -----------------------------------
# Executor Agent
# -----------------------------------

executor = Agent(
    name="ExecutorAgent",
    instructions="""
You are an execution agent.

Execute the remediation action provided.

Example actions:
- restart service
- scale Kubernetes deployment
"""
)

# -----------------------------------
# Execution Function
# -----------------------------------

def execute_command(plan):

    if "scale" in plan.lower():
        cmd = "kubectl scale deployment order-service --replicas=6"
        return subprocess.getoutput(cmd)

    if "restart" in plan.lower():
        cmd = "kubectl rollout restart deployment order-service"
        return subprocess.getoutput(cmd)

    return "No executable command detected"


# -----------------------------------
# Human Approval Function
# -----------------------------------

def human_approval(plan):

    print("\n===== Proposed Plan =====")
    print(plan)

    decision = input("\nApprove execution? (yes/no): ")

    return decision.lower() == "yes"


# -----------------------------------
# Incident Input
# -----------------------------------

incident = """
Users report API timeouts from order-service.
Latency increased to 4 seconds.
"""

# -----------------------------------
# Step 1: Planner creates plan
# -----------------------------------

plan_result = Runner.run_sync(planner, incident)

plan = plan_result.final_output

# -----------------------------------
# Step 2: Human Approval
# -----------------------------------

approved = human_approval(plan)

# -----------------------------------
# Step 3: Execute using Executor Agent
# -----------------------------------

if approved:

    print("\nHuman approved execution.")

    exec_result = Runner.run_sync(executor, plan)

    system_result = execute_command(plan)

    print("\n===== Execution Result =====")
    print(exec_result.final_output)
    print(system_result)

else:

    print("\nExecution cancelled by human.")