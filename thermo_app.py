import pandas as pd
import streamlit as st
from PIL import Image

# ===== CONFIG =====
st.set_page_config(page_title="Thermodynamic Tool")

# ===== LOGO (Top Right) =====
logo_path = "deMlogo.png"
excel_path = "Thermodynamic_Database.xlsx"

# Custom CSS for styling
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

    /* Input boxes - keep white background and black text */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    textarea {{
        background-color: white !important;
        color: white !important;
    }}

    /* Placeholder text color */
    ::placeholder {{
        color: white !important;
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

# Load and display logo also (optional, but you have it)
logo = Image.open(logo_path)
st.image(logo, width=300)  # You can keep or remove this line if CSS logo is enough

# Load Excel data
sat_temp_df = pd.read_excel(excel_path, sheet_name="B1.1-Satd.Water")
sat_press_df = pd.read_excel(excel_path, sheet_name="B1.2-Satd.WaterPressEntry")
superheat_df = pd.read_excel(excel_path, sheet_name="B1.3-SuperheatedVapor")

# Interpolation helper function
def interpolate(df, key, value, outputs):
    df_sorted = df.sort_values(by=key).reset_index(drop=True)
    if value in df_sorted[key].values:
        return df_sorted[df_sorted[key] == value][outputs].iloc[0].to_dict()
    lower = df_sorted[df_sorted[key] <= value].iloc[-1]
    upper = df_sorted[df_sorted[key] >= value].iloc[0]
    frac = (value - lower[key]) / (upper[key] - lower[key])
    return {col: lower[col] + frac * (upper[col] - lower[col]) for col in outputs}

# App title
st.title("Thermodynamic Tool")

# Choose mode
mode = st.selectbox(
    "Choose the mode:",
    ["Saturated Water (by Temperature)", "Saturated Water (by Pressure)", "Superheated Vapor"]
)

if mode == "Saturated Water (by Temperature)":
    T = st.number_input("Enter Temperature (°C)", min_value=float(sat_temp_df["T"].min()), 
                        max_value=float(sat_temp_df["T"].max()))
    outputs = ["P", "v_f", "v_fg", "v_g", "u_f", "u_fg", "u_g", "h_f", "h_fg", "h_g", "s_f", "s_fg", "s_g"]
    if st.button("Get Properties"):
        result = interpolate(sat_temp_df, "T", T, outputs)
        st.write(result)

elif mode == "Saturated Water (by Pressure)":
    P = st.number_input("Enter Pressure (kPa)", min_value=float(sat_press_df["P"].min()), 
                        max_value=float(sat_press_df["P"].max()))
    outputs = ["T", "v_f", "v_fg", "v_g", "u_f", "u_fg", "u_g", "h_f", "h_fg", "h_g", "s_f", "s_fg", "s_g"]
    if st.button("Get Properties"):
        result = interpolate(sat_press_df, "P", P, outputs)
        st.write(result)

else:  # Superheated Vapor
    P = st.selectbox("Select Pressure (MPa)", sorted(superheat_df["P"].unique()))
    T = st.number_input("Enter Temperature (°C)", 
                        min_value=float(superheat_df["T"].min()), 
                        max_value=float(superheat_df["T"].max()))
    df_p = superheat_df[superheat_df["P"] == P]
    outputs = ["v", "u", "h", "s"]
    if st.button("Get Properties"):
        result = interpolate(df_p, "T", T, outputs)
        st.write(result)

# ===== FOOTER =====
st.markdown(
    """
    <hr style="margin-top:50px">
    <div style="text-align:center; font-size:18px;">
        Made with ❤️ by <a href="https://www.linkedin.com/in/suyashsachindamir/" target="_blank">Suyash</a>
        in <a href="https://www.demellogroup.ethz.ch/">deMello group</a>
    </div>
    """,
    unsafe_allow_html=True
)
