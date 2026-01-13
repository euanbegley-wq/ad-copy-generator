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
st.title("✍️ Services Trust-Building Ad Copy Generator")
st.markdown("Generates professional ad copy using **Google Gemini**.")
st.divider()

# --- CATEGORY DATA ---
categories = sorted([
    "Academic", "Accessories", "Accountants", "Accounting", "Acupuncture", 
    "Advertising Agencies", "Airconditioning & Heating", "Alternative Therapies", 
    "Appliance Repair", "Architect", "Aromatherapy", "Arts & Crafts", 
    "Asbestos Removal", "Astrology & Psychics", "Au pairs", "Baby Classes & Groups", 
    "Babysitting", "Bakery", "Bands & Musicians", "Barbers Shops", "Bars & Pubs", 
    "Bathroom Fitters", "Beauty Treatments", "Bedroom Fitters", "Bike Shops", 
    "Blacksmiths", "Body Repair", "Bookkeeping", "Bricklayers", "Builders", 
    "Bus & Coach", "Business", "Cafes", "Cake Makers", "Car Breakers", 
    "Car Servicing & Repair", "Car Valeting", "Car Wash", "Caravan Hire", 
    "Carpentry & Joiners", "Carpet Cleaning", "Carpet Fitters", "Cars & Transportation", 
    "Catering", "Catering & Services", "Central Heating", "Chauffeur & Limousine Hire", 
    "Cheap Loans", "Childcare Agencies", "Childminders", "Children's Activities", 
    "Chimney Sweeps", "Chinese", "Chiropodists & Podiatrists", "Clarinet Tuition", 
    "Clothes Stores", "Coach Hire", "Commercial & Office Cleaning", 
    "Commercial Property Agents", "Complementary Therapies", "Computer Network", 
    "Computer Repair", "Computer Services", "Computer Support", "Construction", 
    "Cookery Classes", "Copywriting", "Counselling", "Courier Services", 
    "Creative Writing", "Curtain & Upholstery Cleaning", "Czech", "DJ & Disco Hire", 
    "Damp Proofing", "Dance Classes", "Dating", "Deep Tissue Massage", "Dentists", 
    "Doctors & Clinics", "Domestic Cleaning", "Door", "Drain & Pipe Cleaning", 
    "Drama Schools", "Dress & Suit Hire", "Driving Lessons & Instructors", 
    "Drum Tuition", "Dry Cleaning & Laundry", "Dutch", "Electrical", "Electricians", 
    "Embroidery", "English", "Entertainers", "Entrance exams", "Estate Agents", 
    "Europe", "Event", "External cleaning", "Eye Treatments", "Facials", 
    "Fashion Designers", "Fencing Contractors", "Financial Advice", 
    "Flatpack Furniture Assemblers", "Floor Tilers", "Florists", "Footwear", 
    "French", "Function Rooms & Banqueting Facilities", "Funeral Directors", 
    "Garage & Mechanic Services", "Garage Doors", "Gardening & Landscaping", 
    "General Office Services", "German", "Glaziers", "Goods Suppliers & Retailers", 
    "Grooming", "Groundworkers", "Guitar Tuition", "Gutter Cleaning", 
    "Gutter install & repair", "Hair Extensions & Wig Services", "Hairdressers", 
    "Hairdressing", "Handymen", "Health & Fitness", "Health & Safety", 
    "Health Clubs & Fitness Centers", "Health Products", "Hen & Stag Planners", 
    "Homeopathy", "Honeymoons", "Hostel & Hotels", "Housekeepers", "Hypnotherapy", 
    "IT & Computing", "Insolvency Practitioners", "Insulation", "Insurance", 
    "Interior Designers", "Interpreting & Translation", "Italian", "Japanese", 
    "Jewellers", "Kitchen Fitters", "Laminate Fitters", "Language", 
    "Leaflet Distribution", "Legal Services", "Letting Agents", "Life Coaching", 
    "Lighting Specialists", "Locksmiths", "Loft Conversion Specialists", 
    "MOT Testing", "Make Up Artists", "Marquee Hire", "Market Research", 
    "Marketing", "Martial Arts Clubs & Schools", "Maths", "Mobile Beauty Therapists", 
    "Mobile Hairdressers", "Mobile Phone", "Models & Actors", "Money Transfer", 
    "Mortgage Brokers", "Motoring", "Music", "Nail Services/Technicians/Manicures", 
    "Nannies", "Nursery Schools", "Nursing & Care", "Office Furniture", 
    "Online Content Providers", "Opticians", "Organisers & Planners", 
    "Other Accountanting", "Other Alternative Therapies", "Other Beauty Treatments", 
    "Other Business & Office Services", "Other Children Services", "Other Classes", 
    "Other Cleaning", "Other Computer Services", "Other Entertainment Services", 
    "Other Fitness Services", "Other Flooring", "Other Food & Drink", 
    "Other Goods Suppliers & Retailers", "Other Health & Beauty Services", 
    "Other Language Lessons", "Other Massage Therapies", "Other Motoring Services", 
    "Other Music Tuition", "Other Pet Services", "Other Property & Maintenance Services", 
    "Other Wedding Services", "Overseas Business", "Overseas Property", 
    "Overseas Removals", "Painting & Decorating", "Parent Support", 
    "Paving & Driveway", "Payroll", "Pedicures", "Personal Trainers", 
    "Pest & Vermin Control", "Petsitters & Dogwalkers", "Phone & Tablet Repair", 
    "Photographers & Videographers", "Photography & Film", "Physics", 
    "Piano Tuition", "Pilates Courses", "Plasterers", "Plumbing", "Polish", 
    "Pregnancy & Child Birth", "Printing", "Proof Reading", "Property", 
    "Property Consultants", "Property Maintenance Services", "Psychotherapy", 
    "Recruitment", "Reflexology", "Reiki Healing", "Removal Services", 
    "Rest of World", "Restaurants", "Roofing", "Russian", "Satellite, Aerial & TV", 
    "Saxophone Tuition", "Scaffolding", "Science", "Seamstress/Tailors", 
    "Secretarial Services", "Security Services", "Self Defence", "Shiatsu Massage", 
    "Shipping", "Shopfitters", "Shredding Services", "Sign Makers", 
    "Singing Lessons", "Skip Hire", "Sofa", "Software Application Development", 
    "Solicitors & Conveyancing", "Spanish", "Speech Writing", "Sports Massage", 
    "Stonemasons", "Storage", "Structural Engineers", "Stylists", "Supermarkets", 
    "Supplies", "Surveyors", "Swedish Massage", "TV Repairs", "Takeaways", 
    "Tanning", "Tattooing & Piercing", "Tax", "Taxi", 
    "Telecom & Internet Service Providers", "Thai Massage", "Tilers", "Training", 
    "Travel Agents", "Tree Surgeons", "Tyre Fitting", "UK & Ireland", "Upholsterers", 
    "Van & Truck Hire", "Vehicle Hire", "Vehicle Recovery Services", 
    "Venues & Nightclubs", "Vets", "Violin Tuition", "Visa & Immigration", 
    "Waxing Treatments", "Web Development", "Web Services", "Website Design", 
    "Wedding & Reception Venues", "Weddings", "Weddings Abroad", "Wholesale", 
    "Window Blinds, Shutters & Curtains", "Window Cleaning", "Windows & Doors", 
    "Windshield Repair", "Wood Flooring", "Writing & Literature", "Yoga Classes", 
    "Yoga Therapy"
])

