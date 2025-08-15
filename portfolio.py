import chromadb
import pandas as pd
import uuid
import os

class Portfolio:
    def __init__(self, file_path="resource/clean_fixed.csv"):
        self.file_path = file_path
        os.makedirs(".chromadb", exist_ok=True)

        # Use DuckDB instead of SQLite (avoids system sqlite version issues)
        self.chroma_client = chromadb.Client(
            settings=chromadb.config.Settings(
                persist_directory=".chromadb",
                chroma_db_impl="duckdb+parquet"
            )
        )

        self.data = pd.read_csv(self.file_path)
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                self.collection.add(
                    documents=row["Techstack"],
                    metadatas={"links": row["Links"]},
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        result = self.collection.query(query_texts=skills, n_results=2)
        return result.get("metadatas", [])
