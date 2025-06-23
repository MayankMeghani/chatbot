from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter,RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda, RunnableBranch
from pathlib import Path
from models import get_embedding_model
from vectorstore import get_vector_store

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]
DATA_DIR = Path("../resources/data")
SUPPORTED_EXTENSIONS = {".md", ".txt"}
DEPARTMENTS = ["engineering", "marketing", "finance", "general","hr"]

embedding_model = get_embedding_model()
vector_store = get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db")
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

class DocumentProcessor:
    def __init__(self, vector_store, markdown_splitter, text_splitter):
        self.vector_store = vector_store
        self.markdown_splitter = markdown_splitter
        self.text_splitter = text_splitter

        self.loader = RunnableLambda(self.load_files)

        self.split_md = RunnableLambda(self.split_markdown)
        self.text_splitter = RunnableLambda(self.split_text_file)

        self.add_metadata = RunnableLambda(self.attach_metadata)

        self.branch_splitter = self.create_splitter_branch()

    def load_files(self, path: str):
        return TextLoader(path, encoding="utf-8").load()

    def split_markdown(self, docs):
        return self.markdown_splitter.split_text(docs[0].page_content)

    def split_text_file(self, docs):
        return self.text_splitter.split_documents(docs)

    def attach_metadata(self, context: dict):
        docs, source, department = context["docs"], context["source"], context["department"]
        for doc in docs:
            doc.metadata.update({
                "source": Path(source).name,
                "department": department
            })
        return {"docs": docs}


    def create_splitter_branch(self):
        return RunnableBranch(
            (lambda docs: Path(docs[0].metadata.get("source", "")).suffix.lower() == ".md", self.split_md),
            self.split_text_file  # fallback: CSV uses CSV splitter
        )

    def process_file(self, file_path: str, department: str):
        file_name = Path(file_path).name

        # Pipeline definition
        pipeline = (
            self.loader
            | self.branch_splitter
            | (lambda docs: {"docs": docs, "source": file_name, "department": department})
            | self.add_metadata
            | RunnableLambda(lambda x: self.vector_store.add_documents(x["docs"]))
        )

        # Execute the pipeline
        pipeline.invoke(file_path)
        print(f"✅ Processed: {file_path} for department: {department}")



if __name__ == "__main__":
    processor = DocumentProcessor(vector_store, markdown_splitter, csv_splitter)

    for department in DEPARTMENTS:
        dept_dir = DATA_DIR / department
        if not dept_dir.exists():
            print(f"⚠️  Missing directory: {dept_dir}")
            continue

        print(f"\n📂 Department: {department}")
        for file_path in dept_dir.glob("*"):
            if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
                try:
                    print(f"  🔄 {file_path.name}")
                    processor.process_file(str(file_path), department)
                except Exception as e:
                    print(f"  ❌ Failed: {file_path.name} -> {e}")