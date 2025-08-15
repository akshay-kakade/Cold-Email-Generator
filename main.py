import chromadb
import pandas as pd
import uuid
import os

class Portfolio:
    def __init__(self, file_path="resource/clean_fixed.csv"):
        self.file_path = file_path
        os.makedirs(".chromadb", exist_ok=True)  # Writable folder for Streamlit Cloud
        self.data = pd.read_csv(self.file_path)
        self.chroma_client = chromadb.PersistentClient(path=".chromadb")
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
