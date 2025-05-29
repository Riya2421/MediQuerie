#import necessary modules
import streamlit as st
from pathlib import Path
import google.generativeai as genai
from api_key import api_key

# Configure the generative AI model
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    safety_settings=safety_settings
)

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your
expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:
1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analyses, note that certain aspects are "Unable to be determined based on the provided image."
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with these four headings: Detailed Analysis, Findings Report, Recommendations and Next Steps, Treatment Suggestions.
"""

text_prompt = """
You are a medical chatbot designed to provide users with general medical information and advice based on their text queries. Please respond to user questions with accurate and helpful information, while encouraging them to consult with a healthcare professional for definitive medical advice.
"""

# Set page configuration
st.set_page_config(page_title="MediQuerie", page_icon=":robot:")

# Set the logo
st.image("doc_logo.jpg", width=200)

# Set the title
st.title("MediQuerie : Expert Medical Guidance")
st.subheader("Your AI Companion for Compassionate Healthcare Advice")

# Image Analysis Section
st.header("Image Analysis")
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=300,caption="Uploaded Medical Image")
submit_button = st.button("Generate Image Analysis")

if submit_button:
    if uploaded_file is not None:
        image_data = uploaded_file.getvalue()
        
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": image_data
            },
        ]
        
        prompt_parts = [
            image_parts[0],
            system_prompt,
        ]

        st.title("Here is the analysis based on your image:")
        response = model.generate_content(prompt_parts)
        st.write(response.text)
    else:
        st.error("Please upload an image before submitting.")

# Text-to-Text Chatbot Section
st.header("Text-to-Text Chatbot")
user_input = st.text_area("Enter your medical question here:")
text_submit_button = st.button("Generate Response")

if text_submit_button:
    if user_input:
        text_prompt_parts = [
            user_input,
            text_prompt,
        ]
        
        text_response = model.generate_content(text_prompt_parts)
        st.title("Chatbot Response:")
        st.write(text_response.text)
    else:
        st.error("Please enter a question before submitting.")