col1, col2 = st.columns(2)

# --- LEFT COLUMN ---
with col1:
    business_name = st.text_input(
        "Business Name", 
        placeholder="Limited Company Name, Brand Name if Sole Trader, or their Name if they are a freelancer/individual."
    )
    
    # Nested columns for Category and Team Size
    cat_col, team_col = st.columns(2)
    with cat_col:
        category = st.selectbox("Category", options=categories)
    with team_col:
        team_size = st.number_input("Team Size", value=1)
        
    years_exp = st.number_input("Years Experience", value=5)

# --- RIGHT COLUMN ---
with col2:
    jobs_completed = st.number_input("Jobs Completed", value=100)
    
    # Nested columns for Pricing
    pricing_col1, pricing_col2 = st.columns(2)
    with pricing_col1:
        pricing_options = [
            "Fixed Price", "Hourly Rate", "Daily Rate", "Price per Unit/Item", 
            "Free Quote", "No Hidden Fees", "No Call-Out Charge", "All-Inclusive"
        ]
        pricing_model = st.selectbox("Pricing Model", pricing_options)
        
    with pricing_col2:
        pricing_amount = st.text_input("Pricing Amount / Detail", placeholder="e.g. £50/hr")

    availability = st.text_input("Availability", placeholder="e.g., Next day")

