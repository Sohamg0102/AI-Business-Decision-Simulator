import streamlit as st

st.set_page_config(page_title="Decision Simulator", layout="centered")

st.title("📊 AI Business Decision Simulator")

st.markdown("---")

st.subheader("Enter Business Parameters")

# Inputs
price = st.number_input("Product Price ($)", min_value=1.0, value=10.0)
marketing = st.number_input("Marketing Spend ($)", min_value=0.0, value=1000.0)
customers = st.number_input("Number of Customers", min_value=1, value=100)

# Simulate button
if st.button("Simulate Decision"):

    # Dummy logic (temporary)
    revenue = price * customers + (marketing * 0.5)

    if revenue > 5000:
        risk = "Low"
    elif revenue > 2000:
        risk = "Medium"
    else:
        risk = "High"

    # Output
    st.success("Simulation Complete!")
    st.subheader("📈 Results")
    st.write(f"Predicted Revenue: ${revenue:.2f}")
    st.write(f"Risk Level: {risk}")