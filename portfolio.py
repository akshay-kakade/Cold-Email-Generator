import pandas as pd
import uuid
import chromadb


class Portfolio:
    def __init__(self, file_path="resource/clean_fixed.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        # Use DuckDB backend to avoid SQLite version issues on Streamlit Cloud
        self.chroma_client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory=None,  # in-memory
                chroma_db_impl="duckdb+parquet"
            )
        )
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=[row["Techstack"]],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        results = self.collection.query(query_texts=skills, n_results=2)
        return [m["links"] for m in results.get("metadatas", []) if "links" in m]