# --- FULL WIDTH INPUTS ---
locations = st.text_input("Locations Covered", placeholder="e.g. London, M25, Greater Manchester, and surrounding areas")

trust_signals = st.text_area(
    "Trust Signals", 
    placeholder="e.g., Insurance (e.g., Public Liability), Certificates (e.g., Gas Safe, DBS Checked), Awards (e.g., Houzz Best of Service, Trustpilot 5-Star)"
)

social_proof = st.text_input("Social Proof", placeholder="e.g., 500+ 5-star reviews")

portfolio_link = st.text_input("External Portfolio Link", placeholder="e.g. www.yourwebsite.com/portfolio or Behance link")

if st.button("Generate Ad Description"):
    if not has_valid_key:
        st.error("No API Key found. Please configure secrets or enter a key.")
    elif not business_name:
        st.warning("Please enter a Business Name.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            # --- PROMPT ---
            prompt = f"""
            System Role:
            You are a human copywriter. You write in a genuine, trustworthy tone, but you strictly follow the provided data hierarchy.
            
            Input Data:
            - Business Name: {business_name}
            - Category: {category}
            - Experience: {years_exp} years
            - Team Size: {team_size}
            - Jobs Completed: {jobs_completed}
            - Trust Signals: {trust_signals}
            - Social Proof: {social_proof}
            - Availability: {availability}
            - Locations: {locations}
            - Portfolio Link: {portfolio_link}
            - Pricing Model: {pricing_model}
            - Pricing Cost: {pricing_amount}

            HIERARCHY & LOGIC RULES:
            1. **CATEGORY IS KING:** The 'Category' field ({category}) is the ABSOLUTE TRUTH. If the Business Name contradicts the Category, ignore the name's implications.
            2. **CRITICAL FACTUAL ACCURACY:** Do not generalize trust signals. Use exact terms provided (e.g. if "DBS Checked", use "DBS Checked", NOT "Fully Insured").
            3. **HONEST PRICING:** Quote pricing exactly as provided.

            TASK:
            Generate two distinct parts: 3 Headline Options and 1 Ad Description.

            PART 1: HEADLINE OPTIONS (The "Golden Rule")
            Generate 3 distinct headlines based on the format: "[Business/Category] - [Key Hook]"
            
            1. **Option 1 (The Trust Hook):** Use the strongest Trust Signal provided (e.g. "Gas Safe").
            2. **Option 2 (The Speed/Logistics Hook):** Use Availability or Location (e.g. "Same Day Service" or "Serving London").
            3. **Option 3 (The Authority Hook):** Use Experience or Job Count (e.g. "100+ Jobs Completed" or "5 Years Exp").
            
            *Constraint:* If a specific data point is missing for an option, fallback to the Category Name.

            PART 2: THE DESCRIPTION (300-400 words)
            Style: No fluff, conversational, use contractions, mix sentence lengths.
            Structure: Hook -> Trust -> Proof -> Logistics -> CTA.

            Output Format:
            Headlines:
            1. [Option 1]
            2. [Option 2]
            3. [Option 3]
            
            Description:
            [Insert Description Here]
            """
            
            with st.spinner('Generating...'):
                response = model.generate_content(prompt)
                
                # --- PARSE THE OUTPUT ---
                full_text = response.text.replace("**", "").replace("## ", "")
                
                headlines = "Option 1..."
                description = full_text
                
                if "Headlines:" in full_text and "Description:" in full_text:
                    parts = full_text.split("Description:")
                    headlines_part = parts[0].replace("Headlines:", "").strip()
                    description_part = parts[1].strip()
                    headlines = headlines_part
                    description = description_part
                
                # --- DISPLAY RESULTS ---
                st.subheader("Headline Options (Pick one):")
                st.text_area("Headlines", value=headlines, height=100)
                
                st.subheader("Your Ad Body:")
                st.text_area("Body", value=description, height=400)
                
        except Exception as e:
            st.error(f"Error: {e}")
