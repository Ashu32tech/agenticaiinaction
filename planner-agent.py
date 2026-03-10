from agents import Agent, Runner
from dotenv import load_dotenv
import asyncio

# Load environment variables (OPENAI_API_KEY etc.)
load_dotenv(override=True)

# -------------------------------------------------
# Production-grade Planner / Reasoning Agent
# -------------------------------------------------
# planner_agent = Agent(
#     name="ProductionPlannerAgent",
#     model="gpt-4o-mini",
#     instructions="""
# You are a senior production engineer acting as an autonomous planning agent.

# For every task:
# 1. Create a clear step-by-step investigation or execution plan.
# 2. Explicitly reason about constraints, risks, and trade-offs.
# 3. Clerly articulate assumptions and unknowns that need to be validated.
# 4. Execute the plan conceptually and produce an actionable final answer.
# 5. Prioritize recommendations by impact and effort.

# Your output must be structured, concise, and suitable for real production use.
# """
# )

# Create planner agent
planner_agent = Agent(
    name="ProductionEngineerPlanner",
    
    instructions="""
You are a senior production engineer acting as an autonomous planning agent.

Your task is ONLY to generate a troubleshooting and remediation plan.
You must NOT execute any actions.

When given a production issue:
1. Analyze the problem
2. Identify possible root causes
3. Create a step-by-step investigation plan
4. Suggest remediation strategies
5. Suggest monitoring/validation steps

Return the response as a structured numbered plan.
"""
)
# -------------------------------------------------
# Async runner
# -------------------------------------------------
async def main():
    # query = """
    # Our n8n workflows started failing intermittently after moving from SQLite
    # to MySQL running in Docker.

    # Observed symptoms:
    # - Random "connection timeout" errors
    # - MySQL CPU spikes during peak hours
    # - Some failures show "too many connections" errors
    # - Failures increase when multiple workflows run in parallel

    # Environment:
    # - n8n + MySQL containers on the same Docker network
    # - MySQL uses a Docker volume
    # - No connection pool tuning done yet

    # Task:
    # Create a step-by-step investigation plan and propose concrete fixes.
    # End with a recommended stable production configuration.
    # """
    query = """
    Order service latency increased and users are experiencing API timeouts.
    """


    result = await Runner.run(planner_agent, query)

    print("\n===== FINAL AGENT OUTPUT =====\n")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
