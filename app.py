import streamlit as st
from utils.file_extractor import extract_text_from_file
import google.generativeai as genai
from config.api_key_path import API_KEY_PATH
import os

# Load Gemini model with path-based API key
with open(API_KEY_PATH, "r") as f:
    api_key = f.read().strip()

genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="models/gemini-2.0-flash")

st.set_page_config(page_title="MedAnalyzer", layout="wide", page_icon="🧬")

st.title("MedAnalyzer")
st.markdown("Upload a **Medical Report** in `.pdf`, `.txt`, `.docx`, or image format (`.jpg`, `.png`, etc.) to analyze its content using Gemini.")

uploaded_file = st.file_uploader("Choose a Medical Report", type=["pdf", "txt", "docx", "png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("Extracting and Analyzing..."):
        try:
            text = extract_text_from_file(uploaded_file)
            prompt = f"""You are a medical expert AI. Analyze the following medical report thoroughly. Identify and explain:

                        1. Patient information
                        2. Symptoms and history
                        3. Diagnoses
                        4. Tests and their results
                        5. Treatment plan
                        6. Medications prescribed
                        7. Any follow-up instructions or concerns

                        Report content:\n\n{text}"""
            response = model.generate_content(prompt)
            st.success("Analysis Complete!")
            st.markdown("### 📋 Medical Report Summary")
            st.write(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
