import streamlit as st
from pathlib import Path
from PIL import Image
import google.generativeai as genai
import time

# --- Configuration ---
# It's better to use st.secrets for API keys in deployed apps
# For local development, this is okay.
try:
    from api_key import api_key
    genai.configure(api_key=api_key)
except ImportError:
    st.error("API key not found. Please create an api_key.py file with your key.")
    st.stop()


# Model Generation Configuration
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# Safety Settings
safety_ratings = [
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# System Prompt
system_prompts = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your
expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images, based on the user's query.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze the image in the context of the user's query, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease that are relevant to the user's question. Clearly articulate these findings.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image and query pertain to human health issues.
2. Clarity of image: In cases where the image quality impedes clear analyses, note that certain aspects are "Unable to be determined based on the
provided image."
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

Please provide me an output response with these four headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.
"""

# Model Configuration - Updated to a more recent, stable model name
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # Using gemini-1.5-flash which is a fast and capable model
    generation_config=generation_config,
    safety_settings=safety_ratings
)

# --- Streamlit App UI ---

# Set the page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# Set the logo and title
# st.image("logo.jpeg", width=150) # You can uncomment this if you have a logo.jpeg file
st.title("👩🏻‍⚕️ Vital❤️Image📷Analytics📊🩺")
st.subheader("Upload a medical image and ask a question to get AI-driven insights.")

# File uploader
uploaded_file = st.file_uploader("1. Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

# Text input for user's query
user_query = st.text_area("2. Enter your question or describe your symptoms here:")

# Display uploaded image
if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Medical Image")

# Submit button
submit_button = st.button("Generate the Analysis")

# --- Logic on Button Click ---

if submit_button:
    # Check if both a file was uploaded and text was entered
    if uploaded_file is not None and user_query:
        # Show a spinner while processing
        with st.spinner("Generating analysis... Please wait."):
            try:
                # Prepare the image for the API
                image_data = uploaded_file.getvalue()
                image_parts = [{"mime_type": uploaded_file.type, "data": image_data}]

                # Prepare the final multimodal prompt
                prompt_parts = [
                    system_prompts,
                    image_parts[0],
                    f"Here is the user's query: {user_query}"
                ]

                # Generate a response
                response = model.generate_content(prompt_parts)

                # Display the analysis
                st.title("Here is the analysis based on your image and query:")
                st.markdown(response.text) # Using st.markdown for better formatting

            except Exception as e:
                # Handle potential errors, including the rate limit error
                st.error(f"An error occurred: {e}")
                st.info("This might be due to API rate limits. Please wait a moment and try again.")
    else:
        # Provide a warning if inputs are missing
        st.warning("Please upload an image AND enter a question before generating the analysis.")
