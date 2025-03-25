import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Streamlit config
st.set_page_config(page_title="Supermarket Dashboard", layout="wide")
sns.set(style="whitegrid")

# Load data
df = pd.read_csv("supermarket_sales.csv")
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

df['total'] = df['unit_price'] * df['quantity']
df['time'] = pd.to_datetime(df['time'], format='%H:%M')
df['hour'] = df['time'].dt.hour

# Sidebar filters
branch = st.sidebar.selectbox("📍 Select Branch", df['branch'].unique())
filtered_df = df[df['branch'] == branch]

# ---------- TITLE ----------
st.markdown("<h1 style='text-align: center;'>🛍 Supermarket Sales Dashboard</h1>", unsafe_allow_html=True)
st.markdown("#### Get powerful sales and customer insights by branch", unsafe_allow_html=True)
st.markdown("---")

# ---------- KPI METRICS ----------
st.markdown("### 📌 Key Performance for Branch: " + branch)
kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("💵 Total Revenue", f"${filtered_df['total'].sum():,.2f}")
kpi2.metric("⭐ Avg. Rating", f"{filtered_df['rating'].mean():.2f}")
kpi3.metric("🧾 Total Transactions", f"{filtered_df.shape[0]}")
st.markdown("---")

# ---------- PRODUCT LINE REVENUE ----------
st.markdown("### 🛒 Revenue by Product Line")
prod_rev = filtered_df.groupby('product_line')['total'].sum().sort_values()
fig1, ax1 = plt.subplots()
sns.barplot(x=prod_rev.values, y=prod_rev.index, palette="Blues_d", ax=ax1)
ax1.set_xlabel("Revenue")
ax1.set_ylabel("Product Line")
st.pyplot(fig1)

# ---------- SALES BY HOUR ----------
st.markdown("### ⏰ Sales by Hour")
hour_rev = filtered_df.groupby('hour')['total'].sum()
fig2, ax2 = plt.subplots()
sns.lineplot(x=hour_rev.index, y=hour_rev.values, marker="o", color="darkorange", ax=ax2)
ax2.set_ylabel("Total Sales")
ax2.set_xlabel("Hour")
st.pyplot(fig2)

# ---------- PAYMENT PIE CHART ----------
st.markdown("### 💳 Revenue by Payment Type")
pay_rev = filtered_df.groupby('payment')['total'].sum()
fig3, ax3 = plt.subplots()
ax3.pie(pay_rev, labels=pay_rev.index, autopct='%1.1f%%', colors=sns.color_palette('Set2'), startangle=90)
ax3.set_title("Revenue Share by Payment Method")
st.pyplot(fig3)

# ---------- CUSTOMER TYPE VS GENDER ----------
st.markdown("### 👤 Avg Spend by Gender & Customer Type")
grouped = filtered_df.groupby(['gender', 'customer_type'])['total'].mean().unstack()
fig4, ax4 = plt.subplots()
grouped.plot(kind='bar', colormap='Accent', ax=ax4)
ax4.set_ylabel("Avg Spending")
st.pyplot(fig4)

# ---------- RATING VS SPENDING ----------
st.markdown("### ⭐ Customer Rating vs Total Spending")
fig5, ax5 = plt.subplots()
sns.scatterplot(data=filtered_df, x='rating', y='total', hue='gender', palette='cool', ax=ax5, alpha=0.7)
ax5.set_title("Do Higher Ratings Mean More Spending?")
st.pyplot(fig5)
