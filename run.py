import streamlit as st
import pandas as pd

from get_customer_advice import get_customer_advice

def display_business_data(data):
    formatted_business_data = pd.DataFrame(
        {
            "Business ID": [data["bus_id"].iloc[0]],
            "Business Type": [data["business_type"].iloc[0]],
            "Industry": [data["industry"].iloc[0]],
            "Address": [data["address"].iloc[0]],
            "Owner Name": [data["owner_name"].iloc[0]],
            "Number of Employees": [data["employees"].iloc[0]],
            "Credit Score": [data["credit_score"].iloc[0]],
        }
    ).T
    st.write(formatted_business_data.to_html(header=False), unsafe_allow_html=True)
    return formatted_business_data

def display_product_data(data):
    formatted_product_data = pd.DataFrame(
        {
            "Product": [data["product"].iloc[0]],
            "Account Number": [data["account_number"].iloc[0]],
            "Balance": [data["balance"].iloc[0]],
            "Rate": [data["rate"].iloc[0]],
            "Term": [data["term"].iloc[0]],
        }
    ).T
    st.write(formatted_product_data.to_html(header=False), unsafe_allow_html=True)

def display_transaction_data(data):
    formated_transactions = pd.DataFrame(
        {
            "Date": data["date"],
            "Transaction": data["transaction_type"],
            "Amount": data["amount"],
        }
    ).sort_values("Date").reset_index(drop=True)
    st.write(formated_transactions.to_html(), unsafe_allow_html=True)
    return formated_transactions


if __name__=="__main__":
    st.set_page_config(layout="wide")

    business_data = pd.read_csv("data/customer_data.csv", dtype={'bus_id': str})
    product_data = pd.read_csv("data/product_data.csv", dtype={'bus_id': str})
    transaction_data = pd.read_csv("data/transaction_data.csv", dtype={'bus_id': str})

    st.sidebar.header("Select Business")
    business_options = business_data["business_name"].unique()
    selected_business = st.sidebar.selectbox("", business_options, label_visibility="collapsed")

    selected_business_data = business_data[business_data["business_name"] == selected_business]
    selected_products = product_data[product_data["bus_id"] == selected_business_data["bus_id"].iloc[0]]["product"]


    with st.container():
        st.sidebar.header("Select Product")
        selected_product = st.sidebar.selectbox("", selected_products, label_visibility="collapsed")

        col1, col2 = st.columns([0.5, 0.5])
        with col1:
            st.subheader(selected_business, divider="blue")
            formatted_business_data = display_business_data(selected_business_data)

        with col2:
            st.subheader(f"Product Details: {selected_product}", divider="blue")
            display_product_data(
                product_data[
                    (product_data["bus_id"] == selected_business_data["bus_id"].iloc[0]) &
                    (product_data["product"] == selected_product)
                ]
            )

        st.subheader("Last 10 transactions", divider="blue")
        formated_transactions = display_transaction_data(transaction_data[transaction_data["bus_id"] == selected_business_data["bus_id"].iloc[0]])

        if st.button(
                "Get Customer Advice",
                on_click=get_customer_advice,
                args=(
                    formatted_business_data,
                    product_data[product_data["bus_id"] == selected_business_data["bus_id"].iloc[0]],
                    formated_transactions,
                )
            ):
            st.write(st.session_state['customer_advice'])