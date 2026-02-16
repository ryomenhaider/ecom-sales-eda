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


st.header('Charts')

st.subheader("Sales by Product Category")
sales_by_category = df.groupby('productcategory')['sales'].sum().sort_values(ascending=False)
st.bar_chart(sales_by_category)

st.subheader("Sales Over Time")
sales_over_time = df.groupby('transactiondate')['sales'].sum()
st.line_chart(sales_over_time)

st.subheader("Top 10 Products by Sales")
top_products = df.groupby('productid')['sales'].sum().sort_values(ascending=False).head(10)
st.bar_chart(top_products)

st.subheader("Customer Demographics")
age_distribution = df['customerage'].dropna()
st.bar_chart(age_distribution.value_counts().sort_index())

st.subheader("Sales by Region")
sales_by_region = df.groupby('customerregion')['sales'].sum().sort_values(ascending=False)
st.bar_chart(sales_by_region)

