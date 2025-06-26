# DS RPC 01: Internal chatbot with role based access control

# 🧠 FinSolve AI Chatbot – Role-Based RAG Assistant

A secure, intelligent AI assistant built with **LangChain**, **FastAPI**, **Streamlit**, and **OpenAI**.  
It delivers **department-specific insights** using **Retrieval-Augmented Generation (RAG)** and **Pandas Agent** with **RBAC (Role-Based Access Control)** logic.

---

## 📌 Features

- 🔐 **Authentication + Role-Based Access**  
  Users log in and receive department-specific access (HR, Finance, Engineering, etc.).

- 📄 **RAG Pipeline**  
  Retrieves and filters documents from vector DB based on user role and query intent.

- 🧮 **Pandas Agent Integration**  
  Supports querying structured CSV data (e.g., employee leave stats) using natural language.

- 🧠 **Conversation Memory**  
  Session-aware memory for coherent and contextual interactions.

- 🖥️ **FastAPI Backend + Streamlit Frontend**  
  Full-stack application with stateless backend and dynamic UI.

---

## 🗂️ Project Structure

```

chatbot/
│
├── backend/              # FastAPI + LangChain logic
│   ├── rag/              # Prompt templates, pipelines, memory, vector logic
│   ├── api/              # FastAPI route handlers
│   ├── .env              # Requires OPENAI\_API\_KEY
│   └── requirements.txt  # Backend dependencies
│
├── frontend/             # Streamlit UI
│   ├── .streamlit/
│   │   └── secrets.toml  # Streamlit secrets (API base URL)
│   └── requirements.txt  # Frontend dependencies
│
├── resources/            # HR CSVs and document folders
└── README.md

````

---

## ⚙️ Installation & Setup

### 🧩 Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)
pip install -r requirements.txt
````

Create `.env` file in `backend/`:

```env
OPENAI_API_KEY=your_openai_api_key
```

Start FastAPI server:

```bash
uvicorn main:app --reload
```

### 🖼️ Frontend (Streamlit)

```bash
cd frontend
pip install -r requirements.txt
```

Add API base URL in `frontend/.streamlit/secrets.toml`:

```toml
[api]
base_url = "https://chatbot-pct9.onrender.com"  # Replace with your actual backend URL
```

Run Streamlit:

```bash
streamlit run app.py
```

---

## 🔐 Roles & Access

| Role         | Access Level                                          |
| ------------ | ----------------------------------------------------- |
| HR           | Employee data, attendance, payroll, performance       |
| Finance      | Revenue, costs, reimbursements                        |
| Marketing    | Campaigns, metrics, customer feedback                 |
| Engineering  | Technical docs, DevOps pipelines, system architecture |
| C-Level Exec | Access to all departments                             |
| Employee     | General policies, FAQs, handbook                      |

---

## 📊 Sample Query Types

* **HR**: *"List all employees with more than 20 leaves remaining."*
* **Engineering**: *"What DevOps practices are followed in FinSolve?"*
* **Finance**: *"What were the Q2 vendor expenses?"*
* **General**: *"How can I apply for leave?"*

---

## 🚀 Deployment

* Backend hosted on **Render**: `https://chatbot-pct9.onrender.com`
* Frontend runs with Streamlit; can be deployed to **Streamlit Cloud** or **Railway**.

---

## 📚 Credits

* 💡 Built as part of the **[Codebasics Resume Project Challenge](https://codebasics.io/)** by **Dhaval Patel**
* 📘 LangChain learning via **CampusX YouTube Channel**
* 🧠 Powered by **OpenAI GPT models**

---

## 📎 License

This project is for educational purposes. Please credit if used or modified.
