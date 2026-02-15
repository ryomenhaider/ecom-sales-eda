import pandas as pd
import streamlit as st
import numpy as np

def load_data():
    df = pd.read_csv('/run/media/alpha/Files/Data_Analytics/ECom_Data_analysis/data/data.csv')
    return df


df = load_data()

st.title("Ecommerce Sales Dashboard")
st.header("Data Overview")
st.write("This dashboard provides insights into the ecommerce sales data, including customer demographics, product performance, and sales trends.") 

st.subheader("Sample Data")
st.dataframe(df.head())
df['sales'] = df['price'] * df['quantity']
st.subheader("KPIs")
st.write(f"Total Sales: ${df['sales'].sum():,.2f}")
st.write(f"Total Orders: {df['transactionid'].nunique()}")
st.write(f"Average Order Value: ${df.groupby('transactionid' )['sales'].sum().mean():.2f}")
st.write(f"Revenue by Category: {df.groupby('productcategory')['sales'].sum().to_dict()}")


st.subheader("revenue Metrics")

revenue_growth_rate = (df.groupby('transactiondate')['sales'].sum().pct_change() * 100).mean()
revenue_per_customer = df.groupby('customerid')['sales'].sum().mean()

st.metric(label="Average Revenue Growth Rate", value=f"{revenue_growth_rate:.2f}%")
st.metric(label="Average Revenue per Customer", value=f"${revenue_per_customer:.2f}")   

st.subheader("Customer Metrics")

repeat_customers = df.groupby('customerid').size()
rcr = (repeat_customers[repeat_customers > 1].count() / df['customerid'].nunique()) * 100
st.metric(label="Repeat Customer Rate", value=f"{rcr:.2f}%")


customers_start = df[df['transactiondate'] < '2026-01-01']['customerid'].unique()
customers_end = df[df['transactiondate'] >= '2026-01-01']['customerid'].unique()
retention_rate = (len(np.intersect1d(customers_start, customers_end)) / len(customers_start)) * 100
st.metric(label="Customer Retention Rate", value=f"{retention_rate:.2f}%")

