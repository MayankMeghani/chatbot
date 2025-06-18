from pathlib import Path
from langchain_community.document_loaders import TextLoader, CSVLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter,RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableLambda, RunnableBranch
from pathlib import Path

HEADERS_TO_SPLIT_ON = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3")
]
DATA_DIR = Path("../resources/data")
SUPPORTED_EXTENSIONS = {".md", ".txt", ".csv"}
DEPARTMENTS = ["engineering", "marketing", "finance", "general","hr"]

embedding_model = get_embedding_model()
vector_store = get_vector_store(embedding_model, collection_name="documents", persist_directory="chroma_db")
markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=HEADERS_TO_SPLIT_ON)
csv_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

class DocumentProcessor:
    def __init__(self, vector_store, markdown_splitter, csv_splitter):
        self.vector_store = vector_store
        self.markdown_splitter = markdown_splitter
        self.csv_splitter = csv_splitter

        # Loaders
        self.load_md = RunnableLambda(self.load_markdown)
        self.load_csv = RunnableLambda(self.load_csv_file)

        # Splitters
        self.split_md = RunnableLambda(self.split_markdown)
        self.split_csv = RunnableLambda(self.split_csv_file)

        # Metadata
        self.add_metadata = RunnableLambda(self.attach_metadata)

        # Branching based on file extension
        self.branch_loader = self.create_loader_branch()
        self.branch_splitter = self.create_splitter_branch()

    def load_markdown(self, path: str):
        return TextLoader(path, encoding="utf-8").load()

    def load_csv_file(self, path: str):
        return CSVLoader(file_path=path).load()

    def split_markdown(self, docs):
        return self.markdown_splitter.split_text(docs[0].page_content)

    def split_csv_file(self, docs):
        return self.csv_splitter.split_documents(docs)

    def attach_metadata(self, context: dict):
        docs, source, department = context["docs"], context["source"], context["department"]
        for doc in docs:
            doc.metadata.update({
                "source": Path(source).name,
                "department": department
            })
        return {"docs": docs}

    def create_loader_branch(self):
        return RunnableBranch(
            (lambda path: Path(path).suffix.lower() == ".csv", self.load_csv),
            self.load_md
        )

    def create_splitter_branch(self):
        return RunnableBranch(
            (lambda docs: Path(docs[0].metadata.get("source", "")).suffix.lower() == ".md", self.split_md),
            self.split_csv  # fallback: CSV uses CSV splitter
        )

    def process_file(self, file_path: str, department: str):
        file_name = Path(file_path).name

        # Pipeline definition
        pipeline = (
            self.branch_loader
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