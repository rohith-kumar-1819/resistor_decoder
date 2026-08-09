import streamlit as st
import urllib.parse


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Resistor Color Code Decoder",
    page_icon="Ω",
    layout="wide"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(65,88,208,0.25), transparent 30%),
        radial-gradient(circle at 90% 80%, rgba(200,80,192,0.20), transparent 30%),
        linear-gradient(135deg, #111323 0%, #171426 50%, #25162b 100%);
    background-attachment: fixed;
}

/* Main width */
.block-container {
    max-width: 1350px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* Text */
h1, h2, h3, h4, p, label {
    color: white !important;
}

/* Select boxes */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

/* Radio */
.stRadio label {
    color: white !important;
}

/* Buttons */
.stButton > button {
    border-radius: 10px;
    min-height: 44px;
    font-weight: 700;
}

/* Divider */
hr {
    border-color: rgba(255,255,255,0.12) !important;
}

</style>
""", unsafe_allow_html=True)


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

COLOR_HEX = {
    "Black": "#000000",
    "Brown": "#8B4513",
    "Red": "#FF0000",
    "Orange": "#FFA500",
    "Yellow": "#FFD700",
    "Green": "#008000",
    "Blue": "#0000FF",
    "Violet": "#8A2BE2",
    "Gray": "#808080",
    "White": "#FFFFFF",
    "Gold": "#FFD700",
    "Silver": "#C0C0C0"
}


# ============================================================
# FUNCTIONS
# ============================================================

def format_resistance(value):

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} GΩ"

    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f} MΩ"

    if value >= 1_000:
        return f"{value / 1_000:.2f} kΩ"

    return f"{value:g} Ω"


def decorative_resistor(c1, c2, c3, c4):

    return f"""
    <div style="text-align:center; margin:20px 0;">

        <svg width="180" height="65"
             viewBox="0 0 180 65"
             xmlns="http://www.w3.org/2000/svg">

            <line x1="5" y1="32"
                  x2="35" y2="32"
                  stroke="white"
                  stroke-width="4"/>

            <line x1="145" y1="32"
                  x2="175" y2="32"
                  stroke="white"
                  stroke-width="4"/>

            <rect x="35" y="12"
                  width="110"
                  height="40"
                  rx="20"
                  fill="#D2B48C"
                  stroke="#444"
                  stroke-width="2"/>

            <rect x="62" y="12"
                  width="7"
                  height="40"
                  fill="{c1}"/>

            <rect x="78" y="12"
                  width="7"
                  height="40"
                  fill="{c2}"/>

            <rect x="94" y="12"
                  width="7"
                  height="40"
                  fill="{c3}"/>

            <rect x="120" y="12"
                  width="7"
                  height="40"
                  fill="{c4}"/>

        </svg>

    </div>
    """


def main_resistor(bands):

    svg_bands = ""

    start_x = 145
    spacing = 35

    for i, color in enumerate(bands):

        x = start_x + i * spacing

        if i == len(bands) - 1 and len(bands) > 3:
            x += 20

        svg_bands += f"""
        <rect
            x="{x}"
            y="30"
            width="14"
            height="60"
            fill="{COLOR_HEX[color]}"
            stroke="#222"
            stroke-width="1.5"
        />
        """

    return f"""
    <div style="display:flex; justify-content:center;">

        <svg width="500"
             height="130"
             viewBox="0 0 500 130"
             xmlns="http://www.w3.org/2000/svg">

            <line
                x1="10"
                y1="65"
                x2="100"
                y2="65"
                stroke="white"
                stroke-width="7"
            />

            <line
                x1="400"
                y1="65"
                x2="490"
                y2="65"
                stroke="white"
                stroke-width="7"
            />

            <path
                d="
                M100 65
                Q110 32 135 32
                L365 32
                Q390 32 400 65
                Q390 98 365 98
                L135 98
                Q110 98 100 65
                Z
                "
                fill="#D2B48C"
                stroke="#333"
                stroke-width="3"
            />

            {svg_bands}

        </svg>

    </div>
    """


# ============================================================
# HERO
# ============================================================

st.html("""
<div style="
    text-align:center;
    padding:25px 10px 18px 10px;
">

    <div style="
        font-size:42px;
        font-weight:800;
        color:white;
        margin-bottom:8px;
    ">
        Ω Resistor Color Code Decoder
    </div>

    <div style="
        color:#c9c9d8;
        font-size:17px;
        margin-bottom:15px;
    ">
        Decode resistor values, multipliers and tolerances instantly.
    </div>

    <span style="
        display:inline-block;
        padding:7px 16px;
        border-radius:20px;
        background:rgba(255,255,255,0.08);
        border:1px solid rgba(255,255,255,0.15);
        color:#eeeeff;
        font-size:13px;
    ">
        Python • Streamlit • Electronics
    </span>

</div>
""")


# ============================================================
# THREE COLUMNS
# ============================================================

left, center, right = st.columns(
    [1, 5, 1],
    gap="large"
)


# ============================================================
# LEFT
# ============================================================

with left:

    st.markdown("### ⚡ Lab Kit")

    st.html(
        decorative_resistor(
            "#FF0000",
            "#FF0000",
            "#8B4513",
            "#FFD700"
        )
    )

    st.html(
        decorative_resistor(
            "#8B4513",
            "#000000",
            "#FFA500",
            "#C0C0C0"
        )
    )

    st.html(
        decorative_resistor(
            "#0000FF",
            "#8A2BE2",
            "#008000",
            "#FFD700"
        )
    )


# ============================================================
# RIGHT
# ============================================================

with right:

    st.markdown("### 🎨 Colors")

    st.html(
        decorative_resistor(
            "#0000FF",
            "#FFA500",
            "#8B4513",
            "#FFD700"
        )
    )

    st.html(
        decorative_resistor(
            "#8A2BE2",
            "#008000",
            "#FF0000",
            "#C0C0C0"
        )
    )

    st.html(
        decorative_resistor(
            "#FFFF00",
            "#000000",
            "#FF0000",
            "#FFD700"
        )
    )


# ============================================================
# CENTER
# ============================================================

with center:

    st.markdown("### 🔧 Resistor Configuration")

    band_count = st.radio(
        "Select Number of Bands",
        [3, 4, 5],
        horizontal=True,
        format_func=lambda x: f"{x}-Band"
    )

    # First band cannot normally be black.
    first_colors = [
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

    # --------------------------------------------------------
    # 3 BAND
    # --------------------------------------------------------

    if band_count == 3:

        c1, c2, c3 = st.columns(3)

        with c1:
            b1 = st.selectbox(
                "1st Band",
                first_colors
            )

        with c2:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with c3:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        base = digits[b1] * 10 + digits[b2]

        tolerance = 20

        bands = [b1, b2, mult]

    # --------------------------------------------------------
    # 4 BAND
    # --------------------------------------------------------

    elif band_count == 4:

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            b1 = st.selectbox(
                "1st Band",
                first_colors
            )

        with c2:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with c3:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        with c4:
            tol = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base = digits[b1] * 10 + digits[b2]

        tolerance = tolerances[tol]

        bands = [b1, b2, mult, tol]

    # --------------------------------------------------------
    # 5 BAND
    # --------------------------------------------------------

    else:

        c1, c2, c3, c4, c5 = st.columns(5)

        with c1:
            b1 = st.selectbox(
                "1st Band",
                first_colors
            )

        with c2:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys())
            )

        with c3:
            b3 = st.selectbox(
                "3rd Band",
                list(digits.keys())
            )

        with c4:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys())
            )

        with c5:
            tol = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold")
            )

        base = (
            digits[b1] * 100
            + digits[b2] * 10
            + digits[b3]
        )

        tolerance = tolerances[tol]

        bands = [b1, b2, b3, mult, tol]


    # ========================================================
    # CALCULATION
    # ========================================================

    multiplier_value = multipliers[mult]

    resistance = base * multiplier_value

    minimum = resistance * (1 - tolerance / 100)

    maximum = resistance * (1 + tolerance / 100)


    # ========================================================
    # RESISTOR
    # ========================================================

    st.html(main_resistor(bands))


    # ========================================================
    # RESULT
    # ========================================================

    st.markdown("---")

    st.markdown(
        f"""
        <div style="
            background:rgba(25,135,84,0.15);
            border:1px solid rgba(25,200,120,0.30);
            border-radius:16px;
            padding:25px;
            text-align:center;
        ">

            <div style="
                color:#aeb7b2;
                font-size:13px;
                letter-spacing:2px;
                text-transform:uppercase;
            ">
                Calculated Resistance
            </div>

            <div style="
                color:white;
                font-size:42px;
                font-weight:800;
                margin:8px;
            ">
                {format_resistance(resistance)}
            </div>

            <div style="
                color:#9fe3bd;
                font-size:18px;
                font-weight:600;
            ">
                ±{tolerance:g}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CALCULATION BREAKDOWN
    # ========================================================

    st.markdown("### 🧮 Calculation Breakdown")

    st.code(
        f"""Significant digits : {base}
Multiplier          : × {multiplier_value:g}
Resistance          : {base} × {multiplier_value:g}
                    = {resistance:g} Ω
Tolerance           : ±{tolerance:g}%""",
        language="text"
    )


    # ========================================================
    # RANGE
    # ========================================================

    st.markdown("### 📏 Resistance Range")

    r1, r2, r3 = st.columns(3)

    with r1:
        st.metric(
            "Nominal",
            format_resistance(resistance)
        )

    with r2:
        st.metric(
            "Minimum",
            format_resistance(minimum)
        )

    with r3:
        st.metric(
            "Maximum",
            format_resistance(maximum)
        )


    # ========================================================
    # ACTIONS
    # ========================================================

    st.markdown("### 🔗 Share")

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
        f"""
        <a href="{whatsapp_url}"
           target="_blank"
           style="text-decoration:none;">

            <div style="
                background:#25D366;
                color:white;
                text-align:center;
                padding:12px;
                border-radius:10px;
                font-weight:700;
                font-size:16px;
            ">
                💬 Share on WhatsApp
            </div>

        </a>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# COLOR REFERENCE
# ============================================================

st.markdown("---")

st.markdown("### 📚 Resistor Color Reference")

reference = [
    ("Black", "0", "×10⁰", "—"),
    ("Brown", "1", "×10¹", "±1%"),
    ("Red", "2", "×10²", "±2%"),
    ("Orange", "3", "×10³", "—"),
    ("Yellow", "4", "×10⁴", "—"),
    ("Green", "5", "×10⁵", "±0.5%"),
    ("Blue", "6", "×10⁶", "±0.25%"),
    ("Violet", "7", "×10⁷", "±0.1%"),
    ("Gray", "8", "×10⁸", "±0.05%"),
    ("White", "9", "×10⁹", "—"),
    ("Gold", "—", "×10⁻¹", "±5%"),
    ("Silver", "—", "×10⁻²", "±10%")
]

cols = st.columns(4)

for col, title in zip(
    cols,
    ["Color", "Digit", "Multiplier", "Tolerance"]
):
    col.markdown(f"**{title}**")

for color, digit, multiplier, tolerance in reference:

    c1, c2, c3, c4 = st.columns(4)

    text_color = (
        "#111111"
        if color in ["White", "Yellow", "Gold", "Silver"]
        else "#FFFFFF"
    )

    with c1:
        st.markdown(
            f"""
            <div style="
                background:{COLOR_HEX[color]};
                color:{text_color};
                padding:7px;
                border-radius:7px;
                text-align:center;
                font-weight:700;
                margin-bottom:5px;
            ">
                {color}
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.write(digit)

    with c3:
        st.write(multiplier)

    with c4:
        st.write(tolerance)


# ============================================================
# ABOUT
# ============================================================

st.markdown("---")

a1, a2 = st.columns(2)

with a1:

    st.markdown("""
    ### 💡 About This Project

    A Python-based resistor color code decoder that supports
    **3-band, 4-band and 5-band resistors**.

    It calculates the nominal resistance, tolerance and
    acceptable resistance range while providing a dynamic
    visual representation of the resistor.
    """)


with a2:

    st.markdown("""
    ### 🛠 Technologies

    **Python**  
    **Streamlit**  
    Python Dictionaries  
    Conditional Logic  
    SVG Visualization  
    Responsive Web Interface
    """)


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#88899a;
        padding:15px;
        font-size:13px;
    ">
        Ω Resistor Color Code Decoder
        <br>
        Built with Python & Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
