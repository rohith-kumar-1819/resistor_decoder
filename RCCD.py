import streamlit as st
import matplotlib.pyplot as plt
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
# RESISTOR DATA
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


# Matplotlib color names

color_map = {
    "Black": "black",
    "Brown": "brown",
    "Red": "red",
    "Orange": "orange",
    "Yellow": "yellow",
    "Green": "green",
    "Blue": "blue",
    "Violet": "violet",
    "Gray": "gray",
    "White": "white",
    "Gold": "gold",
    "Silver": "silver"
}


# ============================================================
# FUNCTIONS
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


def draw_resistor(bands):
    """
    Draw resistor using Matplotlib.
    No HTML/SVG is used.
    """

    fig, ax = plt.subplots(figsize=(8, 2))

    # Resistor body
    body = plt.Rectangle(
        (2, 0.3),
        6,
        1.4,
        facecolor="#D2B48C",
        edgecolor="black",
        linewidth=2
    )

    ax.add_patch(body)

    # Left wire
    ax.plot(
        [0, 2],
        [1, 1],
        color="black",
        linewidth=5
    )

    # Right wire
    ax.plot(
        [8, 10],
        [1, 1],
        color="black",
        linewidth=5
    )

    # Draw bands
    band_positions = []

    if len(bands) == 3:
        band_positions = [3.0, 4.0, 5.0]

    elif len(bands) == 4:
        band_positions = [3.0, 4.0, 5.0, 6.2]

    elif len(bands) == 5:
        band_positions = [2.8, 3.7, 4.6, 5.5, 6.7]

    for position, band in zip(band_positions, bands):

        rect = plt.Rectangle(
            (position, 0.3),
            0.22,
            1.4,
            facecolor=color_map[band],
            edgecolor="black",
            linewidth=0.8
        )

        ax.add_patch(rect)

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 2)
    ax.axis("off")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)


def reset():
    st.session_state.clear()
    st.rerun()


# ============================================================
# TITLE
# ============================================================

st.title("Ω Resistor Color Code Decoder")

st.write(
    "A Python-based resistor calculator using "
    "dictionaries, conditional logic and Streamlit."
)

st.divider()


# ============================================================
# MAIN LAYOUT
# ============================================================

left, center, right = st.columns([1, 5, 1])


# ============================================================
# LEFT PANEL
# ============================================================

with left:

    st.subheader("⚡ Lab Kit")

    st.write("🔴 🟡 🟤")
    st.write("🟤 ⚫ 🟠")
    st.write("🔵 🟣 🟢")
    st.write("🟠 🟡 🔴")


# ============================================================
# CENTER PANEL
# ============================================================

with center:

    st.header("🔧 Resistor Configuration")

    # --------------------------------------------------------
    # BAND COUNT
    # --------------------------------------------------------

    band_count = st.radio(
        "Select Number of Bands",
        [3, 4, 5],
        horizontal=True,
        format_func=lambda x: f"{x}-Band"
    )

    st.divider()


    # --------------------------------------------------------
    # FIRST BAND
    # --------------------------------------------------------

    # Black cannot normally be the first significant digit.

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
                first_band_colors
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with col3:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        base = (
            digits[b1] * 10
            + digits[b2]
        )

        tolerance = 20

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
                first_band_colors
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with col3:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        with col4:

            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base = (
            digits[b1] * 10
            + digits[b2]
        )

        tolerance = tolerances[tolerance_band]

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
                first_band_colors
            )

        with col2:

            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with col3:

            b3 = st.selectbox(
                "3rd Band",
                list(digits.keys())
            )

        with col4:

            multiplier = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        with col5:

            tolerance_band = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base = (
            digits[b1] * 100
            + digits[b2] * 10
            + digits[b3]
        )

        tolerance = tolerances[tolerance_band]

        bands = [
            b1,
            b2,
            b3,
            multiplier,
            tolerance_band
        ]


    # ========================================================
    # CALCULATE
    # ========================================================

    multiplier_value = multipliers[multiplier]

    resistance = base * multiplier_value

    minimum = resistance * (1 - tolerance / 100)

    maximum = resistance * (1 + tolerance / 100)


    # ========================================================
    # RESISTOR VISUALIZATION
    # ========================================================

    st.subheader("🎨 Resistor Preview")

    draw_resistor(bands)


    # ========================================================
    # RESULT
    # ========================================================

    st.subheader("📊 Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:

        st.metric(
            "Resistance",
            format_resistance(resistance)
        )

    with result_col2:

        st.metric(
            "Tolerance",
            f"±{tolerance:g}%"
        )


    # ========================================================
    # CALCULATION
    # ========================================================

    st.subheader("🧮 Calculation")

    st.code(
        f"""Significant digits = {base}
Multiplier = {multiplier_value:g}

Resistance =
{base} × {multiplier_value:g}

= {resistance:g} Ω

Tolerance = ±{tolerance:g}%""",
        language="text"
    )


    # ========================================================
    # RANGE
    # ========================================================

    st.subheader("📏 Resistance Range")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "Minimum",
            format_resistance(minimum)
        )

    with c2:

        st.metric(
            "Nominal",
            format_resistance(resistance)
        )

    with c3:

        st.metric(
            "Maximum",
            format_resistance(maximum)
        )


    # ========================================================
    # RESET
    # ========================================================

    if st.button(
        "↻ Reset Decoder",
        use_container_width=True
    ):
        reset()


# ============================================================
# RIGHT PANEL
# ============================================================

with right:

    st.subheader("🎨 Colors")

    st.write("🔵 🟠 🟤")
    st.write("🟣 🟢 🔴")
    st.write("🟡 ⚫ 🔴")
    st.write("⚪ 🟤 🩶")


# ============================================================
# COLOR REFERENCE
# ============================================================

st.divider()

st.header("📚 Resistor Color Reference")

reference_data = []

for color in digits:

    tolerance_value = tolerances.get(color, "—")

    reference_data.append({
        "Color": color,
        "Digit": digits[color],
        "Multiplier": multipliers[color],
        "Tolerance": (
            f"±{tolerance_value}%"
            if tolerance_value != "—"
            else "—"
        )
    })


# Add Gold and Silver separately

reference_data.append({
    "Color": "Gold",
    "Digit": "—",
    "Multiplier": "×0.1",
    "Tolerance": "±5%"
})

reference_data.append({
    "Color": "Silver",
    "Digit": "—",
    "Multiplier": "×0.01",
    "Tolerance": "±10%"
})


st.dataframe(
    reference_data,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# ABOUT
# ============================================================

st.divider()

about1, about2 = st.columns(2)

with about1:

    st.subheader("💡 About")

    st.write(
        "This application decodes resistor color bands and "
        "calculates resistance, tolerance and resistance range."
    )

    st.write(
        "It supports 3-band, 4-band and 5-band resistor "
        "configurations."
    )


with about2:

    st.subheader("🛠 Technologies")

    st.write("• Python")
    st.write("• Streamlit")
    st.write("• Python Dictionaries")
    st.write("• Conditional Logic")
    st.write("• Matplotlib")
    st.write("• Electronics fundamentals")


# ============================================================
# WHATSAPP SHARE
# ============================================================

st.divider()

app_url = "https://resistor-color-code-decoder.streamlit.app"

message = (
    "Check out my Python Resistor Color Code Decoder: "
    + app_url
)

whatsapp_url = (
    "https://api.whatsapp.com/send?text="
    + urllib.parse.quote(message)
)

st.markdown(
    f"Share your project: {whatsapp_url}"
)


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "Ω Resistor Color Code Decoder • Built with Python & Streamlit"
)
