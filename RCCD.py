import streamlit as st
import urllib.parse

# 1. Web UI Setup (Wide layout with vibrant gradient & glassmorphic card styling)
st.set_page_config(page_title="Python Resistor Decoder", page_icon="Ω", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
        background-attachment: fixed;
    }
    /* Glassmorphism Card Container for High Contrast and Readability */
    .block-container {
        background: rgba(18, 18, 28, 0.9);
        border-radius: 24px;
        padding: 3rem 2rem;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    /* Crisp text colors for clear readability */
    h1, h2, h3, p, label, .stRadio label {
        color: #FFFFFF !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.3);
    }
    /* Selectbox styling inside card */
    .stSelectbox div[data-baseweb="select"] {
        background-color: rgba(255, 255, 255, 0.08);
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Python Dictionaries
digits = {
    "Black": 0, "Brown": 1, "Red": 2, "Orange": 3, "Yellow": 4,
    "Green": 5, "Blue": 6, "Violet": 7, "Gray": 8, "White": 9
}
multipliers = {
    "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
    "Green": 100000, "Blue": 1000000, "Violet": 10000000, "Gray": 100000000,
    "White": 1000000000, "Gold": 0.1, "Silver": 0.01
}
tolerances = {
    "Brown": 1, "Red": 2, "Green": 0.5, "Blue": 0.25,
    "Violet": 0.1, "Gray": 0.05, "Gold": 5, "Silver": 10
}

COLOR_HEX = {
    "Black": "#000000", "Brown": "#8B4513", "Red": "#FF0000", "Orange": "#FFA500",
    "Yellow": "#FFFF00", "Green": "#008000", "Blue": "#0000FF", "Violet": "#8A2BE2",
    "Gray": "#808080", "White": "#FFFFFF", "Gold": "#FFD700", "Silver": "#C0C0C0"
}

# 3. Formatting Function
def format_resistance(value):
    if value >= 1_000_000_000: return f"{value / 1_000_000_000:.2f} GΩ"
    elif value >= 1_000_000: return f"{value / 1_000_000:.2f} MΩ"
    elif value >= 1000: return f"{value / 1000:.2f} kΩ"
    else: return f"{value:g} Ω"

# Helper function to generate decorative side resistors
def deco_resistor(c1, c2, c3, c4):
    return f"""
    <div style="text-align: center; margin-bottom: 25px;">
        <svg width="110" height="45" viewBox="0 0 130 50">
            <line x1="5" y1="25" x2="35" y2="25" stroke="#FFF" stroke-width="4"/>
            <line x1="95" y1="25" x2="125" y2="25" stroke="#FFF" stroke-width="4"/>
            <path d="M 35 25 Q 40 10 55 10 L 75 10 Q 90 10 95 25 Q 90 40 75 40 L 55 40 Q 40 40 35 25 Z" fill="#D2B48C" stroke="#222" stroke-width="2"/>
            <rect x="52" y="12" width="5" height="26" fill="{c1}"/>
            <rect x="62" y="12" width="5" height="26" fill="{c2}"/>
            <rect x="72" y="12" width="5" height="26" fill="{c3}"/>
            <rect x="83" y="12" width="4" height="26" fill="{c4}"/>
        </svg>
    </div>
    """

# Create a 3-Column Layout: Left Side, Center Content, Right Side
left_col, center_col, right_col = st.columns([1, 4, 1])

# --- LEFT DECORATIVE COLUMN ---
with left_col:
    st.markdown("<p style='text-align: center; font-weight: bold; color: #fff;'>⚡ Lab Kit</p>", unsafe_allow_html=True)
    st.markdown(deco_resistor("#FF0000", "#FF0000", "#8B4513", "#FFD700"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#8B4513", "#000000", "#FFA500", "#C0C0C0"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#0000FF", "#8A2BE2", "#008000", "#FFD700"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#FFA500", "#FFFF00", "#FF0000", "#8B4513"), unsafe_allow_html=True)

# --- CENTER MAIN APP COLUMN ---
with center_col:
    st.title("Ω Resistor Color Code Decoder")
    st.write("A Python-based utility using dictionaries and conditional logic.")

    band_count = st.radio("Select Number of Bands:", [3, 4, 5], horizontal=True)

    cols = st.columns(band_count)

    with cols[0]: b1 = st.selectbox("1st Band", list(digits.keys()))
    with cols[1]: b2 = st.selectbox("2nd Band", list(digits.keys()))

    if band_count == 5:
        with cols[2]: b3 = st.selectbox("3rd Band", list(digits.keys()))
        with cols[3]: mult = st.selectbox("Multiplier", list(multipliers.keys()))
        with cols[4]: tol = st.selectbox("Tolerance", list(tolerances.keys()))
        base = (digits[b1] * 100) + (digits[b2] * 10) + digits[b3]
        tol_val = tolerances[tol]
        bands = [b1, b2, b3, mult, tol]
    else:
        with cols[2]: mult = st.selectbox("Multiplier", list(multipliers.keys()))
        if band_count == 4:
            with cols[3]: tol = st.selectbox("Tolerance", list(tolerances.keys()))
            base = (digits[b1] * 10) + digits[b2]
            tol_val = tolerances[tol]
            bands = [b1, b2, mult, tol]
        else:
            base = (digits[b1] * 10) + digits[b2]
            tol_val = 20
            bands = [b1, b2, mult]

    final_res = base * multipliers[mult]

    # --- COLORFUL DYNAMIC RESISTOR GRAPHIC ---
    svg_bands = ""
    start_x = 130
    spacing = 35

    for i, color in enumerate(bands):
        hex_code = COLOR_HEX.get(color, "#D3D3D3")
        x_pos = start_x + (i * spacing)
        if i == len(bands) - 1 and band_count > 3:
            x_pos += 25
        svg_bands += f'<rect x="{x_pos}" y="30" width="12" height="60" fill="{hex_code}" stroke="#000" stroke-width="1"/>'

    resistor_svg = f"""
    <div style="text-align: center; margin: 20px 0;">
        <svg width="400" height="120" viewBox="0 0 400 120" xmlns="http://www.w3.org/2000/svg">
            <line x1="10" y1="60" x2="80" y2="60" stroke="#FFFFFF" stroke-width="8"/>
            <line x1="320" y1="60" x2="390" y2="60" stroke="#FFFFFF" stroke-width="8"/>
            <path d="M 80 60 Q 90 30 110 30 L 290 30 Q 310 30 320 60 Q 310 90 290 90 L 110 90 Q 90 90 80 60 Z" fill="#D2B48C" stroke="#333333" stroke-width="3"/>
            {svg_bands}
        </svg>
    </div>
    """

    st.markdown(resistor_svg, unsafe_allow_html=True)

    # Display Results clearly
    st.divider()
    st.success(f"### Resistance: **{format_resistance(final_res)}**")
    st.info(f"### Tolerance: **±{tol_val}%**")

    # WhatsApp Share Button
    st.divider()
    app_url = "https://resistor-color-code-decoder.streamlit.app"
    msg = f"Check out my Python Resistor Color Code Decoder app: {app_url}"
    whatsapp_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg)}"

    st.markdown(
        f"""
        <a href="{whatsapp_link}" target="_blank">
            <button style="background-color: #25D366; color: white; padding: 12px 20px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; width: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                💬 Share on WhatsApp
            </button>
        </a>
    """,
        unsafe_allow_html=True,
    )

# --- RIGHT DECORATIVE COLUMN ---
with right_col:
    st.markdown("<p style='text-align: center; font-weight: bold; color: #fff;'>🎨 Colors</p>", unsafe_allow_html=True)
    st.markdown(deco_resistor("#0000FF", "#FFA500", "#8B4513", "#FFD700"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#8A2BE2", "#008000", "#FF0000", "#C0C0C0"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#FFFF00", "#000000", "#FF0000", "#FFD700"), unsafe_allow_html=True)
    st.markdown(deco_resistor("#808080", "#FFFFFF", "#8B4513", "#C0C0C0"), unsafe_allow_html=True)
