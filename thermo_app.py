import pandas as pd
import streamlit as st
from PIL import Image

# ===== CONFIG =====
st.set_page_config(page_title="Thermodynamic Tool")

logo_path = "deMlogo.png"
excel_path = "Thermodynamic_Database.xlsx"

# Custom CSS: background, text colors, input boxes, button style, logo positioning
st.markdown(
    f"""
    <style>
    /* Page background and text */
    [data-testid="stAppViewContainer"] {{
        background-color: white;
        color: black;
    }}

    /* Footer text */
    div[style*="text-align:center"] {{
        color: black !important;
        font-size: 18px;
    }}

    /* Inputs, selects, textareas: white background, black text */
    input, select, textarea {{
        background-color: white !important;
        color: black !important;
    }}

    /* Placeholder text */
    ::placeholder {{
        color: #555 !important;
    }}

    /* Style the "Get Properties" button */
    .stButton > button {{
        background-color: #ff69b4;  /* pink */
        color: white;
        border: none;
        padding: 8px 20px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #ff85c1;
    }}

    /* Top right logo container */
    .top-right-logo {{
        position: absolute;
        top: 10px;
        right: 10px;
        z-index: 9999;
        width: 300px;
    }}

    .top-right-logo img {{
        width: 100%;
        height: auto;
    }}
    </style>

    <div class="top-right-logo">
        <img src="{logo_path}" alt="Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Load and display logo (optional, you have the CSS logo already)
logo = Image.open(logo_path)
st.image(logo, width=300)

# Load Excel
