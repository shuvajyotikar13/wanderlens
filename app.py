import streamlit as st
from src.orchestrator import AgenticOrchestrator
from datetime import datetime, timedelta

st.set_page_config(page_title="WanderLens", layout="centered")

st.title("📸 WanderLens: Pixels to Pathways")
st.markdown("Upload a photo of a landmark, and let our Agentic AI build your itinerary.")

# Initialize the orchestrator (cached to prevent reloading)
@st.cache_resource
def get_orchestrator():
    return AgenticOrchestrator()

orchestrator = get_orchestrator()

with st.sidebar:
    st.header("Travel Preferences")
    user_location = st.text_input("Current City", value="Bangalore, India")
    user_iata = st.text_input("Nearest Airport IATA", value="BLR")
    travel_date = st.date_input("Planned Travel Date", min_value=datetime.today() + timedelta(days=7))

uploaded_file = st.file_uploader("Upload Landmark Photo", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    
    if st.button("Generate Itinerary"):
        with st.spinner("Analyzing image and consulting travel APIs..."):
            try:
                image_bytes = uploaded_file.getvalue()
                formatted_date = travel_date.strftime("%Y-%m-%d")
                
                # Trigger the Agentic Flow
                itinerary = orchestrator.process_request(
                    image_bytes=image_bytes,
                    user_location=user_location,
                    user_iata=user_iata,
                    travel_date=formatted_date
                )
                
                st.success("Itinerary Generated!")
                st.markdown("### Your Custom Travel Plan")
                st.write(itinerary)
                
            except Exception as e:
                st.error(f"An error occurred during processing: {str(e)}")
