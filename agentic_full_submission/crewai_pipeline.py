
from crewai import Agent, Task, Crew

def run_crewai(feedback, category):
    
    bug_agent = Agent(role="Bug Analysis Agent", 
                      goal="Extract issue, steps, platform, severity", 
                      backstory="Debug expert")

    feature_agent = Agent(role="Feature Extractor Agent", 
                          goal="Extract feature, impact", 
                          backstory="PM expert")
    
    ticket_agent = Agent(role="Ticket Creator Agent", 
                         goal="Create structured ticket", 
                         backstory="Jira expert")
    
    qa_agent = Agent(role="Quality Critic Agent", 
                     goal="Validate ticket", 
                     backstory="QA expert")

    bug_task = Task(description=f"If Bug, analyze: {feedback}", agent=bug_agent)
    
    feature_task = Task(description=f"If Feature, analyze: {feedback}", agent=feature_agent)
    
    ticket_task = Task(description=f"Create ticket for: {feedback} with category {category}", agent=ticket_agent)
    
    qa_task = Task(description="Validate ticket completeness and accuracy", agent=qa_agent)

    crew = Crew(agents=[bug_agent, feature_agent, ticket_agent, qa_agent],
                tasks=[bug_task, feature_task, ticket_task, qa_task])
    return crew.kickoff()
