import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import database

# -----------------------------
# INIT DB TABLES
# -----------------------------
database.create_table()
database.create_user_table()

# -----------------------------
# SESSION STATE
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# -----------------------------
# LOGIN / SIGNUP
# -----------------------------
if not st.session_state.logged_in:

    st.title("🔐 Login / Signup")

    menu = ["Login", "Signup"]
    choice = st.selectbox("Select Option", menu)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            database.add_user(username, password)
            st.success("Account created! Please login.")

    elif choice == "Login":
        if st.button("Login"):
            user = database.login_user(username, password)
            if user:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid credentials")

# -----------------------------
# MAIN APP
# -----------------------------
if st.session_state.logged_in:

    # Sidebar
    st.sidebar.write(f"👤 Logged in as: {st.session_state.username}")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # Load model
    with open("models/revenue_model.pkl", "rb") as f:
        model = pickle.load(f)

    st.title("📊 AI Business Decision Simulator")

    # -----------------------------
    # CURRENT SCENARIO
    # -----------------------------
    st.subheader("📍 Current Business Scenario")

    price_current = st.number_input("Current Price ($)", value=10.0)
    marketing_current = st.number_input("Current Marketing ($)", value=1000.0)
    customers_current = st.number_input("Current Customers", value=100)

    current_input = np.array([[price_current, marketing_current, customers_current]])
    revenue_current = model.predict(current_input)[0]

    # -----------------------------
    # NEW SCENARIO
    # -----------------------------
    st.subheader("🚀 New Strategy Scenario")

    price_new = st.number_input("New Price ($)", value=12.0)
    marketing_new = st.number_input("New Marketing ($)", value=1500.0)
    customers_new = st.number_input("New Customers", value=120)

    if st.button("Compare Decisions"):

        new_input = np.array([[price_new, marketing_new, customers_new]])
        revenue_new = model.predict(new_input)[0]

        diff = revenue_new - revenue_current

        # Save to DB
        database.insert_data(
            st.session_state.username,
            price_current, marketing_current, customers_current,
            price_new, marketing_new, customers_new,
            revenue_current, revenue_new, diff
        )

        st.success(f"Predicted Revenue: ${revenue_new:.2f}")
        st.info(f"Change from current: ${diff:.2f}")

        # -----------------------------
        # IMPACT CHART
        # -----------------------------
        price_effect = price_new - price_current
        marketing_effect = marketing_new - marketing_current
        customer_effect = customers_new - customers_current

        fig = go.Figure(data=[
            go.Bar(
                x=["Price", "Marketing", "Customers"],
                y=[price_effect, marketing_effect, customer_effect]
            )
        ])

        st.plotly_chart(fig)
        st.info("This shows how each factor contributed to revenue change")

        # -----------------------------
        # AI INSIGHT
        # -----------------------------
        st.subheader("🧠 AI Insight")

        if diff > 0:
            st.write("Revenue increased due to improved strategy.")
        else:
            st.write("Revenue decreased. Consider adjusting strategy.")

    # -----------------------------
    # PRICE SENSITIVITY
    # -----------------------------
    st.subheader("📈 Price Sensitivity Analysis")

    prices = np.linspace(5, 20, 50)
    revenues = []

    for p in prices:
        input_data = np.array([[p, marketing_new, customers_new]])
        pred = model.predict(input_data)[0]
        revenues.append(pred)

    fig_price = go.Figure()
    fig_price.add_trace(go.Scatter(x=prices, y=revenues, mode='lines'))

    st.plotly_chart(fig_price)

    # -----------------------------
    # MARKETING ANALYSIS 🔥
    # -----------------------------
    st.subheader("📊 Marketing Spend Analysis")

    marketing_range = np.linspace(100, 5000, 50)
    revenues_marketing = []

    for m in marketing_range:
        input_data = np.array([[price_new, m, customers_new]])
        pred = model.predict(input_data)[0]
        revenues_marketing.append(pred)

    fig_marketing = go.Figure()
    fig_marketing.add_trace(go.Scatter(
        x=marketing_range,
        y=revenues_marketing,
        mode='lines'
    ))

    st.plotly_chart(fig_marketing)

    # -----------------------------
# 🔥 STRATEGY RECOMMENDATION ENGINE
# -----------------------------
    st.subheader("🤖 AI Strategy Recommendation")

if st.button("🎯 Generate Best Strategy"):

    best_revenue = -1
    best_price = 0
    best_marketing = 0
    best_customers = 0

    # Try multiple combinations
    for _ in range(100):

        test_price = random.uniform(5, 20)
        test_marketing = random.uniform(100, 5000)
        test_customers = random.randint(50, 300)

        input_data = np.array([[test_price, test_marketing, test_customers]])
        pred_revenue = model.predict(input_data)[0]

        if pred_revenue > best_revenue:
            best_revenue = pred_revenue
            best_price = test_price
            best_marketing = test_marketing
            best_customers = test_customers

    # Show results
    st.success("🏆 Recommended Strategy")

    st.write(f"💰 Expected Revenue: ${best_revenue:.2f}")
    st.write(f"📌 Optimal Price: {best_price:.2f}")
    st.write(f"📢 Optimal Marketing: {best_marketing:.2f}")
    st.write(f"👥 Target Customers: {best_customers}")

    st.subheader("🧠 Why this strategy?")
    st.info(
        "This strategy maximizes predicted revenue based on your model by balancing pricing, marketing investment, and customer volume."
    )
    # -----------------------------
    # AUTO SIMULATION
    # -----------------------------
    if st.button("⚡ Run Auto Simulation (10 Scenarios)"):

        for _ in range(10):
            price = random.uniform(5, 20)
            marketing = random.uniform(100, 5000)
            customers = random.randint(50, 300)

            input_data = np.array([[price, marketing, customers]])
            revenue = model.predict(input_data)[0]

            database.insert_data(
                st.session_state.username,
                price, marketing, customers,
                price, marketing, customers,
                revenue, revenue, 0
            )

        st.success("✅ 10 simulations added!")

    # -----------------------------
    # HISTORY
    # -----------------------------
    st.subheader("📜 Scenario History")

    rows = database.get_data(st.session_state.username)

    if rows:
        df = pd.DataFrame(rows, columns=[
            "ID",
            "Username",
            "Price_Current", "Marketing_Current", "Customers_Current",
            "Price_New", "Marketing_New", "Customers_New",
            "Revenue_Current", "Revenue_New", "Difference"
        ])

        st.dataframe(df)

        # -----------------------------
        # INSIGHTS
        # -----------------------------
        st.subheader("📊 Insights Dashboard")

        st.write(f"🔥 Best Revenue: ${df['Revenue_New'].max():.2f}")
        st.write(f"⚠️ Worst Revenue: ${df['Revenue_New'].min():.2f}")
        st.write(f"📊 Average Revenue: ${df['Revenue_New'].mean():.2f}")

        fig2 = px.line(df, y="Revenue_New", title="Revenue Trend")
        st.plotly_chart(fig2)

        # -----------------------------
        # BEST STRATEGY
        # -----------------------------
        best_row = df.loc[df["Revenue_New"].idxmax()]

        st.subheader("🏆 Best Strategy Recommendation")

        st.write(f"💰 Expected Revenue: ${best_row['Revenue_New']:.2f}")
        st.write(f"📌 Optimal Price: {best_row['Price_New']}")
        st.write(f"📢 Optimal Marketing: {best_row['Marketing_New']}")
        st.write(f"👥 Target Customers: {best_row['Customers_New']}")

        st.subheader("🧠 Why this works")
        st.info("Higher marketing and customer growth contributed to better revenue.")