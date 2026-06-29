import os
import streamlit as st
from core.pdb_fetcher import PDBFetcher
from core.structural_parser import StructuralParser
from core.ai_engine import NeuroAIEngine
from core.exporter import ReportExporter

# Set up production page styling configurations
st.set_page_config(
    page_title="NREP Dashboard",
    page_icon="🔬",
    layout="wide"
)

# Initialize backend classes within the dashboard session
@st.cache_resource
def init_backend():
    return PDBFetcher(), StructuralParser()

fetcher, parser = init_backend()

# Title and Layout Header
st.title("🔬 Neuro-Receptor Excitability Predictor (NREP)")
st.caption("An Open-Source TRIADS Framework for Structural Bioinformatics & Computational Neuroscience")
st.markdown("---")

# Sidebar Configuration Layout
st.sidebar.header("🛠️ Engine Configurations")

# 1. AI Provider Selection Toggle
ai_provider = st.sidebar.selectbox(
    "Select Target AI Brain:",
    ["Claude (Flagship)", "OpenAI / OpenRouter (Sandbox)"],
    index=1  # Defaulting to OpenAI/OpenRouter sandbox for active system testing
)
provider_key = "claude" if "Claude" in ai_provider else "openai"

# 2. Ingestion Framework Toggle
ingestion_mode = st.sidebar.radio(
    "Data Ingestion Method:",
    ["Automated database Fetch", "Manual Local PDB Upload"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Repository Status:** Local Active Sandbox")

# Main Dashboard Workspace
col_input, col_results = st.columns([1, 2])

# Initializing a structural tracking state variable across reloads
if "extracted_metrics" not in st.session_state:
    st.session_state.extracted_metrics = None
if "active_filepath" not in st.session_state:
    st.session_state.active_filepath = None

with col_input:
    st.subheader("📥 Data Input Workspace")
    
    # Mode A: Database Automated Query
    if ingestion_mode == "Automated database Fetch":
        id_type = st.selectbox("Identifier Target Type:", ["RCSB PDB ID", "UniProt ID"])
        user_id = st.text_input("Enter Structural Identifier (e.g., 1AIE or P00533):", "").strip()
        
        if st.button("Fetch & Map Structure", use_container_width=True):
            if not user_id:
                st.error("Please provide a valid structural identifier text string.")
            else:
                with st.spinner("Executing network fetch protocols..."):
                    try:
                        if id_type == "RCSB PDB ID":
                            filepath = fetcher.fetch_by_pdb_id(user_id)
                        else:
                            filepath = fetcher.fetch_by_uniprot_id(user_id)
                            
                        # Parse the downloaded file instantly
                        metrics = parser.extract_metrics(filepath)
                        st.session_state.extracted_metrics = metrics
                        st.session_state.active_filepath = filepath
                        st.success(f"Successfully localized file: {filepath}")
                    except Exception as e:
                        st.error(f"Ingestion Sequence Interrupted: {e}")
                        
    # Mode B: Manual Local Desktop Upload
    else:
        uploaded_file = st.file_uploader("Drag & Drop Targeted Protein Crystal Structure File (.pdb)", type=["pdb"])
        if uploaded_file is not None:
            # Secure file to local development cache folder structure
            save_path = os.path.join("data/cache", uploaded_file.name)
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                
            if st.button("Process Uploaded File", use_container_width=True):
                with st.spinner("Parsing localized geometric constraints..."):
                    try:
                        metrics = parser.extract_metrics(save_path)
                        st.session_state.extracted_metrics = metrics
                        st.session_state.active_filepath = save_path
                        st.success("File processed successfully.")
                    except Exception as e:
                        st.error(f"Parsing Sequence Interrupted: {e}")

    # Section for Custom AI Engineering Inquiries
    st.markdown("---")
    st.subheader("🤖 Live Structural Inquiry")
    user_query = st.text_area(
        "Direct specific residue questions or mutation vectors to the model here:",
        value="Analyze how this specific structural density might influence downstream ion channel kinetics and network firing thresholds."
    )

with col_results:
    st.subheader("📊 Output Analytics Console")
    
    if st.session_state.extracted_metrics:
        m = st.session_state.extracted_metrics
        
        # Displaying structural summary parameters dynamically using Streamlit metric blocks
        st.markdown(f"### Current Structural Profile: **{m['protein_id']}**")
        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Total Chains", len(m['chains']))
        metric_col2.metric("Total Residues", m['total_residues'])
        metric_col3.metric("Total Active Atoms", m['total_atoms'])
        
        # Visual interactive table overview of individual peptide sequences mapped
        st.dataframe(m['chains'], use_container_width=True)
        
        # Execution Trigger Button for AI Reporting Pipeline
        if st.button(f"🚀 Execute Circuit Analysis via {provider_key.upper()} Engine", use_container_width=True):
            with st.spinner(f"Routing metadata payloads securely to {provider_key.upper()} clusters..."):
                try:
                    # Dynamically initialize and call selected core engine configuration
                    engine = NeuroAIEngine(provider=provider_key)
                    report_content = engine.generate_excitability_report(m, query=user_query)
                    
                    # --- NEW EXPORT LOGIC ---
                    exporter = ReportExporter()
                    saved_filepath = exporter.generate_pdf_report(m['protein_id'], report_content)
                    
                    st.markdown("### 🔬 Computed Neuro-Excitability Assessment")
                    st.info(report_content)
                    
                    # Notify user of successful local save and provide download button
                    st.success(f"📄 PDF Report securely saved to your local folder: `{saved_filepath}`")
                    
                    with open(saved_filepath, "rb") as pdf_file:
                        st.download_button(
                            label="📥 Download PDF Copy",
                            data=pdf_file,
                            file_name=os.path.basename(saved_filepath),
                            mime="application/pdf",
                            use_container_width=True
                        )
                    # ------------------------
                        
                except Exception as e:
                    st.error(f"Analytical Engine Runtime Halted: {e}")
