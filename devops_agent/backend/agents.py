
from crewai import Agent, Task, Crew
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

def run_agents(query, logs, context):
    sre = Agent(role="SRE Agent", goal="Understand issue", backstory="Expert SRE", llm=llm)
    rca = Agent(role="RCA Agent", goal="Find root cause", backstory="Debug expert", llm=llm)

    task = Task(
        description=f"Query:{query}\nLogs:{logs}\nContext:{context}\nFind root cause.",
        agent=rca
    )

    crew = Crew(agents=[sre, rca], tasks=[task])
    result = crew.kickoff()
    return str(result)
