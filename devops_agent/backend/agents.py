
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-4o-mini")

def run_agents(query, logs, context):
    sre = Agent(
        role="SRE Agent",
        goal="Understand issue",
        backstory="Expert SRE",
        llm=llm,
        verbose=True
    )

    rca = Agent(
        role="RCA Agent",
        goal="Find root cause",
        backstory="Debug expert",
        llm=llm,
        verbose=True
    )

    task1 = Task(
        description=f"""
        User Query:
        {query}

        Logs:
        {logs}

        Context:
        {context}

        Analyze the logs and summarize the issue clearly.
        """,
        agent=sre,
        expected_output="Detailed summary of the issue from logs"
    )

    task2 = Task(
        description=f"""
        Based on the following:

        Query: {query}
        Logs: {logs}
        Context: {context}

        Identify the root cause and suggest a fix.
        """,
        agent=rca,
        expected_output="""
        Return JSON:
        {
          "root_cause": "...",
          "reason": "...",
          "fix": "..."
        }
        """
    )

    crew = Crew(agents=[sre, rca], tasks=[task1, task2], verbose=True)

    result = crew.kickoff()
    return str(result)
