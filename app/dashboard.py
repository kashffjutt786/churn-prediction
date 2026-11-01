import os
import sys
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT / "src"))

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Churn Prediction", page_icon="📉", layout="wide")
st.title("📉 Customer Churn Prediction")

tab1, tab2 = st.tabs(["Predict", "Risk Overview"])

# ---------------- Tab 1: Single customer prediction ----------------
with tab1:
    st.subheader("Customer ki details daalein")

    with st.form("customer_form"):
        c1, c2, c3 = st.columns(3)

        with c1:
            gender = st.selectbox("Gender", ["Female", "Male"])
            senior = st.selectbox("Senior citizen", [0, 1])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["No", "Yes"])
            tenure = st.slider("Tenure (months)", 0, 72, 5)
            phone = st.selectbox("Phone service", ["Yes", "No"])
            multi = st.selectbox("Multiple lines", ["No", "Yes", "No phone service"])

        with c2:
            internet = st.selectbox("Internet service", ["Fiber optic", "DSL", "No"])
            sec = st.selectbox("Online security", ["No", "Yes", "No internet service"])
            backup = st.selectbox("Online backup", ["No", "Yes", "No internet service"])
            protect = st.selectbox("Device protection", ["No", "Yes", "No internet service"])
            support = st.selectbox("Tech support", ["No", "Yes", "No internet service"])
            tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
            movies = st.selectbox("Streaming movies", ["Yes", "No", "No internet service"])

        with c3:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            paperless = st.selectbox("Paperless billing", ["Yes", "No"])
            payment = st.selectbox("Payment method", [
                "Electronic check", "Mailed check",
                "Bank transfer (automatic)", "Credit card (automatic)"])
            monthly = st.number_input("Monthly charges", 0.0, 200.0, 85.5)
            total = st.number_input("Total charges", 0.0, 10000.0, 420.0)

        submitted = st.form_submit_button("Predict churn")

    if submitted:
        payload = {
            "gender": gender, "senior_citizen": senior, "partner": partner,
            "dependents": dependents, "tenure_months": tenure,
            "phone_service": phone, "multiple_lines": multi,
            "internet_service": internet, "online_security": sec,
            "online_backup": backup, "device_protection": protect,
            "tech_support": support, "streaming_tv": tv,
            "streaming_movies": movies, "contract": contract,
            "paperless_billing": paperless, "payment_method": payment,
            "monthly_charges": monthly, "total_charges": total,
        }
        try:
            r = requests.post(f"{API_URL}/predict", json=payload, timeout=90)
            r.raise_for_status()
            res = r.json()

            prob, risk = res["churn_probability"], res["risk_level"]
            m1, m2 = st.columns(2)
            m1.metric("Churn probability", f"{prob * 100:.1f}%")
            m2.metric("Risk level", risk)
            st.progress(min(prob, 1.0))

            if risk == "High":
                st.error("High risk: is customer ko retention offer dein (discount ya contract upgrade).")
            elif risk == "Medium":
                st.warning("Medium risk: customer par nazar rakhein.")
            else:
                st.success("Low risk: customer stable hai.")
        except Exception as e:
            st.error(f"API se connection nahi hua. Kya API chal rahi hai? ({e})")

# ---------------- Tab 2: Overview ----------------
with tab2:
    st.subheader("Risk overview")

    @st.cache_data(ttl=300)
    def load_overview():
        try:
            from db import get_engine
            eng = get_engine()
            df = pd.read_sql(
                "SELECT p.customer_id, p.churn_probability, p.risk_level, "
                "b.contract, b.monthly_charges "
                "FROM dbo.churn_predictions p "
                "JOIN dbo.billing b ON b.customer_id = p.customer_id", eng)
            source = "SQL Server"
        except Exception:
            df = pd.read_csv(ROOT / "data" / "predictions_snapshot.csv")
            source = "snapshot CSV (cloud demo)"

        risk = df.groupby("risk_level").size().rename("customers").reset_index()
        by_contract = (df.groupby("contract")["churn_probability"].mean() * 100).round(2) \
            .rename("avg_churn_pct").reset_index()
        top = df[df["risk_level"] == "High"].nlargest(20, "churn_probability")
        return risk, by_contract, top, source

    try:
        risk_df, contract_df, top_df, source = load_overview()
        st.caption(f"Data source: {source}")

        left, right = st.columns(2)
        with left:
            st.markdown("**Risk level ke hisaab se customers**")
            st.bar_chart(risk_df.set_index("risk_level"))
        with right:
            st.markdown("**Contract ke hisaab se average churn probability (%)**")
            st.bar_chart(contract_df.set_index("contract"))

        st.markdown("**Top 20 high-risk customers**")
        st.dataframe(top_df, use_container_width=True)
    except Exception as e:
        st.error(f"Data nahi mila: {e}")