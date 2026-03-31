from langgraph.graph import StateGraph
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase
from langchain_core.runnables.graph import MermaidDrawMethod


########################################
#docker run -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password --name neo4j-container neo4j
#docker run -d -p 6333:6333 -p 6334:6334 --name qdrant qdrant/qdrant
# VECTOR DB (QDRANT)
########################################

model = SentenceTransformer("all-MiniLM-L6-v2")

qdrant = QdrantClient(url="http://localhost:6333")

collection = "runbooks"

# create collection only if not exists
collections = qdrant.get_collections().collections
if collection not in [c.name for c in collections]:
    qdrant.create_collection(
        collection_name=collection,
        vectors_config=VectorParams(size=384, distance=Distance.COSINE)
    )

docs = [
    "OOMKilled means container ran out of memory",
    "CrashLoopBackOff occurs when container repeatedly fails",
    "Increase Kubernetes memory limits if pods crash"
]

points = []

for i, doc in enumerate(docs):
    embedding = model.encode(doc).tolist()

    points.append(
        PointStruct(
            id=i,
            vector=embedding,
            payload={"text": doc}
        )
    )

qdrant.upsert(collection_name=collection, points=points)


def rag_search(query):

    vector = model.encode(query).tolist()

    results = qdrant.query_points(
        collection_name=collection,
        query=vector,
        limit=2
    )

    return [r.payload["text"] for r in results.points]


########################################
# NEO4J GRAPH DB
########################################

driver = GraphDatabase.driver(
    "bolt://localhost:7687",
    auth=("neo4j", "password")
)


def get_dependencies(service):

    query = """
    MATCH (s:Service {name:$service})-[:DEPENDS_ON]->(d)
    RETURN d.name as name
    """

    with driver.session() as session:
        result = session.run(query, service=service)
        return [r["name"] for r in result]


########################################
# AGENTS
########################################

def planner_agent(state):

    return {
        "question": state["question"],
        "service": "payment-service"
    }


def rag_agent(state):

    docs = rag_search(state["question"])

    return {
        **state,
        "rag_docs": docs
    }


def graph_agent(state):

    deps = get_dependencies(state["service"])

    return {
        **state,
        "dependencies": deps
    }


def answer_agent(state):

    answer = f"""
Runbook suggestions:
{state.get("rag_docs", [])}

Service dependencies:
{state.get("dependencies", [])}
"""

    return {
        **state,
        "final_answer": answer
    }


########################################
# LANGGRAPH WORKFLOW
########################################

workflow = StateGraph(dict)

workflow.add_node("planner", planner_agent)
workflow.add_node("rag", rag_agent)
workflow.add_node("graph", graph_agent)
workflow.add_node("answer", answer_agent)

workflow.set_entry_point("planner")

# sequential flow (fix concurrent update error)
workflow.add_edge("planner", "rag")
workflow.add_edge("rag", "graph")
workflow.add_edge("graph", "answer")

graph = workflow.compile()


########################################
# RUN SYSTEM
########################################

graph_path = "langgraph_workflow.png"

print("Generating graph image...")

try:
    graph.get_graph().draw_mermaid_png(
        output_file_path=graph_path,
        draw_method=MermaidDrawMethod.PYPPETEER
    )
    print("Graph saved:", graph_path)

except Exception as e:
    print("Graph generation failed:", e)