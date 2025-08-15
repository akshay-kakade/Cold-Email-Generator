# portfolio.py
import os
import uuid
import pandas as pd
import chromadb
import streamlit as st
from chromadb.utils import embedding_functions

class Portfolio:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name="portfolio",
            embedding_function=embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        )
        self.data = None

    def load_portfolio(self):
        csv_path = os.path.join("resource", "clean_fixed.csv")
        if not os.path.exists(csv_path):
            st.error(f"CSV file not found: {csv_path}")
            return

        self.data = pd.read_csv(csv_path)

        if self.collection.count() == 0:
            for _, row in self.data.iterrows():
                techstack = str(row.get("Techstack", "")).strip()
                link = str(row.get("Links", "")).strip()
                if techstack:
                    self.collection.add(
                        documents=[techstack],
                        metadatas=[{"links": link}],
                        ids=[str(uuid.uuid4())]
                    )
            st.write(f"✅ Loaded {self.collection.count()} documents into Chroma.")

    def query_links(self, skills):
        if not skills:
            st.error("No skills provided for query.")
            return []

        if self.collection.count() == 0:
            st.error("Portfolio collection is empty. Load data first.")
            return []

        results = self.collection.query(
            query_texts=skills,
            n_results=5
        )

        return [meta["links"] for meta in results.get("metadatas", [[]])[0] if "links" in meta]
