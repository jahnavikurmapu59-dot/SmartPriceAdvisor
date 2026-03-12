import streamlit as st
import joblib

# Load model and encoder
model = joblib.load("price_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

st.title("💬 Smart Price Advisor")

st.write("Enter the product name and its current price, and get a recommendation to Buy or Wait!")

# Input fields
product = st.text_input("Product Name")
price_input = st.text_input("Current Price")

if st.button("Get Recommendation"):
    if not product or not price_input:
        st.error("Please enter valid product name and price.")
    else:
        try:
            price = float(price_input)
            prediction = model.predict([[price]])
            label = label_encoder.inverse_transform(prediction)[0]
            st.success(f"Product: **{product}** | Price: **${price:.2f}** | Recommendation: **{label}**")
        except ValueError:
            st.error("Please enter a valid number for the price.")
