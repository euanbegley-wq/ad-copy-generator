import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Ad Copy Generator", page_icon="✍️")

# --- Logic to handle API Key ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    has_valid_key = True
else:
    st.sidebar.header("Configuration")
    api_key = st.sidebar.text_input("Enter Google API Key", type="password")
    has_valid_key = bool(api_key)

# --- Main App UI ---
st.title("✍️ Trust-Building Ad Copy Generator")
st.markdown("Generates professional ad copy using **Google Gemini**.")
st.divider()

col1, col2 = st.columns(2)
with col1:
    business_name = st.text_input("Business Name", placeholder="e.g., Apex Plumbing")
    years_exp = st.number_input("Years Experience", value=5)
    team_size = st.number_input("Team Size", value=1)

with col2:
    jobs_completed = st.number_input("Jobs Completed", value=100)
    pricing = st.selectbox("Pricing", ["Fixed Price", "Hourly", "No Hidden Fees"])
    availability = st.text_input("Availability", placeholder="e.g., Next day")

# --- FULL WIDTH INPUTS START HERE ---
locations = st.text_input("Locations Covered", placeholder="e.g. London, M25, Greater Manchester, and surrounding areas")
trust_signals = st.text_area("Trust Signals", placeholder="e.g., Insured by AXA, Gas Safe")
social_proof = st.text_input("Social Proof", placeholder="e.g., 500+ 5-star reviews")

if st.button("Generate Ad Description"):
    if not has_valid_key:
        st.error("No API Key found. Please configure secrets or enter a key.")
    elif not business_name:
        st.warning("Please enter a Business Name.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Write a trust-building ad description (max 500 words).
            Business: {business_name}, Exp: {years_exp} yrs, Team: {team_size}, Jobs: {jobs_completed}.
            Trust Signals: {trust_signals}. Pricing: {pricing}. 
            Availability: {availability}. Locations: {locations}. Social: {social_proof}.
            
            Guidelines:
            1. Intro: State experience/team/jobs.
            2. Eliminate Risk: Use trust signals. If Issuer (e.g. AXA) is listed, name them.
            3. Pricing: State clearly.
            4. Social Proof: Mention it.
            5. Logistics: State availability and explicitly mention that you serve {locations}.
            Output: Ad copy only.
            """
            
            with st.spinner('Generating...'):
                response = model.generate_content(prompt)
                st.subheader("Your Ad Copy:")
                st.text_area("Result", value=response.text, height=300)
        except Exception as e:
            st.error(f"Error: {e}")
