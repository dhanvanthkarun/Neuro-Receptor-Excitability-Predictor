# 🔬 Neuro-Receptor Excitability Predictor (NREP)

**Neuro-Receptor Excitability Predictor (NREP)** is an elite, open-source computational biology pipeline engineered to bridge the fundamental gap between structural bioinformatics and systemic computational neuroscience.

Built on the **TRIADS** framework (Bioinformatics, Neuroscience, AI), NREP serves as an autonomous research tool that automates the biophysical parsing of protein structures and leverages advanced Large Language Models (LLMs) to predict the downstream neuro-pharmacological impacts of structural variations.

### 🧬 What This Project Does
The Neuro-Receptor Excitability Predictor (NREP) transforms how researchers analyze the relationship between protein structure and neural circuit behavior. It performs the following operations:

1.  **Autonomous Structural Acquisition:** The pipeline automatically queries the RCSB Protein Data Bank or UniProt databases to fetch high-resolution crystal structures based on user identifiers.
2.  **Biophysical Metric Extraction:** Utilizing the `BioPython` engine, NREP parses raw PDB data to map internal protein geometry, including residue density, atomic counts, and conformational structural features.
3.  **AI-Driven Neuro-Pharmacological Inference:** The tool routes the extracted structural data to an intelligent AI backend. The AI acts as an expert computational neurobiologist to infer how specific mutations or binding dynamics will alter ion channel kinetics (e.g., NMDA or GABA_A receptor functionality) and subsequently impact local neural network firing rates.
4.  **Publication-Ready Automated Reporting:** NREP automatically compiles the analytical findings into professional, timestamped PDF reports, stored locally for immediate reference or dissemination in research environments.

### 🚀 Technical Implementation
NREP utilizes a modular architecture designed for local Ubuntu environments:
* **`app.py`**: A modern `Streamlit` dashboard providing a visual, interactive interface for real-time analysis and structural inquiry.
* **`core/pdb_fetcher.py`**: An automated network layer for secure PDB/UniProt data ingestion.
* **`core/structural_parser.py`**: A rigorous geometric calculation engine for structural data extraction.
* **`core/ai_engine.py`**: A multi-provider AI routing architecture, natively supporting **Anthropic (Claude 3.5 Haiku)** for primary scientific analysis and **OpenAI/OpenRouter** for sandbox development.
* **`core/exporter.py`**: An automated reporting utility for generating PDF-formatted scientific summaries.

---

### 💻 Installation & Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/dhanvanthkarun/NREP.git](https://github.com/dhanvanthkarun/NREP.git)
cd NREP
