import chromadb
import pandas as pd
import uuid
import json

class Portfolio:
    def __init__(self, file_path="resource/clean_fixed.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(self.file_path)

        self.chroma_client = chromadb.PersistentClient(path="vectorstore")
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def _to_string(self, value):
        """Convert dict or other types to a clean string."""
        if isinstance(value, dict):
            required_skills = ", ".join(value.get("required", {}).keys())
            desired_skills = value.get("desired", "")
            return f"Required: {required_skills}. Desired: {desired_skills}"
        return str(value)

    def load_portfolio(self):
        if not self.collection.count():
            for _, row in self.data.iterrows():
                techstack_str = self._to_string(row["Techstack"])
                link_str = str(row["Links"]).strip()

                if techstack_str.strip():
                    self.collection.add(
                        documents=[techstack_str],
                        metadatas=[{"links": link_str}],
                        ids=[str(uuid.uuid4())]
                    )

    def query_links(self, skills):
        # Ensure skills are strings
        if isinstance(skills, dict):
            skills = [self._to_string(skills)]
        elif not isinstance(skills, list):
            skills = [str(skills)]

        results = self.collection.query(
            query_texts=skills,
            n_results=2,
            include=["metadatas", "documents", "distances"]
        )

        return [
            m["links"]
            for meta_list in results.get("metadatas", [])
            for m in meta_list
            if "links" in m
        ]
