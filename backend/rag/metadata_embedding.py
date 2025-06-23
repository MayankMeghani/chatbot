from langchain_core.documents import Document
from models import get_embedding_model
from vectorstore import get_vector_store
department_docs = [
    Document(page_content="""Documents FinSolve’s complete technical architecture
            - Documents FinSolve’s complete technical architecture and engineering processes.
            - Includes microservices, CI/CD pipelines, security models, and compliance (GDPR, DPDP, PCI-DSS).
            - Covers development standards, DevOps practices, monitoring, and future tech roadmap (AI, blockchain).
            - Owned by the Engineering Team; updated quarterly.
            - Access is restricted to Engineering Team and C-Level Executives due to high sensitivity.
            - Serves as a reference for audits, onboarding, scaling, and system maintenance.""", metadata={"department": "engineering"}),
    Document(page_content="""Documents FinSolve’s quarterly financial performance
            - Documents FinSolve’s quarterly financial performance for the year 2024.
            - Includes revenue, income, gross margin, marketing spend, vendor costs, and cash flow data.
            - Provides detailed expense breakdowns and risk mitigation strategies for each quarter.
            - Owned by the Finance Team; updated quarterly.
            - Access is restricted to the Finance Team and C-Level Executives due to financial sensitivity.
            - Serves as a key reference for financial planning, audits, investor reporting, and strategic decisions.""", metadata={"department": "finance"}),
    Document(page_content="""Documents FinSolve’s marketing strategies and campaigns
            - Includes campaign overviews, spend allocations, customer acquisition targets, revenue projections, conversion and ROI benchmarks.
            - Provides detailed highlights on digital marketing, B2B initiatives, customer retention programs, and preliminary performance analysis.
            - Owned by the Marketing Team; refreshed quarterly.
            - Serves as a key reference for quarterly planning, budget allocation, performance reviews, and Q1 2025 strategy recommendations.""", metadata={"department": "marketing"}),
    Document(page_content="""Documents FinSolve’s HR policies and procedures
             - Documents HR’s employee dataset, covering 100 records with demographics, employment, compensation, leave, attendance, and performance fields.
            - Provides workforce composition insights, turnover tracking, leave utilization, and performance trend analysis.
            - Owned by the HR & People Analytics team; refreshed monthly to capture hires, exits, and updates.
            - Serves as a key reference for talent forecasting, compensation reviews, compliance reporting, and employee engagement initiatives.""", metadata={"department": "hr"}),
    Document(page_content="""Documents FinSolve’s general company policies and procedures
            - Comprehensive company policies covering onboarding & benefits, leave policies, work hours & attendance, code of conduct & workplace behavior, health & safety, compensation & payroll, reimbursement, training & development, performance & feedback, privacy & data security, exit procedures, FAQs, and miscellaneous guidelines.
            - Purpose: Serves as the authoritative guide for employees on company vision, values, HR processes, legal compliance, and workplace standards.
            - Ownership & Maintenance: Owned by the Human Resources Department; reviewed and updated annually or as regulations and company practices.
            - Usage: Key reference for new-hire orientation, policy clarifications, leave & attendance management, performance reviews, and exit procedures.""", metadata={"department": "general"})
    ]


embedding_model = get_embedding_model()
vector_store = get_vector_store(embedding_model, collection_name="metadata", persist_directory="chroma_db")

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

