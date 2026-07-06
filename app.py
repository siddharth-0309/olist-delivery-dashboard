import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Olist Delivery Performance Dashboard", layout="wide")

conn = sqlite3.connect('olist.db', check_same_thread=False)

st.title("📦 Olist E-Commerce: Delivery Performance & Customer Satisfaction")
st.markdown("Analyzing how delivery delays impact customer satisfaction, seller performance, and regional risk.")

col1, col2, col3, col4 = st.columns(4)

kpi_query = """
SELECT 
    COUNT(*) AS total_orders,
    ROUND(AVG(review_score), 2) AS avg_review
FROM orders o
JOIN order_review r ON o.order_id = r.order_id
WHERE o.order_delivered_customer_date IS NOT NULL;
"""
kpi = pd.read_sql_query(kpi_query, conn)

col1.metric("Total Delivered Orders", f"{kpi['total_orders'][0]:,}")
col2.metric("Avg Review Score", kpi['avg_review'][0])

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Delay vs Satisfaction", "Seller Performance",
    "Regional Risk", "Category Risk", "Payment Methods"
])

with tab1:
    st.subheader("Delivery Delay Impact on Review Score")
    q1 = """
    SELECT
        CASE
            WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) <= 0 THEN 'On-Time'
            WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) BETWEEN 1 AND 3 THEN '1-3 Days Late'
            WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) BETWEEN 4 AND 7 THEN '4-7 Days Late'
            ELSE '7+ Days Late'
        END AS delay_bucket,
        COUNT(*) AS total_orders,
        ROUND(AVG(r.review_score), 2) AS avg_review_score
    FROM orders o
    JOIN order_review r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY delay_bucket
    ORDER BY avg_review_score DESC;
    """
    df1 = pd.read_sql_query(q1, conn)
    fig1 = px.bar(df1, x='delay_bucket', y='avg_review_score',
                  color='avg_review_score', color_continuous_scale='RdYlGn')
    st.plotly_chart(fig1, width='stretch')

with tab2:
    st.subheader("Top & Worst Performing Sellers")
    q2 = """
    WITH seller_stats AS (
        SELECT
            oi.seller_id,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(CASE
                    WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) > 0
                    THEN 1 ELSE 0
                END) AS late_orders,
            ROUND(AVG(r.review_score), 2) AS avg_review_score
        FROM order_items oi
        JOIN orders o ON oi.order_id = o.order_id
        JOIN order_review r ON o.order_id = r.order_id
        WHERE o.order_delivered_customer_date IS NOT NULL
        GROUP BY oi.seller_id
        HAVING total_orders >= 10
    )
    SELECT *,
           ROUND(1.0 - (late_orders * 1.0 / total_orders), 3) AS on_time_rate,
           RANK() OVER (ORDER BY (1.0 - (late_orders * 1.0 / total_orders)) DESC) AS seller_rank
    FROM seller_stats
    ORDER BY seller_rank
    LIMIT 15;
    """
    df2 = pd.read_sql_query(q2, conn)
    st.dataframe(df2)

with tab3:
    st.subheader("State-wise Delivery Risk")
    q3 = """
    SELECT
        c.customer_state,
        COUNT(*) AS total_orders,
        SUM(CASE
                WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) > 0
                THEN 1 ELSE 0
            END) AS late_orders,
        ROUND(SUM(CASE
                WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) > 0
                THEN 1 ELSE 0
            END) * 100.0 / COUNT(*), 2) AS late_pct,
        ROUND(AVG(julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date)), 2) AS avg_delay_days
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY c.customer_state
    ORDER BY late_pct DESC
    LIMIT 10;
    """
    df3 = pd.read_sql_query(q3, conn)
    fig3 = px.bar(df3, x='customer_state', y='late_pct')
    st.plotly_chart(fig3, width='stretch')

with tab4:
    st.subheader("Category-wise Delay Risk")
    q4 = """
    SELECT
        ct.product_category_name_english AS category,
        COUNT(*) AS total_orders,
        ROUND(SUM(CASE
                WHEN julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) > 0
                THEN 1 ELSE 0
            END) * 100.0 / COUNT(*), 2) AS late_pct,
        ROUND(AVG(oi.price), 2) AS avg_price
    FROM order_items oi
    JOIN orders o ON oi.order_id = o.order_id
    JOIN products pr ON oi.product_id = pr.product_id
    JOIN category_translation ct ON pr.product_category_name = ct.product_category_name
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY category
    HAVING total_orders >= 30
    ORDER BY late_pct DESC
    LIMIT 10;
    """
    df4 = pd.read_sql_query(q4, conn)
    fig4 = px.bar(df4, x='category', y='late_pct')
    st.plotly_chart(fig4, width='stretch')

with tab5:
    st.subheader("Payment Method Distribution")
    q5 = """
    SELECT
        payment_type,
        COUNT(*) AS total_transactions,
        ROUND(AVG(payment_value), 2) AS avg_payment_value
    FROM order_payments
    GROUP BY payment_type
    ORDER BY avg_payment_value DESC;
    """
    df5 = pd.read_sql_query(q5, conn)
    fig5 = px.pie(df5, names='payment_type', values='total_transactions')
    st.plotly_chart(fig5, width='stretch')
