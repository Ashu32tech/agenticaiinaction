
from crewai import Agent

def get_agents():
    return {
        "csv_reader": Agent(role="CSV Reader Agent", 
                            goal="Read CSV data", 
                            backstory="CSV expert"),
        "classifier": Agent(role="Feedback Classifier Agent", 
                            goal="Classify feedback", 
                            backstory="NLP expert"),
        "bug": Agent(role="Bug Analysis Agent", 
                     goal="Extract bug details", 
                     backstory="Debug expert"),
        "feature": Agent(role="Feature Extractor Agent", 
                         goal="Extract feature details", 
                         backstory="PM expert"),
        "ticket": Agent(role="Ticket Creator Agent", 
                        goal="Create structured ticket and save CSV", 
                        backstory="Jira expert"),
        "qa": Agent(role="Quality Critic Agent", 
                    goal="Validate ticket accuracy", 
                    backstory="QA expert")
    }
