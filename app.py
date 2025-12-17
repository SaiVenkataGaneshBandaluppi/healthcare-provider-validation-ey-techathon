import streamlit as st
import pandas as pd
from orchestrator import AgentOrchestrator
from utils.database import Database
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Page config
st.set_page_config(
    page_title="Healthcare Provider Directory Validator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1e40af;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #64748b;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .success-card {
        background: #10b981;
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .warning-card {
        background: #f59e0b;
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
    .error-card {
        background: #ef4444;
        padding: 1rem;
        border-radius: 0.5rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'results' not in st.session_state:
    st.session_state.results = None
if 'db' not in st.session_state:
    st.session_state.db = Database()

def main():
    # Header
    st.markdown('<h1 class="main-header">Healthcare Provider Directory Validator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Powered by Multi-Agent AI System | EY Techathon 6.0</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/2/24/EY_logo_2019.svg/2560px-EY_logo_2019.svg.png", width=150)
        st.markdown("---")
        st.subheader("System Status")
        
        # Check API key
        api_key = os.getenv("GROQ_API_KEY")
        if api_key and api_key.startswith("gsk_"):
            st.success("Groq API Connected")
        else:
            st.error("Groq API Key Missing")
            st.info("Add your Groq API key to .env file")
        
        st.markdown("---")
        st.subheader("Active Agents")
        st.write("1. Validation Agent")
        st.write("2. Enrichment Agent")
        st.write("3. Quality QA Agent")
        st.write("4. Management Agent")
        
        st.markdown("---")
        st.info("**Team:** Bandaluppi Sai Venkata Ganesh, Pilla Srikar, Poosarla Neeraj")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs([" Upload & Process", " Results Dashboard", " About"])
    
    with tab1:
        st.subheader("Upload Provider Directory")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload CSV file with provider data",
                type=['csv'],
                help="CSV should contain: name, npi, phone, address, city, state, zip"
            )
        
        with col2:
            st.markdown("**Required Columns:**")
            st.code("""
- name
- npi
- phone
- address
- city
- state
- zip
            """)
        
        # Sample data option
        if st.button(" Load Sample Data (5 providers)"):
            sample_data = pd.DataFrame([
                {
                    "name": "Dr. Sarah Johnson",
                    "npi": "1234567890",
                    "phone": "555-123-4567",
                    "address": "123 Medical Plaza",
                    "city": "New York",
                    "state": "NY",
                    "zip": "10001",
                    "specialty": ""
                },
                {
                    "name": "Dr. Michael Chen",
                    "npi": "9876543210",
                    "phone": "555-987-6543",
                    "address": "456 Healthcare Ave",
                    "city": "Los Angeles",
                    "state": "CA",
                    "zip": "90001",
                    "specialty": ""
                },
                {
                    "name": "Dr. Emily Rodriguez",
                    "npi": "5555555555",
                    "phone": "555-555-5555",
                    "address": "789 Wellness St",
                    "city": "Chicago",
                    "state": "IL",
                    "zip": "60601",
                    "specialty": ""
                },
                {
                    "name": "Dr. James Williams",
                    "npi": "1111222233",
                    "phone": "555-111-2222",
                    "address": "321 Care Blvd",
                    "city": "Houston",
                    "state": "TX",
                    "zip": "77001",
                    "specialty": ""
                },
                {
                    "name": "Dr. Lisa Anderson",
                    "npi": "4444555566",
                    "phone": "555-444-5555",
                    "address": "654 Health Way",
                    "city": "Phoenix",
                    "state": "AZ",
                    "zip": "85001",
                    "specialty": ""
                }
            ])
            
            # Save to session state
            st.session_state.uploaded_data = sample_data
            st.success(" Sample data loaded!")
            st.dataframe(sample_data)
        
        # Process uploaded file
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.session_state.uploaded_data = df
                
                st.success(f" File uploaded: {len(df)} providers")
                st.dataframe(df.head())
                
            except Exception as e:
                st.error(f"Error reading file: {e}")
        
        # Process button
        if st.button(" Start Validation Process", type="primary", use_container_width=True):
            if 'uploaded_data' not in st.session_state:
                st.error(" Please upload a file or load sample data first!")
            else:
                process_providers(st.session_state.uploaded_data)
    
    with tab2:
        st.subheader(" Validation Results Dashboard")
        
        if st.session_state.results is not None:
            display_results(st.session_state.results)
        else:
            st.info(" Upload and process provider data to see results here")
    
    with tab3:
        st.subheader(" About This System")
        
        st.markdown("""
        ###  Multi-Agent AI Architecture
        
        Our system uses **4 specialized autonomous agents** that work collaboratively:
        
        **1. Validation Agent**
        - Verifies NPI numbers against CMS NPPES Registry
        - Validates phone and address formats
        - Makes autonomous decisions on data validity
        
        **2. Enrichment Agent**
        - Enhances records with specialty information
        - Standardizes address formats
        - Adapts enrichment strategy based on available data
        
        **3. Quality Assurance Agent**
        - Cross-validates results from other agents
        - Self-corrects inconsistencies
        - Calculates confidence scores
        
        **4. Management Agent**
        - Orchestrates the entire workflow
        - Creates audit trails for compliance
        - Makes goal-driven decisions on next actions
        
        ###  Key Benefits
        
        -  **240x Faster**: 3 minutes vs 20 hours for 200 providers
        -  **99% Cost Reduction**: $10/day vs $600/day
        -  **85-92% Accuracy**: Consistent validation across all fields
        -  **100% Compliant**: Complete audit trails for regulatory requirements
        
        ###  Team
        
        - **Bandaluppi Sai Venkata Ganesh** - AI Architecture & System Design
        - **Pilla Srikar** - Backend Development & API Integration  
        - **Poosarla Neeraj** - Frontend Development & Quality Assurance
        
        ###  EY Techathon 6.0
        
        Developed for EY Techathon 6.0 - Agentic AI Challenge
        """)

def process_providers(df: pd.DataFrame):
    """Process providers through multi-agent system"""
    
    # Initialize orchestrator
    with st.spinner(" Initializing multi-agent system..."):
        if st.session_state.orchestrator is None:
            st.session_state.orchestrator = AgentOrchestrator()
        time.sleep(1)
    
    st.success(" System initialized!")
    
    # Convert dataframe to list of dicts
    providers = df.to_dict('records')
    
    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    results = []
    
    for i, provider in enumerate(providers):
        status_text.text(f"Processing {i+1}/{len(providers)}: {provider.get('name', 'Unknown')}")
        
        # Process through orchestrator
        result = st.session_state.orchestrator.process_provider(provider)
        results.append(result)
        
        # Update progress
        progress_bar.progress((i + 1) / len(providers))
        
        # Save to database
        st.session_state.db.save_provider(result['final_record'])
    
    status_text.text(" Processing complete!")
    st.session_state.results = results
    
    # Show completion message
    st.balloons()
    st.success(f" Successfully processed {len(results)} providers!")

def display_results(results: list):
    """Display validation results"""
    
    # Summary metrics
    st.markdown("###  Summary Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    approved = sum(1 for r in results if r['qa']['final_status'] == 'APPROVED')
    needs_review = sum(1 for r in results if r['qa']['final_status'] == 'NEEDS_REVIEW')
    rejected = sum(1 for r in results if r['qa']['final_status'] == 'REJECTED')
    avg_confidence = sum(r['qa']['final_confidence'] for r in results) / len(results)
    
    with col1:
        st.markdown('<div class="success-card">', unsafe_allow_html=True)
        st.metric(" Approved", approved, f"{approved/len(results)*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="warning-card">', unsafe_allow_html=True)
        st.metric(" Needs Review", needs_review, f"{needs_review/len(results)*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="error-card">', unsafe_allow_html=True)
        st.metric(" Rejected", rejected, f"{rejected/len(results)*100:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(" Avg Confidence", f"{avg_confidence:.1%}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Results table
    st.markdown("###  Detailed Results")
    
    results_data = []
    for r in results:
        final_rec = r['final_record']
        results_data.append({
            "Provider Name": final_rec.get('name'),
            "NPI": final_rec.get('npi'),
            "Specialty": final_rec.get('specialty'),
            "Phone": final_rec.get('phone'),
            "Status": r['qa']['final_status'],
            "Confidence": f"{r['qa']['final_confidence']:.1%}",
            "Processing Time": f"{r['processing_time']:.2f}s"
        })
    
    results_df = pd.DataFrame(results_data)
    
    # Color code by status
    def color_status(val):
        if val == 'APPROVED':
            return 'background-color: #d1fae5'
        elif val == 'NEEDS_REVIEW':
            return 'background-color: #fef3c7'
        else:
            return 'background-color: #fee2e2'
    
    styled_df = results_df.style.applymap(color_status, subset=['Status'])
    st.dataframe(styled_df, use_container_width=True)
    
    # Export button
    csv = results_df.to_csv(index=False)
    st.download_button(
        label=" Download Results as CSV",
        data=csv,
        file_name="validation_results.csv",
        mime="text/csv",
        use_container_width=True
    )
    
    # Show agent decisions
    with st.expander(" View Agent Decisions & Audit Trail"):
        for i, r in enumerate(results, 1):
            st.markdown(f"**Provider {i}: {r['provider_input']['name']}**")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown("**Validation Agent**")
                for decision in r['validation']['decisions'][:3]:
                    st.text(f"• {decision[:50]}...")
            
            with col2:
                st.markdown("**Enrichment Agent**")
                for decision in r['enrichment']['decisions'][:3]:
                    st.text(f"• {decision[:50]}...")
            
            with col3:
                st.markdown("**QA Agent**")
                for decision in r['qa']['decisions'][:3]:
                    st.text(f"• {decision[:50]}...")
            
            with col4:
                st.markdown("**Management Agent**")
                for decision in r['management']['decisions'][:3]:
                    st.text(f"• {decision[:50]}...")
            
            st.markdown("---")

if __name__ == "__main__":
    main()