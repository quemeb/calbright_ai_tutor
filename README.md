# Calbright AI Tutor (Multi-Agent ADK System)

A fully functional **multi-agent AI Tutor** built using **Google’s Agent Development Kit (ADK)** to support students in Calbright College’s Data Analytics program.  
This project is submitted under the **Agents for Good** track of the *Kaggle Agents Intensive Capstone Project*.

---

## 🧠 Project Overview

Adult learners in Calbright College competency-based education programs often need:

- On-demand help with **SQL**
- Support understanding **Google Sheets / spreadsheets**
- Career guidance about **data analytics roles**
- Personalized explanations at their own pace  
- Consistent support even when instructors are offline

This project builds an AI Tutor that uses **multi-agent specialization** and **retrieval-augmented generation (RAG)** to provide accurate, curriculum-aligned answers.

---

## 🎯 Problem Statement

Students in Calbright’s Data Analytics program struggle with:

- Determining whether a question is SQL or Sheets related  
- Finding information within long PDFs  
- Learning asynchronously outside instructor hours  
- Balancing school, work, and family  
- Understanding realistic career pathways  

Traditional chatbots hallucinate or give generic answers.  
This system solves that using **specialized agents + grounded context via RAG**.

---

## 🚀 Solution

This project implements a **four-agent architecture** powered by Gemini 2.5 Flash:

### **1. SQL Agent**
- Answers SQL questions  
- Uses RAG (`course_rag`) for grounded explanations  
- Covers SELECT, WHERE, JOIN, GROUP BY, aggregates, etc.

### **2. Sheets Agent**
- Supports Google Sheets formulas, pivot tables, charts, data cleaning  
- Uses the same RAG engine filtered for “Sheets” materials  

### **3. Career Agent**
- Uses **Google Search built-in tool** for real job-market insights  
- Helps students understand analyst, BI, and database roles  

### **4. Supervisor Agent**
- Routes student questions to the correct specialist  
- Unifies the final answer in a friendly tutor voice  
- Maintains conversation quality and context consistency  

All agents operate using ADK **sessions and memory**.

---

## 🧰 ADK Features Demonstrated

This project incorporates more than the required three (3) ADK capabilities:

### **✔ Multi-Agent System**
- SQL Agent  
- Sheets Agent  
- Career Agent  
- Supervisor (routing) Agent  

### **✔ Tools**
- Custom tool: `course_rag`  
- Built-in tool: `google_search`  
- FAISS vector search  

### **✔ Sessions & Memory**
- Implements `InMemorySessionService`  
- Manages multi-turn conversations with context  

### **✔ Context Engineering**
- RAG context filtered by module (`SQL` vs `Sheets`)  
- Cleaned, chunked Calbright course materials used for FAISS index  

### **✔ Async Runner**
- Fully async streaming conversation loop (`run_tutor.py`)

These demonstrate meaningful and real use of ADK’s agent architecture.

---

## 📁 Project Structure

```text

calbright_ai_tutor/
│
├── calbright_adk/
│   ├── agents/
│   │   ├── sql_agent.py
│   │   ├── sheets_agent.py
│   │   ├── career_agent.py
│   │   ├── supervisor_agent.py
│   │   └── __init__.py
│   │
│   ├── tools/
│   │   ├── course_rag.py
│   │   ├── search_tool.py
│   │   └── __init__.py
│   │
│   └── coordinator.py
│
├── embeddings/
│   ├── faiss_index.bin
│   └── metadata.json
│
├── data/
│
├── build_index.py
├── rag_tools.py
├── run_tutor.py
├── requirements.txt
├── .env.example
└── README.md
```
---

## ▶️ Running the Tutor Locally

### 1. Create a virtual environment
    python -m venv venv
    # Windows:
    # venv\Scripts\activate
    # macOS / Linux:
    # source venv/bin/activate

### 2. Install dependencies
    pip install -r requirements.txt

### 3. Add your API key

Copy `.env.example` to `.env` and fill in:

    GOOGLE_API_KEY=your-key-here

### 4. Run the tutor
    python run_tutor.py

You will be prompted for a student ID or email.  
The ADK session begins and the multi-agent tutor comes online.

---

## 🧰 Retrieval-Augmented Generation (RAG)

This project uses a custom FAISS vectorstore:

- `rag_tools.py` implements the RAGEngine  
- `build_index.py` loads Calbright course materials and builds the index  
- Documents are chunked, embedded, and stored as FAISS binary under `embeddings/`

Agents access RAG via:

    course_rag(question, module="SQL")

or

    course_rag(question, module="Sheets")

This ensures grounded, accurate responses aligned with Calbright curriculum.

---

## 🎓 Value & Impact

This AI Tutor can:

- Support thousands of asynchronous learners  
- Reduce instructor support load  
- Improve student retention  
- Increase access to high-quality education for adult learners  
- Provide accurate, hallucination-resistant tutoring  

This aligns directly with the Agents for Good track by improving educational equity.

---

## 🏆 Capstone Requirements Checklist

| Requirement                | Status |
|----------------------------|--------|
| Multi-agent system         | ✅     |
| Tools (custom + built-in)  | ✅     |
| Memory + sessions          | ✅     |
| Context engineering        | ✅     |
| Async runner               | ✅     |
| Documentation              | ✅     |
| GitHub repo                | ✅     |
| (Optional) Deployment      | Not required |
| (Optional) Video           | Optional |

---

## 👤 Author

**Bryan Queme**  
