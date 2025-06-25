from langchain.prompts import PromptTemplate

def get_default_prompt_template():
    return PromptTemplate(
        input_variables=["context", "question", "history"],
        template=(
            "You are FinSolve’s AI assistant designed to provide secure, helpful, and professional answers.\n\n"
            "Context may include internal documents filtered based on the user's department role. "
            "Use this context when relevant, but you may also rely on your general knowledge if no context is provided.\n\n"

            "Guidelines:\n"
            "- Prefer using the context if it's available.\n"
            "- If no relevant context is found, use your best judgment to help the user professionally.\n"
            "- For sensitive topics (e.g., finance, HR, engineering), do **not** guess. Only use the context.\n"
            "- If a sensitive question lacks context, respond with: \"Access is restricted or information is not available for your role.\"\n"
            "- When referencing internal content, always mention the source department and file name.\n\n"

            "Conversation History:\n{history}\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n"
        )
    )



destinations = [
    {"name": "pandas", "description": "Questions involving employee datasets such as leave, performance, compensation, headcount, attendance, or any structured table requiring calculations, trends, or filtering."},
    {"name": "rag", "description": "Questions about HR policies, rules, guidelines, company FAQs, or written documents."}
]

destination_str = "\n".join([f"{d['name']}: {d['description']}" for d in destinations])

def get_routing_prompt():
    return PromptTemplate.from_template(f"""
You are a query router for a role-based HR assistant. 
You must classify user queries as either "pandas" or "rag".

**Data Available:**
HR has a structured dataset of 100 employees with fields like:
- Demographics
- Compensation
- Leave balances and utilization
- Attendance
- Performance scores
- Employment start/end dates

This data is updated monthly and used for analytics, forecasting, reviews, and reporting.

**Routing Options:**
{destination_str}

Classify the question strictly:
- If it's about **data analysis**, **counts**, **employee comparisons**, or anything answerable from the dataset → respond with `pandas`
- If it's about **policies**, **rules**, or **textual HR knowledge** → respond with `rag`

Examples:
- "How many employees took more than 10 leave days?" → pandas
- "What is the leave policy for contractors?" → rag

Respond with exactly one word: **pandas** or **rag**

Question: {{input}}
""")

def get_pandas_agent_prompt():
    return PromptTemplate.from_template("""
Given the past conversation and the current query, rewrite the user’s question clearly and unambiguously.

Chat History:
{chat_history}

Current Question:
{question}

Rewritten Query:
""")
    
def get_format_prompt():
    return PromptTemplate.from_template("""
You are a helpful assistant. Format the following output into a clean, readable response.

Original Query: {query}
Agent Output: {raw_output}

Final Answer:
""")