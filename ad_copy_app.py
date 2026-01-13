import streamlit as st
from openai import OpenAI

# Page Configuration
st.set_page_config(page_title="Trust-Building Ad Copy Generator", page_icon="✍️")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        background-color: #0066cc;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar for API Key ---
st.sidebar.header("Configuration")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# --- Main Interface ---
st.title("✍️ Trust-Building Ad Copy Generator")
st.markdown("Generates a professional description that eliminates customer risk and validates competence.")

st.divider()

col1, col2 = st.columns(2)

with col1:
    business_name = st.text_input("Business / Freelancer Name", placeholder="e.g., Apex Plumbing Solutions")
    years_exp = st.number_input("Years of Experience", min_value=0, step=1, value=5)
    team_size = st.number_input("Team Size", min_value=1, step=1, value=1)

with col2:
    jobs_completed = st.number_input("Jobs Completed", min_value=0, step=1, value=100)
    pricing_structure = st.selectbox("Pricing Structure", 
        ["Fixed Price (Quote)", "Hourly Rate", "No Hidden Fees", "Retainer", "Custom"])
    availability = st.text_input("Availability", placeholder="e.g., Next day availability, 24/7 Emergency")

st.markdown("### 🛡️ Trust & Proof")
trust_signals = st.text_area("Trust Signals (Certificates, Insurance, Awards)", 
    placeholder="e.g., Fully Insured by AXA ($5m coverage), Gas Safe Registered, Master Builder Award 2023")
social_proof = st.text_input("Social Proof / Portfolio", placeholder="e.g., Portfolio available on request, 500+ 5-star reviews on Google")

# --- Logic Generation ---
if st.button("Generate Ad Description"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar to proceed.")
    elif not business_name:
        st.warning("Please enter a Business Name.")
    else:
        client = OpenAI(api_key=api_key)
        
        # Constructing the Prompt based on your specific requirements
        prompt_text = f"""
        You are an expert ad copywriter. Your goal is to write a trust-building ad description that eliminates customer risk and validates competence.

        Input Data:
        Business/Name: {business_name}
        Years of Experience: {years_exp}
        Team Size: {team_size}
        Jobs Completed: {jobs_completed}
        Trust Signals: {trust_signals}
        Pricing Structure: {pricing_structure}
        Availability: {availability}
        Social Proof: {social_proof}

        Writing Guidelines: 
        Write a good, 500 words max description that includes the following five elements in a professional tone, with perfect grammar:
        
        1. The Intro: Start by introducing the business/person, explicitly mentioning years of experience, team size, and number of jobs completed to establish identity and competence.
        2. Eliminate Risk & Validate Competence: Use the provided Trust Signals to address the customer's fear. If the signal is safety-related (e.g., Insurance, DBS), position it to reduce risk. If the signal is quality-related (e.g., Degrees, Awards), position it to prove quality. CRUCIAL: If a Verifier/Issuer is provided in the input (e.g., "Insured by AXA"), you MUST explicitly name them in the text to increase credibility.
        3. Pricing Transparency: State the Pricing Structure clearly to create predictability.
        4. Social Proof: Mention the Social Proof (reviews/portfolio) if provided.
        5. Logistics: State the Availability to address deadlines.

        Output: Please output only the final Description. Do not include labels like "Intro:" or "Logistics:". Just the ad copy.
        """

        with st.spinner('Drafting your copy...'):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo", # You can switch to gpt-4 for higher quality
                    messages=[
                        {"role": "system", "content": "You are a professional copywriter specialized in high-trust service industries."},
                        {"role": "user", "content": prompt_text}
                    ],
                    temperature=0.7
                )
                
                generated_copy = response.choices[0].message.content
                
                # Output Display
                st.success("Description Generated!")
                st.markdown("### Your Ad Copy:")
                st.text_area("Copy to clipboard", value=generated_copy, height=300)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")