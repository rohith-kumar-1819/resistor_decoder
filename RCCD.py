import streamlit as st
import urllib.parse


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Python Resistor Decoder",
    page_icon="Ω",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# 2. CUSTOM CSS
# ============================================================

st.markdown("""
<style>

/* ---------- Main Application Background ---------- */

.stApp {
    background:
        radial-gradient(circle at top left, rgba(65, 88, 208, 0.35), transparent 35%),
        radial-gradient(circle at bottom right, rgba(200, 80, 192, 0.30), transparent 35%),
        linear-gradient(135deg, #10111f 0%, #171426 45%, #211728 100%);
    background-attachment: fixed;
}


/* ---------- Main Container ---------- */

.block-container {
    max-width: 1400px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}


/* ---------- Typography ---------- */

h1, h2, h3, h4, p, label {
    color: #ffffff !important;
}

h1 {
    font-size: 2.7rem !important;
    font-weight: 800 !important;
    letter-spacing: -1px;
}

h2 {
    font-weight: 750 !important;
}

h3 {
    font-weight: 700 !important;
}

p {
    color: #d7d7e2 !important;
}


/* ---------- Glass Cards ---------- */

.glass-card {
    background: rgba(25, 25, 38, 0.88);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.28);
    margin-bottom: 20px;
}


/* ---------- Header ---------- */

.hero {
    text-align: center;
    padding: 20px 10px 10px 10px;
}

.hero-title {
    font-size: 2.8rem;
    font-weight: 850;
    color: #ffffff;
    margin-bottom: 8px;
}

.hero-subtitle {
    color: #c8c8d8;
    font-size: 1.05rem;
    margin-bottom: 5px;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.14);
    border-radius: 30px;
    padding: 7px 15px;
    font-size: 0.82rem;
    color: #eeeeff;
    margin-top: 10px;
}


/* ---------- Section Titles ---------- */

.section-title {
    color: #ffffff;
    font-size: 1.15rem;
    font-weight: 750;
    margin-bottom: 10px;
}


/* ---------- Select Boxes ---------- */

div[data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.07) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 10px !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}


/* ---------- Radio Buttons ---------- */

.stRadio label {
    color: #ffffff !important;
}


/* ---------- Result Card ---------- */

.result-card {
    background: linear-gradient(
        135deg,
        rgba(25, 135, 84, 0.18),
        rgba(25, 25, 38, 0.95)
    );
    border: 1px solid rgba(25, 200, 120, 0.30);
    border-radius: 18px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0,0,0,0.20);
}

.result-label {
    color: #b9c2ca;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.result-value {
    color: #ffffff;
    font-size: 2.6rem;
    font-weight: 850;
    margin: 8px 0;
}

.result-tolerance {
    color: #9fe3bd;
    font-size: 1.1rem;
    font-weight: 650;
}


/* ---------- Calculation Card ---------- */

.calculation-card {
    background: rgba(255, 255, 255, 0.045);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 15px;
    padding: 20px;
    margin-top: 15px;
}

.calculation-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 750;
    margin-bottom: 10px;
}

.calculation-text {
    color: #d8d8e5;
    font-family: monospace;
    font-size: 0.95rem;
    line-height: 1.8;
}


/* ---------- Info Cards ---------- */

.info-card {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 15px;
    padding: 18px;
    height: 100%;
}

.info-number {
    font-size: 1.4rem;
    font-weight: 800;
    color: #ffffff;
}

.info-label {
    font-size: 0.82rem;
    color: #aeb0c0;
}


/* ---------- Decorative Resistor ---------- */

.decorative-title {
    color: #ffffff;
    font-weight: 750;
    text-align: center;
    margin-bottom: 15px;
}


/* ---------- Buttons ---------- */

.stButton > button {
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.15);
    font-weight: 700;
    min-height: 44px;
}


/* ---------- Divider ---------- */

hr {
    border-color: rgba(255,255,255,0.10) !important;
}


/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #8f90a0;
    font-size: 0.82rem;
    padding: 25px 0 5px 0;
}


/* ---------- Mobile ---------- */

@media (max-width: 900px) {

    .hero-title {
        font-size: 2.1rem;
    }

    h1 {
        font-size: 2.1rem !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. RESISTOR DATA
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
# 4. HELPER FUNCTIONS
# ============================================================

def format_resistance(value):
    """Convert resistance into a readable engineering format."""

    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f} GΩ"

    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f} MΩ"

    elif value >= 1_000:
        return f"{value / 1_000:.2f} kΩ"

    else:
        return f"{value:g} Ω"


def deco_resistor(c1, c2, c3, c4):
    """Generate a decorative SVG resistor."""

    return f"""
    <div style="text-align:center; margin:25px 0;">
        <svg width="190" height="70"
             viewBox="0 0 190 70"
             xmlns="http://www.w3.org/2000/svg">

            <line x1="5" y1="35" x2="35" y2="35"
                  stroke="#FFFFFF" stroke-width="4"/>

            <line x1="155" y1="35" x2="185" y2="35"
                  stroke="#FFFFFF" stroke-width="4"/>

            <rect x="35" y="15"
                  width="120"
                  height="40"
                  rx="20"
                  fill="#D2B48C"
                  stroke="#555"
                  stroke-width="2"/>

            <rect x="65" y="15"
                  width="7"
                  height="40"
                  fill="{c1}"/>

            <rect x="82" y="15"
                  width="7"
                  height="40"
                  fill="{c2}"/>

            <rect x="99" y="15"
                  width="7"
                  height="40"
                  fill="{c3}"/>

            <rect x="125" y="15"
                  width="7"
                  height="40"
                  fill="{c4}"/>

        </svg>
    </div>
    """


def resistor_svg(bands):
    """Create the main dynamic resistor graphic."""

    svg_bands = ""

    start_x = 130
    spacing = 35

    for i, color in enumerate(bands):

        hex_code = COLOR_HEX.get(color, "#D3D3D3")

        x_pos = start_x + (i * spacing)

        if i == len(bands) - 1 and len(bands) > 3:
            x_pos += 20

        svg_bands += f"""
        <rect
            x="{x_pos}"
            y="30"
            width="13"
            height="60"
            fill="{hex_code}"
            stroke="#222222"
            stroke-width="1.5"
        />
        """

    return f"""
    <div style="text-align:center; margin:25px 0;">

        <svg
            width="460"
            height="120"
            viewBox="0 0 460 120"
            xmlns="http://www.w3.org/2000/svg"
        >

            <!-- Left wire -->
            <line
                x1="10"
                y1="60"
                x2="90"
                y2="60"
                stroke="#FFFFFF"
                stroke-width="7"
            />

            <!-- Right wire -->
            <line
                x1="350"
                y1="60"
                x2="450"
                y2="60"
                stroke="#FFFFFF"
                stroke-width="7"
            />

            <!-- Resistor body -->
            <path
                d="
                M 90 60
                Q 100 30 120 30
                L 320 30
                Q 340 30 350 60
                Q 340 90 320 90
                L 120 90
                Q 100 90 90 60
                Z
                "
                fill="#D2B48C"
                stroke="#333333"
                stroke-width="3"
            />

            {svg_bands}

        </svg>

    </div>
    """


def reset_app():
    """Reset all widget values."""

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    st.rerun()


# ============================================================
# 5. HEADER
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-title">
        Ω Resistor Color Code Decoder
    </div>

    <div class="hero-subtitle">
        Decode resistor values, multipliers and tolerances instantly.
    </div>

    <div class="badge">
        Python • Streamlit • Electronics
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# 6. MAIN THREE-COLUMN LAYOUT
# ============================================================

left_col, center_col, right_col = st.columns(
    [1, 5, 1],
    gap="large"
)


# ============================================================
# 7. LEFT DECORATIVE COLUMN
# ============================================================

with left_col:

    st.markdown(
        '<div class="decorative-title">⚡ Lab Kit</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#FF0000",
            "#FF0000",
            "#8B4513",
            "#FFD700"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#8B4513",
            "#000000",
            "#FFA500",
            "#C0C0C0"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#0000FF",
            "#8A2BE2",
            "#008000",
            "#FFD700"
        ),
        unsafe_allow_html=True
    )


# ============================================================
# 8. RIGHT DECORATIVE COLUMN
# ============================================================

with right_col:

    st.markdown(
        '<div class="decorative-title">🎨 Colors</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#0000FF",
            "#FFA500",
            "#8B4513",
            "#FFD700"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#8A2BE2",
            "#008000",
            "#FF0000",
            "#C0C0C0"
        ),
        unsafe_allow_html=True
    )

    st.markdown(
        deco_resistor(
            "#FFFF00",
            "#000000",
            "#FF0000",
            "#FFD700"
        ),
        unsafe_allow_html=True
    )


# ============================================================
# 9. CENTER APPLICATION
# ============================================================

with center_col:

    # --------------------------------------------------------
    # Band Selection
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">🔧 Resistor Configuration</div>',
        unsafe_allow_html=True
    )

    band_count = st.radio(
        "Select Number of Bands",
        [3, 4, 5],
        horizontal=True,
        format_func=lambda x: f"{x}-Band",
        key="band_count"
    )


    # --------------------------------------------------------
    # Valid first-band colors
    # Black is not used as first significant digit.
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


    # --------------------------------------------------------
    # Band Inputs
    # --------------------------------------------------------

    if band_count == 3:

        cols = st.columns(3)

        with cols[0]:
            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="b1"
            )

        with cols[1]:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="b2"
            )

        with cols[2]:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="mult"
            )

        base = digits[b1] * 10 + digits[b2]

        tol_val = 20

        bands = [
            b1,
            b2,
            mult
        ]

        tolerance_name = "None specified (3-band standard: ±20%)"


    elif band_count == 4:

        cols = st.columns(4)

        with cols[0]:
            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="b1"
            )

        with cols[1]:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="b2"
            )

        with cols[2]:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="mult"
            )

        with cols[3]:
            tol = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold"),
                key="tol"
            )

        base = digits[b1] * 10 + digits[b2]

        tol_val = tolerances[tol]

        bands = [
            b1,
            b2,
            mult,
            tol
        ]

        tolerance_name = tol


    else:

        cols = st.columns(5)

        with cols[0]:
            b1 = st.selectbox(
                "1st Band",
                first_band_colors,
                key="b1"
            )

        with cols[1]:
            b2 = st.selectbox(
                "2nd Band",
                list(digits.keys()),
                key="b2"
            )

        with cols[2]:
            b3 = st.selectbox(
                "3rd Band",
                list(digits.keys()),
                key="b3"
            )

        with cols[3]:
            mult = st.selectbox(
                "Multiplier",
                list(multipliers.keys()),
                key="mult"
            )

        with cols[4]:
            tol = st.selectbox(
                "Tolerance",
                list(tolerances.keys()),
                index=list(tolerances.keys()).index("Gold"),
                key="tol"
            )

        base = (
            digits[b1] * 100
            + digits[b2] * 10
            + digits[b3]
        )

        tol_val = tolerances[tol]

        bands = [
            b1,
            b2,
            b3,
            mult,
            tol
        ]

        tolerance_name = tol


    # --------------------------------------------------------
    # Calculate Resistance
    # --------------------------------------------------------

    multiplier_value = multipliers[mult]

    final_res = base * multiplier_value


    # ========================================================
    # 10. DYNAMIC RESISTOR
    # ========================================================

    st.markdown(
        resistor_svg(bands),
        unsafe_allow_html=True
    )


    # ========================================================
    # 11. RESULT
    # ========================================================

    formatted_resistance = format_resistance(final_res)

    minimum_resistance = final_res * (1 - tol_val / 100)

    maximum_resistance = final_res * (1 + tol_val / 100)


    st.markdown(f"""
    <div class="result-card">

        <div class="result-label">
            Calculated Resistance
        </div>

        <div class="result-value">
            {formatted_resistance}
        </div>

        <div class="result-tolerance">
            ±{tol_val:g}%
        </div>

    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # 12. CALCULATION BREAKDOWN
    # ========================================================

    st.markdown(f"""
    <div class="calculation-card">

        <div class="calculation-title">
            🧮 Calculation Breakdown
        </div>

        <div class="calculation-text">

            Significant digits:
            <b>{base}</b>
            <br>

            Multiplier:
            <b>× {multiplier_value:g}</b>
            <br>

            Resistance:
            <b>{base} × {multiplier_value:g}
            = {final_res:g} Ω</b>
            <br>

            Tolerance:
            <b>±{tol_val:g}%</b>

        </div>

    </div>
    """, unsafe_allow_html=True)


    # ========================================================
    # 13. RESISTANCE RANGE
    # ========================================================

    st.markdown("### 📏 Resistance Range")

    range_cols = st.columns(3)

    with range_cols[0]:

        st.markdown(f"""
        <div class="info-card">

            <div class="info-label">
                NOMINAL
            </div>

            <div class="info-number">
                {formatted_resistance}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with range_cols[1]:

        st.markdown(f"""
        <div class="info-card">

            <div class="info-label">
                MINIMUM
            </div>

            <div class="info-number">
                {format_resistance(minimum_resistance)}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with range_cols[2]:

        st.markdown(f"""
        <div class="info-card">

            <div class="info-label">
                MAXIMUM
            </div>

            <div class="info-number">
                {format_resistance(maximum_resistance)}
            </div>

        </div>
        """, unsafe_allow_html=True)


    # ========================================================
    # 14. RESET + WHATSAPP
    # ========================================================

    st.markdown("### 🔄 Actions")

    action_cols = st.columns(2)

    with action_cols[0]:

        if st.button(
            "↻ Reset Decoder",
            use_container_width=True
        ):
            reset_app()


    with action_cols[1]:

        app_url = (
            "https://resistor-color-code-decoder.streamlit.app"
        )

        msg = (
            "Check out my Python Resistor Color Code Decoder app: "
            + app_url
        )

        whatsapp_link = (
            "https://api.whatsapp.com/send?text="
            + urllib.parse.quote(msg)
        )

        st.markdown(
            f"""
            <a href="{whatsapp_link}" target="_blank"
               style="text-decoration:none;">

                <div style="
                    background:#25D366;
                    color:white;
                    padding:11px;
                    border-radius:10px;
                    text-align:center;
                    font-weight:700;
                    font-size:16px;
                    margin-top:0px;
                ">

                    💬 Share on WhatsApp

                </div>

            </a>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 15. COLOR REFERENCE
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="section-title">📚 Resistor Color Reference</div>',
    unsafe_allow_html=True
)


reference_data = [
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

headers = [
    "Color",
    "Digit",
    "Multiplier",
    "Tolerance"
]

for i, header in enumerate(headers):

    with cols[i]:
        st.markdown(
            f"**{header}**"
        )


for color, digit, multiplier, tolerance in reference_data:

    cols = st.columns(4)

    with cols[0]:
        hex_color = COLOR_HEX[color]

        # Choose readable text for dark/light colors
        text_color = "#000000" if color in ["White", "Yellow", "Gold", "Silver"] else "#FFFFFF"

        st.markdown(
            f"""
            <div style="
                background:{hex_color};
                color:{text_color};
                padding:7px 12px;
                border-radius:7px;
                font-weight:700;
                text-align:center;
                margin-bottom:5px;
            ">
                {color}
            </div>
            """,
            unsafe_allow_html=True
        )

    with cols[1]:
        st.write(digit)

    with cols[2]:
        st.write(multiplier)

    with cols[3]:
        st.write(tolerance)


# ============================================================
# 16. ABOUT PROJECT
# ============================================================

st.markdown("---")

about_col1, about_col2 = st.columns(2)

with about_col1:

    st.markdown("""
    <div class="glass-card">

        <h3>💡 About This Tool</h3>

        <p>
        This Python-based application decodes standard resistor
        color bands and calculates the corresponding resistance,
        multiplier and tolerance.
        </p>

        <p>
        It supports 3-band, 4-band and 5-band resistor configurations
        with a dynamic visual resistor representation.
        </p>

    </div>
    """, unsafe_allow_html=True)


with about_col2:

    st.markdown("""
    <div class="glass-card">

        <h3>🛠 Technologies Used</h3>

        <p>
        <b>Python</b><br>
        <b>Streamlit</b><br>
        Python Dictionaries<br>
        Conditional Logic<br>
        SVG Visualization<br>
        Responsive Web UI
        </p>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# 17. FOOTER
# ============================================================

st.markdown("""
<div class="footer">

    Ω Resistor Color Code Decoder
    <br>
    Built with Python & Streamlit • Electronics Utility

</div>
""", unsafe_allow_html=True)
