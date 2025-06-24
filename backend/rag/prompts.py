from langchain.prompts import PromptTemplate

def get_default_prompt_template():
    """
    Returns a secure prompt template that enforces department-based data access
    and requires source attribution in the answer.
    """
    return PromptTemplate(
        input_variables=["context", "question", "history"],
        template=(
            "You are a secure, helpful assistant for FinSolve.\n\n"
            # "You must answer the question using only the context provided below, which comes from documents the user is allowed to access based on their department role.\n"
            # "If the context does not provide enough information, reply with: \"Access to this information is restricted or not available based on your role.\"\n"
            "Always mention the source department and filename when referencing the information.\n\n"
            "{history}\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n\n"
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
