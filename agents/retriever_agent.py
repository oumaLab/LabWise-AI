import os

class RetrieverAgent:
    def __init__(self, knowledge_base_path="data/medical_context.txt"):
        self.kb_path = knowledge_base_path
        self.context_data = self._load_data()

    def _load_data(self):
        """Loads the text data into memory."""
        try:
            if os.path.exists(self.kb_path):
                with open(self.kb_path, "r", encoding="utf-8") as f:
                    return f.read()
            else:
                # Fallback if running from a different relative path
                abs_path = os.path.join(os.getcwd(), self.kb_path)
                if os.path.exists(abs_path):
                     with open(abs_path, "r", encoding="utf-8") as f:
                        return f.read()
                return "No medical context found."
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
