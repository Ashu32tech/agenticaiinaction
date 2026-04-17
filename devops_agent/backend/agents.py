
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

llm = ChatOpenAI(model="gpt-4o-mini")

def run_agents(query, logs, context):
    sre = Agent(role="SRE Agent", goal="Understand issue", backstory="Expert SRE", llm=llm, verbose=True)
    rca = Agent(role="RCA Agent", goal="Find root cause", backstory="Debug expert", llm=llm, verbose=True)

    task1 = Task(
        description="Analyze logs and summarize issue",
        agent=sre,
        expected_output="Summary of issue"
    )

    task2 = Task(
        description="Find root cause based on summary",
        agent=rca,
        expected_output="Root cause + fix"
    )

    crew = Crew(agents=[sre, rca], tasks=[task1, task2])
    result = crew.kickoff()
    return str(result)
