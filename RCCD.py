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
# COLOR SYMBOLS
# ============================================================

# These are only Unicode symbols.
# No HTML, CSS, SVG or external visualization library is used.

color_symbol = {
    "Black": "⬛",
    "Brown": "🟫",
    "Red": "🟥",
    "Orange": "🟧",
    "Yellow": "🟨",
    "Green": "🟩",
    "Blue": "🟦",
    "Violet": "🟪",
    "Gray": "◻️",
    "White": "⬜",
    "Gold": "🟨",
    "Silver": "◽"
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_resistance(value):
    """
    Convert resistance value into a readable format.
    """

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} GΩ"

    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} MΩ"

    elif value >= 1_000:
        return f"{value / 1_000:.2f} kΩ"

    else:
        return f"{value:g} Ω"


def display_band(color):
    """
    Return a simple Streamlit-friendly representation
    of a resistor color.
    """

    return f"{color_symbol[color]} {color}"


def reset_decoder():
    """
    Reset the application.
    """

    st.session_state.clear()
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
    st.write("⬜ 🟫 ◻️")

    st.divider()

    st.caption("Digit")
    st.caption("Multiplier")
    st.caption("Tolerance")


# ============================================================
# MAIN APPLICATION
# ============================================================

with main_col:

    st.header("🔧 Resistor Configuration")

    # --------------------------------------------------------
    # SELECT NUMBER OF BANDS
    # --------------------------------------------------------

    band_count = st.radio(
        "Select Number of Bands",
        [3, 4, 5],
        horizontal=True,
        format_func=lambda x: f"{x}-Band",
        key="band_count"
    )

    st.divider()


    # --------------------------------------------------------
    # FIRST BAND COLORS
    # --------------------------------------------------------
    #
    # Black is excluded because the first significant digit
    # of a normal resistor cannot be zero.
    # --------------------------------------------------------

    first_band_colors = [
        "Brown",
        "Red",
        "Orange",
        "Yellow",
        "Green",
        "Blue",
        "Violet",
        "Gray",
        "White"
    ]


    # ========================================================
    # 3-BAND RESISTOR
    # ========================================================

    if band_count == 3:

        col1, col2, col3 = st.columns(3)

        with col1:

            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="band_1"
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="band_2"
            )

        with col3:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="band_mult"
            )

        # Two significant digits
        base_value = (
            digits[b1] * 10
            + digits[b2]
        )

        # Standard 3-band resistor tolerance
        tolerance_value = 20

        bands = [
            b1,
            b2,
            multiplier
        ]


    # ========================================================
    # 4-BAND RESISTOR
    # ========================================================

    elif band_count == 4:

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="band_1"
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="band_2"
            )

        with col3:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="band_mult"
            )

        with col4:

            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold"),
                key="band_tol"
            )

        # Two significant digits
        base_value = (
            digits[b1] * 10
            + digits[b2]
        )

        tolerance_value = tolerances[tolerance_band]

        bands = [
            b1,
            b2,
            multiplier,
            tolerance_band
        ]


    # ========================================================
    # 5-BAND RESISTOR
    # ========================================================

    else:

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:

            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="band_1"
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="band_2"
            )

        with col3:

            b3 = st.selectbox(
                "3rd Band",
                list(digits.keys()),
                key="band_3"
            )

        with col4:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="band_mult"
            )

        with col5:

            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold"),
                key="band_tol"
            )

        # Three significant digits
        base_value = (
            digits[b1] * 100
            + digits[b2] * 10
            + digits[b3]
        )

        tolerance_value = tolerances[tolerance_band]

        bands = [
            b1,
            b2,
            b3,
            multiplier,
            tolerance_band
        ]


    # ========================================================
    # RESISTANCE CALCULATION
    # ========================================================

    multiplier_value = multipliers[multiplier]

    resistance = (
        base_value * multiplier_value
    )

    minimum_resistance = (
        resistance *
        (1 - tolerance_value / 100)
    )

    maximum_resistance = (
        resistance *
        (1 + tolerance_value / 100)
    )


    # ========================================================
    # RESISTOR PREVIEW
    # ========================================================

    st.subheader("🎨 Resistor Preview")

    st.info(
        "   ───  "
        + "  ".join(
            color_symbol[band]
            for band in bands
        )
        + "  ───"
    )

    st.caption(
        "  •  ".join(bands)
    )


    # ========================================================
    # BAND INFORMATION
    # ========================================================

    st.subheader("🔍 Band Information")

    band_columns = st.columns(len(bands))

    for index, (column, band) in enumerate(
        zip(band_columns, bands)
    ):

        with column:

            if index == len(bands) - 1 and band_count >= 4:

                # Last band = tolerance
                st.metric(
                    "Tolerance",
                    f"±{tolerances[band]}%"
                )

            elif index == len(bands) - 2 and band_count >= 4:

                # Second last band = multiplier
                st.metric(
                    "Multiplier",
                    f"×{multipliers[band]:g}"
                )

            elif index < band_count - 1:

                st.metric(
                    f"Band {index + 1}",
                    str(digits[band])
                )

            else:

                st.metric(
                    "Multiplier",
                    f"×{multipliers[band]:g}"
                )


    # ========================================================
    # CALCULATED RESULT
    # ========================================================

    st.divider()

    st.subheader("📊 Calculated Result")

    result1, result2 = st.columns(2)

    with result1:

        st.metric(
            "Resistance",
            format_resistance(resistance)
        )

    with result2:

        st.metric(
            "Tolerance",
            f"±{tolerance_value:g}%"
        )


    # ========================================================
    # CALCULATION BREAKDOWN
    # ========================================================

    st.subheader("🧮 Calculation Breakdown")

    if band_count == 3:

        formula = (
            f"({digits[b1]} × 10 + {digits[b2]}) "
            f"× {multiplier_value:g}"
        )

    elif band_count == 4:

        formula = (
            f"({digits[b1]} × 10 + {digits[b2]}) "
            f"× {multiplier_value:g}"
        )

    else:

        formula = (
            f"({digits[b1]} × 100 + "
            f"{digits[b2]} × 10 + "
            f"{digits[b3]}) "
            f"× {multiplier_value:g}"
        )


    st.code(
        f"""Significant Digits : {base_value}
Multiplier         : × {multiplier_value:g}

Formula:
{formula}

Resistance:
= {resistance:g} Ω

Tolerance:
= ±{tolerance_value:g}%""",
        language="text"
    )


    # ========================================================
    # RESISTANCE RANGE
    # ========================================================

    st.subheader("📏 Resistance Range")

    range1, range2, range3 = st.columns(3)

    with range1:

        st.metric(
            "Minimum",
            format_resistance(
                minimum_resistance
            )
        )

    with range2:

        st.metric(
            "Nominal",
            format_resistance(
                resistance
            )
        )

    with range3:

        st.metric(
            "Maximum",
            format_resistance(
                maximum_resistance
            )
        )


    # ========================================================
    # ACTIONS
    # ========================================================

    st.subheader("🔄 Actions")

    action1, action2 = st.columns(2)

    with action1:

        if st.button(
            "↻ Reset Decoder",
            use_container_width=True
        ):
            reset_decoder()

    with action2:

        st.write(
            "Change any band above to calculate "
            "a new resistor value."
        )


