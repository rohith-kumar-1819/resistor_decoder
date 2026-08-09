import streamlit as st
import urllib.parse

# 1. Page Configuration & Professional Styling
st.set_page_config(page_title="Professional Resistor Color Code Decoder", page_icon="⚡", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        background-attachment: fixed;
    }
    header[data-testid="stHeader"] { background: transparent !important; }
    .block-container {
        background: rgba(30, 41, 59, 0.85);
        border-radius: 20px;
        padding: 2.5rem 2rem;
        box-shadow: 0 15px 40px rgba(0,0,0,0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-top: 1rem;
        margin-bottom: 2rem;
    }
    h1, h2, h3, h4, p, label { color: #f8fafc !important; }
    </style>
""", unsafe_allow_html=True)

# 2. Dictionaries & Strict Validation Maps
COLOR_HEX = {
    "Black": "#000000", "Brown": "#8B4513", "Red": "#FF0000", "Orange": "#FFA500",
    "Yellow": "#FFFF00", "Green": "#008000", "Blue": "#0000FF", "Violet": "#8A2BE2",
    "Gray": "#808080", "White": "#FFFFFF", "Gold": "#FFD700", "Silver": "#C0C0C0"
}

# Significant digits exclude Gold and Silver for strict validation
digit_colors = ["Black", "Brown", "Red", "Orange", "Yellow", "Green", "Blue", "Violet", "Gray", "White"]
digits = {color: i for i, color in enumerate(digit_colors)}

multipliers = {
    "Black": 1, "Brown": 10, "Red": 100, "Orange": 1000, "Yellow": 10000,
    "Green": 100000, "Blue": 1000000, "Violet": 10000000, "Gray": 100000000,
    "White": 1000000000, "Gold": 0.1, "Silver": 0.01
}

tolerances = {
    "Brown": 1.0, "Red": 2.0, "Green": 0.5, "Blue": 0.25,
    "Violet": 0.1, "Gray": 0.05, "Gold": 5.0, "Silver": 10.0, "None": 20.0
}

# 3. Formatting Function
def format_resistance(val):
    if val >= 1_000_000_000: return f"{val / 1_000_000_000:.2f} GΩ"
    elif val >= 1_000_000: return f"{val / 1_000_000:.2f} MΩ"
    elif val >= 1000: return f"{val / 1000:.2f} kΩ"
    else: return f"{val:g} Ω"

# App Header
st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>⚡ Resistor Color Code Decoder</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 1.1rem;'>Professional Engineering Utility for Resistance & Tolerance Analysis</p>", unsafe_allow_html=True)
st.divider()

# Reset / Band Configuration Controls
col_top1, col_top2, col_top3 = st.columns([2, 2, 1])
with col_top1:
    band_count = st.radio("Number of Bands:", [3, 4, 5], horizontal=True, index=1)
with col_top3:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↻ Reset Defaults", use_container_width=True):
        st.rerun()

# 4. Dynamic User Inputs & Calculation Logic
if band_count == 3:
    c1, c2, c3 = st.columns(3)
    with c1: b1 = st.selectbox("1st Digit", digit_colors, index=4)  # Yellow
    with c2: b2 = st.selectbox("2nd Digit", digit_colors, index=7)  # Violet
    with c3: mult_key = st.selectbox("Multiplier", list(multipliers.keys()), index=2)  # Red
    tol_val = 20.0
    base = (digits[b1] * 10) + digits[b2]
    mult_val = multipliers[mult_key]
    final_res = base * mult_val
    bands_list = [b1, b2, mult_key]
    calc_formula = f"({digits[b1]} \\times 10 + {digits[b2]}) \\times {mult_val:,} = {final_res:g}\\ \\Omega"

elif band_count == 4:
    c1, c2, c3, c4 = st.columns(4)
    with c1: b1 = st.selectbox("1st Digit", digit_colors, index=4)  # Yellow
    with c2: b2 = st.selectbox("2nd Digit", digit_colors, index=7)  # Violet
    with c3: mult_key = st.selectbox("Multiplier", list(multipliers.keys()), index=2)  # Red
    with c4: tol_key = st.selectbox("Tolerance", list(tolerances.keys())[:-1], index=6)  # Gold
    tol_val = tolerances[tol_key]
    base = (digits[b1] * 10) + digits[b2]
    mult_val = multipliers[mult_key]
    final_res = base * mult_val
    bands_list = [b1, b2, mult_key, tol_key]
    calc_formula = f"({digits[b1]} \\times 10 + {digits[b2]}) \\times {mult_val:,} = {final_res:g}\\ \\Omega"

else:  # 5 Bands
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: b1 = st.selectbox("1st Digit", digit_colors, index=4)
    with c2: b2 = st.selectbox("2nd Digit", digit_colors, index=7)
    with c3: b3 = st.selectbox("3rd Digit", digit_colors, index=2)
    with c4: mult_key = st.selectbox("Multiplier", list(multipliers.keys()), index=1)
    with c5: tol_key = st.selectbox("Tolerance", list(tolerances.keys())[:-1], index=0)
    tol_val = tolerances[tol_key]
    base = (digits[b1] * 100) + (digits[b2] * 10) + digits[b3]
    mult_val = multipliers[mult_key]
    final_res = base * mult_val
    bands_list = [b1, b2, b3, mult_key, tol_key]
    calc_formula = f"({digits[b1]} \\times 100 + {digits[b2]} \\times 10 + {digits[b3]}) \\times {mult_val:,} = {final_res:g}\\ \\Omega"

# Tolerance window calculations
min_res = final_res * (1 - tol_val / 100)
max_res = final_res * (1 + tol_val / 100)

# 5. Live SVG Resistor Preview Graphic
svg_bands_html = ""
start_x = 130
spacing = 35
for i, color_name in enumerate(bands_list):
    hx = COLOR_HEX.get(color_name, "#ccc")
    xp = start_x + (i * spacing)
    if i == len(bands_list) - 1 and band_count > 3:
        xp += 25  # gap for tolerance band
    svg_bands_html += f'<rect x="{xp}" y="30" width="12" height="60" fill="{hx}" stroke="#1e293b" stroke-width="1.5"/>'

resistor_preview = f"""
<div style="text-align: center; margin: 25px 0;">
    <svg width="420" height="120" viewBox="0 0 420 120" xmlns="http://www.w3.org/2000/svg">
        <line x1="10" y1="60" x2="80" y2="60" stroke="#94a3b8" stroke-width="6"/>
        <line x1="340" y1="60" x2="410" y2="60" stroke="#94a3b8" stroke-width="6"/>
        <path d="M 80 60 Q 90 25 115 25 L 305 25 Q 330 25 340 60 Q 330 95 305 95 L 115 95 Q 90 95 80 60 Z" fill="#e2e8f0" stroke="#64748b" stroke-width="3"/>
        {svg_bands_html}
    </svg>
</div>
"""
st.markdown(resistor_preview, unsafe_allow_html=True)

# 6. Professional Result Card Layout
st.markdown("### 📊 Calculated Analysis")
res_col1, res_col2 = st.columns([1.5, 1])

with res_col1:
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 12px; border-left: 5px solid #38bdf8;">
        <span style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Resistance Value</span>
        <h2 style="color: #38bdf8; margin: 5px 0 15px 0; font-size: 2.2rem;">{format_resistance(final_res)}</h2>
        <hr style="border-color: rgba(255,255,255,0.1); margin: 10px 0;">
        <p style="margin: 5px 0;"><b>Tolerance:</b> ±{tol_val}%</p>
        <p style="margin: 5px 0;"><b>Acceptable Range:</b> {format_resistance(min_res)} – {format_resistance(max_res)}</p>
    </div>
    """, unsafe_allow_html=True)

with res_col2:
    st.markdown(f"""
    <div style="background: rgba(15, 23, 42, 0.6); padding: 20px; border-radius: 12px; height: 100%;">
        <span style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Active Band Sequence</span>
        <p style="margin-top: 10px; font-weight: bold; color: #f8fafc;">
            {' • '.join(bands_list)}
        </p>
        <span style="color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">Standard Compliance</span>
        <p style="margin-top: 5px; font-size: 0.85rem; color: #cbd5e1;">
            IEC color-coding specification protocol.
        </p>
    </div>
    """, unsafe_allow_html=True)

# 7. Calculation Breakdown Expander
with st.expander("🔍 View Detailed Calculation Breakdown"):
    st.write("Step-by-step mathematical evaluation of the decoded resistor configuration:")
    st.latex(calc_formula)
    st.write(f"- **Nominal Value:** {final_res:,} Ω")
    st.write(f"- **Tolerance Spread:** ±{tol_val}% (Minimum: {min_res:,.2f} Ω, Maximum: {max_res:,.2f} Ω)")

st.divider()

# 8. Color Reference Chart Expander
with st.expander("📚 Resistor Color Reference Chart"):
    st.markdown("Reference guide for standard EIA color-coding values:")
    ref_data = [
        ["Black", "0", "×10⁰ (1)", "—"],
        ["Brown", "1", "×10¹ (10)", "±1%"],
        ["Red", "2", "×10² (100)", "±2%"],
        ["Orange", "3", "×10³ (1k)", "—"],
        ["Yellow", "4", "×10⁴ (10k)", "—"],
        ["Green", "5", "×10⁵ (100k)", "±0.5%"],
        ["Blue", "6", "×10⁶ (1M)", "±0.25%"],
        ["Violet", "7", "×10⁷ (10M)", "±0.1%"],
        ["Gray", "8", "×10⁸ (100M)", "±0.05%"],
        ["White", "9", "×10⁹ (1G)", "—"],
        ["Gold", "—", "×10⁻¹ (0.1)", "±5%"],
        ["Silver", "—", "×10⁻² (0.01)", "±10%"]
    ]
    st.table(ref_data)

# 9. Project Info & Technologies Footer
st.divider()
col_about1, col_about2 = st.columns(2)
with col_about1:
    st.markdown("### About the Tool")
    st.write("This professional engineering utility decodes standard 3, 4, and 5-band resistors, computing exact resistance, tolerance thresholds, and threshold windows dynamically.")
with col_about2:
    st.markdown("### Technologies Used")
    st.markdown("""
    * **Python** (Core data structures & conditional logic)
    * **Streamlit** (Interactive web UI framework)
    * **SVG Graphics** (Real-time dynamic visual rendering)
    * **IEC Standards** (Mathematical compliance algorithm)
    """)

# 10. WhatsApp Share Button
st.divider()
app_url = "https://resistor-color-code-decoder.streamlit.app"
msg = f"Check out my Python Resistor Color Code Decoder app: {app_url}"
whatsapp_link = f"https://api.whatsapp.com/send?text={urllib.parse.quote(msg)}"

st.markdown(
    f"""
    <div style="text-align: center;">
        <a href="{whatsapp_link}" target="_blank">
            <button style="background-color: #25D366; color: white; padding: 12px 24px; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.3);">
                💬 Share App on WhatsApp
            </button>
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)
