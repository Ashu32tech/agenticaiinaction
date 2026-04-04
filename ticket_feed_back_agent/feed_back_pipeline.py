
from crewai import Task, Crew
from feed_back_agents import agents
from observability import trace_id, log
import csv, os

def save(ticket):
    try:
        # Ensure output directory exists
        os.makedirs("output", exist_ok=True)

        file_path = os.path.join("output", "generated_tickets.csv")

        file_exists = os.path.isfile(file_path)

        # Ensure consistent field order
        fieldnames = [
            "trace_id",
            "source_id",
            "source_type",
            "category",
            "priority",
            "technical_details",
            "suggested_title"
        ]

        with open(file_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            # Write header only once
            if not file_exists:
                writer.writeheader()

            # Write row safely (missing keys handled)
            writer.writerow({key: ticket.get(key, "") for key in fieldnames})

    except PermissionError:
        print("❌ Permission denied: close the CSV file if open (Excel issue)")
    except Exception as e:
        print(f"❌ Failed to save ticket: {e}")

def run(row):
    t_id=trace_id()
    ag=agents()
    text=row.get("review_text") or row.get("body")

    log(t_id,"input",text)

    csv_reader = Task(description=f"Read: {row}",agent=ag["csv"],expected_output="Structured understanding of the input row")
    feedback_classifier = Task(description=f"Classify into Bug, Feature, Praise, Complaint, Spam: {text}",agent=ag["cls"],expected_output="One category label from [Bug, Feature, Praise, Complaint, Spam]")

    reader_classifier_crew=Crew(agents=list(ag.values()),tasks=[csv_reader,feedback_classifier])
    res=reader_classifier_crew.kickoff()
    category=str(res).split()[0]

    log(t_id,"category",category)

    if category=="Bug":
        bug_or_feture_requester = Task(
        description=f"Extract detailed bug report from: {text}",
        agent=ag["bug"],
        expected_output="Detailed bug report including steps, expected behavior, and actual behavior"
    )
    else:
        bug_or_feture_requester = Task(
        description=f"Extract feature request details from: {text}",
        agent=ag["feat"],
        expected_output="Detailed feature request including requirement, benefit, and priority"
    )

    ticket_creater = Task(
    description=f"Create structured ticket from: {text}",
    agent=ag["ticket"],
    expected_output="Structured ticket with title, description, priority, and category"
)
    ticket_validator = Task(
    description="Validate the created ticket for completeness and correctness",
    agent=ag["qa"],
    expected_output="Validation result with status (valid/invalid) and improvement suggestions"
)

    admin_crew=Crew(agents=list(ag.values()),tasks=[bug_or_feture_requester,ticket_creater,ticket_validator])
    analysis=admin_crew.kickoff()

    ticket={
        "trace_id":t_id,
        "source_id":row.get("review_id") or row.get("email_id"),
        "source_type":"app_store" if "review_id" in row else "email",
        "category":category,
        "priority":"High" if category=="Bug" else "Medium",
        "technical_details":str(analysis),
        "suggested_title": text[:50] if text else "No Title Available"
    }

    save(ticket)
    log(t_id,"ticket",ticket)

    return ticket
