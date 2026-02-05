# LabWise AI - Agentic RAG Medical Analysis Assistant 🧬

**"Empowering Patients with Knowledge"**

LabWise AI is an academic prototype designed to interpret laboratory results (starting with CBC: Complete Blood Count) and provide simplified explanations in Moroccan Darija/Arabic.

**⚠️ DISCLAIMER: This is NOT a diagnostic tool. It is for educational and awareness purposes only. Always consult a doctor.**

## 🎯 Social Vision
- **Reduce Anxiety**: Patients often panic when they see "High" or "Low" on their papers. We explain what it might mean calmly.
- **Micro-Learning**: Educate users about their health (Anemia, Infection signs) in their local language.
- **Orientation**: Guide users to seek professional medical help.

## 🏗️ Architecture (Agentic RAG)
The system uses a **Multi-Agent Architecture** with **Local RAG (Retrieval-Augmented Generation)**.

1.  **Abnormality Agent**: Analyzes numerical values (Hb, WBC, Platelets) against WHO standard ranges based on gender.
2.  **Retriever Agent**: Searches a local medical knowledge base (`medical_context.txt`) to find relevant clinical context for detected abnormalities.
3.  **Explanation Agent**: Synthesizes the findings into a user-friendly explanation in Moroccan Darija (simulated for prototype).
4.  **Report Agent**: compiles everything into a downloadable medical report.

## 🚀 How to Run

1.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run Application**:
    ```bash
    streamlit run app.py
    ```

3.  **Usage**:
    - Select Gender.
    - Enter Hemoglobin, WBC, and Platelet values.
    - Click **Analyze Results**.

## 📂 Project Structure
```
labo_oumaima/
├── app.py                  # Main Streamlit Dashboard
├── agents/                 # Intelligent Agents
│   ├── abnormality_agent.py
│   ├── retriever_agent.py
│   ├── explanation_agent.py
│   └── report_agent.py
├── data/
│   └── medical_context.txt # Local RAG Knowledge Base
└── requirements.txt
```

## 🔮 Future Roadmap
- [ ] Add Diabetes (Glucose, HbA1c) module.
- [ ] Integrate Real Open Source LLM (Llama 3 or Mistral) for dynamic text generation.
- [ ] Add Voice Output (Text-to-Speech) for accessibility.
