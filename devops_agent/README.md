# 🚀 DevOps Agentic AI System

**CrewAI + LangGraph + MCP + Quadrant RAG + Streamlit**

---

## 🧠 Overview

This project implements a **production-style Agentic DevOps AI system** that can:

* Understand natural language DevOps issues
* Analyze Kubernetes pods & logs
* Retrieve context using **Quadrant RAG**
* Perform **root cause analysis using LLM (CrewAI)**
* Execute actions via **MCP tools (Kubernetes)**
* Include **Human-in-the-loop (HITL)** approval

---

## 🏗️ Architecture

```text
User (Streamlit UI)
        ↓
LangGraph (Workflow Orchestrator)
        ↓
CrewAI (Multi-Agent LLM Reasoning)
        ↓
RAG (Quadrant Vector DB)
        ↓
MCP Client (Tool Caller)
        ↓
MCP Server (@mcp.tool)
        ↓
Kubernetes Cluster
```

---

## 🧩 Components

### 🖥️ 1. Streamlit UI

* User inputs DevOps query
* Displays logs, decisions, and approval buttons

---

### 🔄 2. LangGraph (Workflow)

Controls execution flow:

* Fetch pods
* Fetch logs
* Retrieve RAG context
* Run agents
* Generate decision
* Await approval

---

### 🤖 3. CrewAI Agents

| Agent            | Role                |
| ---------------- | ------------------- |
| SRE Agent        | Understand query    |
| Kubernetes Agent | Analyze pod state   |
| Logs Agent       | Analyze logs        |
| RCA Agent        | Root cause analysis |
| Action Agent     | Suggest fix         |

---

### 📚 4. Quadrant RAG

Knowledge split into domains:

| Quadrant  | Description         |
| --------- | ------------------- |
| Logs      | Raw log patterns    |
| Incidents | Historical failures |
| Runbooks  | Fix instructions    |
| Metrics   | System signals      |

Uses:

* SentenceTransformers (embeddings)
* FAISS (vector search)

---

### 🔌 5. MCP (Model Context Protocol)

#### MCP Server

* Exposes tools via `@mcp.tool()`
* Runs independently

#### MCP Tools

```python
@get_pods(namespace)
@get_pod_logs(pod_name)
@restart_pod(pod_name)
@describe_pod(pod_name)
```

---

### 🔗 6. MCP Client

* Calls tools via HTTP
* Decouples execution from logic

---

## 🔄 Data Flow

```text
1. User enters query (Streamlit)
2. LangGraph starts workflow
3. MCP → fetch pods
4. MCP → fetch logs
5. RAG → retrieve similar incidents
6. CrewAI → analyze + find root cause
7. Decision generated
8. UI asks for approval (HITL)
9. MCP executes action (restart pod)
10. Result returned and displayed
```

---

## ⚙️ Installation

### 1️⃣ Clone project

```bash
git clone <your-repo>
cd devops-agent
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Set environment variable

```bash
export OPENAI_API_KEY=your_key
```

Windows:

```bash
setx OPENAI_API_KEY "your_key"
```

---

## ▶️ Running the System

### Step 1: Start MCP Server

```bash
python mcp_server.py
```

---

### Step 2: Run Streamlit UI

```bash
streamlit run app.py
```

---

### Step 3: (Optional CLI)

```bash
python run_mcp_client.py
```

---

## 🧪 Example Query

```text
"My pods are restarting continuously"
```

---

## ✅ Example Output

```text
Root Cause: OOMKilled (memory issue)

Suggested Action:
Restart pod + increase memory
```

---

## 🔐 Safety Features

* Human approval before execution
* Mock fallback if Kubernetes unavailable
* Exception handling in MCP calls

---

## ⚠️ Common Issues

### ❌ MCP not connecting

* Ensure server is running on port 8000

### ❌ kubectl error

* Install Kubernetes CLI
* Or use mock fallback

### ❌ Dependency conflicts

* Use virtual environment
* Upgrade `pydantic >= 2.12.2`

---

## 🚀 Future Enhancements

* Auto tool-calling by LLM
* LangGraph persistent state
* Multi-cluster support
* Slack/Teams approval
* Observability (Langfuse / tracing)
* Kafka event-driven automation

---

## 💡 Key Insight

This system separates:

* 🧠 Intelligence → CrewAI (LLM)
* 📚 Memory → RAG
* ⚙️ Execution → MCP
* 🔄 Control → LangGraph

👉 Result: **True Agentic AI DevOps Platform**

---

## 🏁 Summary

You now have a system that is:

* Modular
* Scalable
* LLM-powered
* Tool-integrated
* Production-ready (extensible)

---

**Built for modern DevOps + Agentic AI systems 🚀**
