import streamlit as st
import urllib.parse


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Resistor Color Code Decoder",
    page_icon="Ω",
    layout="wide"
)


# ============================================================
# RESISTOR COLOR DATA
# ============================================================

digits = {
    "Black": 0,
    "Brown": 1,
    "Red": 2,
    "Orange": 3,
    "Yellow": 4,
    "Green": 5,
    "Blue": 6,
    "Violet": 7,
    "Gray": 8,
    "White": 9
}

multipliers = {
    "Black": 1,
    "Brown": 10,
    "Red": 100,
    "Orange": 1_000,
    "Yellow": 10_000,
    "Green": 100_000,
    "Blue": 1_000_000,
    "Violet": 10_000_000,
    "Gray": 100_000_000,
    "White": 1_000_000_000,
    "Gold": 0.1,
    "Silver": 0.01
}

tolerances = {
    "Brown": 1,
    "Red": 2,
    "Green": 0.5,
    "Blue": 0.25,
    "Violet": 0.1,
    "Gray": 0.05,
    "Gold": 5,
    "Silver": 10
}


# ============================================================
# COLOR EMOJIS
# ============================================================

color_emoji = {
    "Black": "⬛",
    "Brown": "🟫",
    "Red": "🟥",
    "Orange": "🟧",
    "Yellow": "🟨",
    "Green": "🟩",
    "Blue": "🟦",
    "Violet": "🟪",
    "Gray": "⬜",
    "White": "⬜",
    "Gold": "🟨",
    "Silver": "⬜"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_resistance(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} GΩ"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} MΩ"
    elif value >= 1_000:
        return f"{value / 1_000:.2f} kΩ"
    else:
        return f"{value:g} Ω"


def band_display(color):
    return f"{color_emoji.get(color, '⬜')} {color}"


def reset_decoder():
    keys = list(st.session_state.keys())
    for key in keys:
        del st.session_state[key]
    st.rerun()


# ============================================================
# HEADER
# ============================================================

st.title("Ω Resistor Color Code Decoder")

st.write(
    "A Python-based utility for decoding resistor color bands, "
    "calculating resistance, tolerance and resistance range."
)

st.caption(
    "Built with Python • Streamlit • Electronics Fundamentals"
)

st.divider()


# ============================================================
# PAGE LAYOUT
# ============================================================

left_col, main_col, right_col = st.columns(
    [1, 5, 1],
    gap="large"
)


# ============================================================
# LEFT SIDE
# ============================================================

with left_col:
    st.subheader("⚡ Lab Kit")
    st.write("🟥 🟨 🟫")
    st.write("🟫 ⬛ 🟧")
    st.write("🟦 🟪 🟩")
    st.write("🟧 🟨 🟥")
    st.divider()
    st.caption("Electronics")
    st.caption("Resistors")
    st.caption("Color Codes")


# ============================================================
# RIGHT SIDE
# ============================================================

with right_col:
    st.subheader("🎨 Colors")
    st.write("🟦 🟧 🟫")
    st.write("🟪 🟩 🟥")
    st.write("🟨 ⬛ 🟥")
    st.write("⬜ 🟫 ⬜")
    st.divider()
    st.caption("0–9")
    st.caption("Multiplier")
    st.caption("Tolerance")


# ============================================================
# MAIN APPLICATION
# ============================================================

with main_col:
    st.header("🔧 Resistor Configuration")

    band_count = st.radio(
        "Select Number of Bands",
        [3, 4, 5],
        horizontal=True,
        format_func=lambda x: f"{x}-Band"
    )

    st.divider()

    first_band_colors = [
        "Brown", "Red", "Orange", "Yellow",
        "Green", "Blue", "Violet", "Gray", "White"
    ]

    # ========================================================
    # 3-BAND
    # ========================================================
    if band_count == 3:
        col1, col2, col3 = st.columns(3)
        with col1:
            b1 = st.selectbox("1st Band", first_band_colors)
        with col2:
            b2 = st.selectbox("2nd Band", list(digits.keys()))
        with col3:
            multiplier = st.selectbox("Multiplier", list(multipliers.keys()))

        base_value = digits[b1] * 10 + digits[b2]
        tolerance_value = 20
        bands = [b1, b2, multiplier]

    # ========================================================
    # 4-BAND
    # ========================================================
    elif band_count == 4:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            b1 = st.selectbox("1st Band", first_band_colors)
        with col2:
            b2 = st.selectbox("2nd Band", list(digits.keys()))
        with col3:
            multiplier = st.selectbox("Multiplier", list(multipliers.keys()))
        with col4:
            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base_value = digits[b1] * 10 + digits[b2]
        tolerance_value = tolerances[tolerance_band]
        bands = [b1, b2, multiplier, tolerance_band]

    # ========================================================
    # 5-BAND
    # ========================================================
    else:
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            b1 = st.selectbox("1st Band", first_band_colors)
        with col2:
            b2 = st.selectbox("2nd Band", list(digits.keys()))
        with col3:
            b3 = st.selectbox("3rd Band", list(digits.keys()))
        with col4:
            multiplier = st.selectbox("Multiplier", list(multipliers.keys()))
        with col5:
            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base_value = digits[b1] * 100 + digits[b2] * 10 + digits[b3]
        tolerance_value = tolerances[tolerance_band]
        bands = [b1, b2, b3, multiplier, tolerance_band]

    # ========================================================
    # CALCULATION
    # ========================================================
    multiplier_value = multipliers[multiplier]
    resistance = base_value * multiplier_value
    minimum_resistance = resistance * (1 - tolerance_value / 100)
    maximum_resistance = resistance * (1 + tolerance_value / 100)

    # ========================================================
    # RESISTOR PREVIEW
    # ========================================================
    st.subheader("🎨 Resistor Preview")
    preview = "──── "
    for band in bands:
        preview += color_emoji.get(band, "⬜") + " "
    preview += "────"

    st.write(preview, unsafe_allow_html=False)
    st.caption(" • ".join(bands))

    # ========================================================
    # RESULT
    # ========================================================
    st.divider()
    st.subheader("📊 Calculated Result")

    result1, result2 = st.columns(2)
    with result1:
        st.metric("Resistance", format_resistance(resistance))
    with result2:
        st.metric("Tolerance", f"±{tolerance_value:g}%")

    # ========================================================
    # CALCULATION BREAKDOWN
    # ========================================================
    st.subheader("🧮 Calculation Breakdown")
    st.code(
        f"""Significant Digits : {base_value}
Multiplier         : × {multiplier_value:g}

Resistance
= {base_value} × {multiplier_value:g}
= {resistance:g} Ω

Tolerance
= ±{tolerance_value:g}%""",
        language="text"
    )

    # ========================================================
    # RESISTANCE RANGE
    # ========================================================
    st.subheader("📏 Resistance Range")
    range1, range2, range3 = st.columns(3)
    with range1:
        st.metric("Minimum", format_resistance(minimum_resistance))
    with range2:
        st.metric("Nominal", format_resistance(resistance))
    with range3:
        st.metric("Maximum", format_resistance(maximum_resistance))

    # ========================================================
    # ACTIONS
    # ========================================================
    st.subheader("🔄 Actions")
    action1, action2 = st.columns(2)
    with action1:
        if st.button("↻ Reset Decoder", use_container_width=True):
            reset_decoder()
    with action2:
        st.write("Change any band above to calculate again.")

# ============================================================
# COLOR REFERENCE TABLE
# ============================================================
st.divider()
st.header("📚 Resistor Color Reference")

reference_data = []
for color, digit in digits.items():
    reference_data.append({
        "Color": color,
        "Digit": digit,
        "Multiplier": f"×{multipliers[color]:g}",
        "Tolerance": f"±{tolerances[color]}%" if color in tolerances else "—"
    })

reference_data.append({"Color": "Gold", "Digit": "—", "Multiplier": "×0.1", "Tolerance": "±5%"})
reference_data.append({"Color": "Silver", "Digit": "—", "Multiplier": "×0.01", "Tolerance": "±10%"})

st.dataframe(reference_data, use_container_width=True, hide_index=True)

# ============================================================
# HOW IT WORKS
# ============================================================
st.divider()
st.header("📖 How the Decoder Works")

info1, info2, info3 = st.columns(3)
with info1:
    st.subheader("3-Band")
    st.write("Two significant digits + multiplier.")
    st.code("R = (10D₁ + D₂) × 10ᴹ")
with info2:
    st.subheader("4-Band")
    st.write("Two significant digits + multiplier + tolerance.")
    st.code("R = (10D₁ + D₂) × 10ᴹ")
with info3:
    st.subheader("5-Band")
    st.write("Three significant digits + multiplier + tolerance.")
    st.code("R = (100D₁ + 10D₂ + D₃) × 10ᴹ")

# ============================================================
# ABOUT PROJECT
# ============================================================
st.divider()
about1, about2 = st.columns(2)
with about1:
    st.subheader("💡 About the Project")
    st.write("This application is a Python-based resistor color code decoder designed to quickly determine resistance values from standard resistor color bands.")
    st.write("It supports 3-band, 4-band and 5-band resistors.")
with about2:
    st.subheader("🛠 Technologies Used")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• Dictionaries")
    st.write("• Conditional Logic")
    st.write("• Electronics Fundamentals")

# ============================================================
# SHARE
# ============================================================
st.divider()
st.subheader("🔗 Share Project")
app_url = "https://resistor-color-code-decoder.streamlit.app"
message = "Check out my Python Resistor Color Code Decoder: " + app_url
whatsapp_url = "https://api.whatsapp.com/send?text=" + urllib.parse.quote(message)

st.link_button("💬 Share on WhatsApp", whatsapp_url, use_container_width=True)

# ============================================================
# FOOTER
# ============================================================
st.divider()
st.caption("Ω Resistor Color Code Decoder • Built with Python & Streamlit")