# ============================================================
# RESISTOR COLOR REFERENCE
# ============================================================

st.divider()

st.header("📚 Resistor Color Reference")


reference_data = []


for color, digit in digits.items():

    tolerance_text = "—"

    if color in tolerances:
        tolerance_text = f"±{tolerances[color]}%"

    reference_data.append(
        {
            "Color": color,
            "Digit": digit,
            "Multiplier": f"×{multipliers[color]:g}",
            "Tolerance": tolerance_text
        }
    )


# Gold

reference_data.append(
    {
        "Color": "Gold",
        "Digit": "—",
        "Multiplier": "×0.1",
        "Tolerance": "±5%"
    }
)


# Silver

reference_data.append(
    {
        "Color": "Silver",
        "Digit": "—",
        "Multiplier": "×0.01",
        "Tolerance": "±10%"
    }
)


st.dataframe(
    reference_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# HOW THE DECODER WORKS
# ============================================================

st.divider()

st.header("📖 How the Decoder Works")


info1, info2, info3 = st.columns(3)


with info1:

    st.subheader("3-Band")

    st.write(
        "Two significant digits + multiplier."
    )

    st.code(
        "R = (10D₁ + D₂) × 10ᴹ"
    )


with info2:

    st.subheader("4-Band")

    st.write(
        "Two significant digits + multiplier "
        "+ tolerance."
    )

    st.code(
        "R = (10D₁ + D₂) × 10ᴹ"
    )


with info3:

    st.subheader("5-Band")

    st.write(
        "Three significant digits + multiplier "
        "+ tolerance."
    )

    st.code(
        "R = (100D₁ + 10D₂ + D₃) × 10ᴹ"
    )


# ============================================================
# ABOUT PROJECT
# ============================================================

st.divider()

about1, about2 = st.columns(2)


with about1:

    st.subheader("💡 About the Project")

    st.write(
        "This application is a Python-based resistor "
        "color code decoder designed to determine "
        "resistance values from standard resistor bands."
    )

    st.write(
        "It supports 3-band, 4-band and 5-band "
        "resistor configurations."
    )


with about2:

    st.subheader("🛠 Technologies Used")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• Python Dictionaries")
    st.write("• Conditional Logic")
    st.write("• Electronics Fundamentals")


# ============================================================
# SHARE PROJECT
# ============================================================

st.divider()

st.subheader("🔗 Share Project")

app_url = (
    "https://resistor-color-code-decoder.streamlit.app"
)

message = (
    "Check out my Python Resistor Color Code Decoder: "
    + app_url
)

whatsapp_url = (
    "https://api.whatsapp.com/send?text="
    + urllib.parse.quote(message)
)


st.link_button(
    "💬 Share on WhatsApp",
    whatsapp_url,
    use_container_width=True
)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Ω Resistor Color Code Decoder • "
    "Built with Python & Streamlit"
)
