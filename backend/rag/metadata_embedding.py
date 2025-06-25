from langchain_core.documents import Document
from models import get_embedding_model
from vectorstore import get_vector_store
department_docs = [
    Document(
    page_content="""This document provides a high-level overview of FinSolve’s Engineering practices and technology stack.
    - Covers the architecture of microservices, CI/CD pipelines, security protocols, and compliance initiatives (GDPR, DPDP, PCI-DSS).
    - Introduces development workflows, DevOps culture, monitoring strategies, and the tech roadmap involving AI and blockchain.
    - Intended for technical awareness and onboarding support across departments.""",
    metadata={"department": "general"}
    ),
    Document(
    page_content="""This document summarizes FinSolve’s Finance department structure and reporting approach.
    - Includes a general overview of quarterly performance reporting, budgeting, and strategic expense allocation.
    - Introduces key financial metrics tracked across the business such as revenue, margins, and cost efficiency.
    - Serves as a reference for understanding financial operations, useful to employees across roles.""",
    metadata={"department": "general"}
    ),
    Document(
    page_content="""This document offers an accessible summary of FinSolve’s official Employee Handbook for all employees.
    - Describes onboarding procedures, benefit eligibility, and leave types.
    - Details work hour expectations, attendance norms, and behavior guidelines.
    - Explains payroll policies, reimbursements, performance reviews, training, and feedback mechanisms.
    - Highlights company values, vision, legal compliance practices, and data security expectations.
    - Serves as a go-to reference for any employee seeking clarity on HR policies or workplace standards.""",
    metadata={"department": "general"}
        ),
    Document(
        page_content="""This document introduces how the HR department uses data to support people strategy and transparency.
        - Outlines the types of data collected: demographics, employment records, leave and attendance, performance ratings, etc.
        - Explains how trends in employee engagement, attrition, or leave utilization are monitored.
        - Describes how HR data supports talent planning, compliance tracking, and decision-making.
        - Helpful for employees interested in understanding how HR analytics inform policies and initiatives.""",metadata={"department": "general"}
        ),
    Document(
        page_content="""This overview introduces FinSolve’s HR data-driven practices and employee engagement tracking.
            - Summarizes how HR monitors leave usage, performance scores, and headcount trends.
            - Explains how these metrics support forecasting, compliance, and workforce planning.
            - Aims to build transparency on how HR decisions are informed.""", metadata={"department": "general"}
        )]


embedding_model = get_embedding_model()
vector_store = get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db")

def add_documents_to_vector_store(docs):
    """
    Adds a list of documents to the vector store with appropriate metadata.
    
    Args:
        docs (list): List of Document objects to be added.
    """
    for doc in docs:
        if not doc.metadata.get("department"):
            raise ValueError("Each document must have a 'department' metadata field.")
    
    vector_store.add_documents(docs)
    print(f"✅ Added {len(docs)} documents to the vector store.")

if __name__ == "__main__":
    try:
        add_documents_to_vector_store(department_docs)
        print("All documents added successfully.")
    except Exception as e:
        print(f"Error adding documents: {e}")

