import streamlit as st

# 1. Python Dictionaries (Matching your resume description!)
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

# 2. Formatting Function
def format_resistance(value):
    if value >= 1_000_000_000: return f"{value / 1_000_000_000:.2f} GΩ"
    elif value >= 1_000_000: return f"{value / 1_000_000:.2f} MΩ"
    elif value >= 1000: return f"{value / 1000:.2f} kΩ"
    else: return f"{value:g} Ω"

# 3. Web UI Setup
st.set_page_config(page_title="Python Resistor Decoder", page_icon="Ω")
st.title(" Ω Resistor Color code decoder")
st.write("A Python-based utility using dictionaries and conditional logic.")

# 4. User Inputs (Radio buttons and dropdowns)
band_count = st.radio("Select Number of Bands:", [3, 4, 5], horizontal=True)

# Create layout columns based on how many bands the user selected
cols = st.columns(band_count)

with cols[0]: b1 = st.selectbox("1st Band", list(digits.keys()))
with cols[1]: b2 = st.selectbox("2nd Band", list(digits.keys()))

if band_count == 5:
    with cols[2]: b3 = st.selectbox("3rd Band", list(digits.keys()))
    with cols[3]: mult = st.selectbox("Multiplier", list(multipliers.keys()))
    with cols[4]: tol = st.selectbox("Tolerance", list(tolerances.keys()))
else:
    with cols[2]: mult = st.selectbox("Multiplier", list(multipliers.keys()))
    if band_count == 4:
        with cols[3]: tol = st.selectbox("Tolerance", list(tolerances.keys()))

# 5. Calculation (Python Conditional Logic)
if band_count == 5:
    base = (digits[b1] * 100) + (digits[b2] * 10) + digits[b3]
    tol_val = tolerances[tol]
else:
    base = (digits[b1] * 10) + digits[b2]
    tol_val = tolerances[tol] if band_count == 4 else 20

final_res = base * multipliers[mult]

# 6. Display Results
st.divider()
st.success(f"### Resistance: **{format_resistance(final_res)}**")
st.info(f"### Tolerance: **±{tol_val}%**")
