import os

class RetrieverAgent:
    def __init__(self, knowledge_base_path="data/medical_context.txt"):
        self.kb_path = knowledge_base_path
        self.context_data = self._load_data()

    def _load_data(self):
        """Loads the text data into memory."""
        try:
            # Robust path finding for Streamlit Cloud
            # Assuming structure: /app/agents/retriever_agent.py and /app/data/medical_context.txt
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_path = os.path.join(base_dir, self.kb_path)
            
            if os.path.exists(data_path):
                with open(data_path, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                return f"Error: Medical context file not found at {data_path}"
        except Exception as e:
            return f"Error loading context: {str(e)}"

    def retrieve(self, query_keywords):
        """
        Simple keyword-based retrieval.
        Returns the relevant section from the context file.
        """
        # In a real RAG system, this would use embeddings (ChromaDB/FAISS).
        # For this prototype, we extract sections based on headers.
        
        relevant_context = []
        content_lower = self.context_data.lower()
        
        # Simple extraction logic
        if "hb" in query_keywords or "hemoglobin" in query_keywords or "anemia" in query_keywords:
            start = self.context_data.find("[HEMOGLOBIN]")
            end = self.context_data.find("[WBC - White Blood Cells]")
            if start != -1:
                chunk = self.context_data[start:end].strip()
                relevant_context.append(chunk)

        if "wbc" in query_keywords or "leukocytes" in query_keywords or "infection" in query_keywords:
            start = self.context_data.find("[WBC - White Blood Cells]")
            end = self.context_data.find("[PLATELETS]")
            if start != -1:
                chunk = self.context_data[start:end].strip()
                relevant_context.append(chunk)

        if "platelets" in query_keywords or "thrombocytes" in query_keywords:
            start = self.context_data.find("[PLATELETS]")
            end = self.context_data.find("[GENERAL ADVICE]")
            if start != -1:
                chunk = self.context_data[start:end].strip()
                relevant_context.append(chunk)
        
        if not relevant_context:
            return "No specific context found for the abnormalities."
        
        return "\n\n".join(relevant_context)
