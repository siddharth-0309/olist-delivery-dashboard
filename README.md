# 📦 Olist Delivery Performance & Customer Satisfaction Analysis

An end-to-end SQL analytics project analyzing how delivery performance impacts customer satisfaction, seller accountability, and regional/category risk — using the Olist Brazilian E-Commerce dataset. Built with SQL (SQLite) and deployed as an interactive Streamlit dashboard.

🔗 **Live App:** [olist-delivery-dashboard.streamlit.app](https://olist-delivery-dashboard-68o6q373ygdcpxb4acb8bq.streamlit.app/)

---

## 📌 Problem Statement

E-commerce platforms lose customer trust and revenue when deliveries are delayed — but *how much* impact does a delay actually have, and where in the operation does it originate? This project answers four business questions using the Olist dataset (~99,000 orders, 2016–2018):

1. Does delivery delay significantly affect customer review scores?
2. Which sellers consistently underperform on delivery timelines?
3. Are certain regions (states) more prone to delivery delays?
4. Do certain product categories carry higher delay risk?

---

## 🔑 Key Findings

| Insight | Finding |
|---|---|
| **Delay → Satisfaction** | Average review score drops from **4.29 (on-time)** to **2.27 (late)** — a ~47% decline. Delay is one of the strongest single predictors of customer dissatisfaction. |
| **Seller Performance** | On-time delivery rate varies widely across the 3,000+ active sellers, even after filtering out low-volume sellers (min. 10 orders) to avoid statistical noise. |
| **Regional Risk** | Delay rates are not uniform across customer states — some regions show significantly higher late-delivery percentages, pointing to logistics bottlenecks. |
| **Category Risk** | Certain product categories show higher delay rates than others, useful for inventory and packaging planning. |
| **Payment Behavior** | Credit card is the dominant payment method among customers, ahead of boleto, voucher, and debit card. |

---

## 🛠️ Tech Stack

- **SQL (SQLite)** — CTEs, window functions (`RANK() OVER`), multi-table joins, conditional aggregation (`CASE WHEN`)
- **Python** — Pandas for data loading and query execution
- **Streamlit** — Interactive multi-tab dashboard
- **Plotly** — Data visualizations (bar charts, pie charts)

---

## 📊 Dashboard Overview

The live app has 5 sections:

1. **Delay vs Satisfaction** — Review score by delay bucket (On-Time, 1–3 days late, 4–7 days late, 7+ days late)
2. **Seller Performance** — Ranked seller leaderboard by on-time delivery rate
3. **Regional Risk** — State-wise late delivery percentage
4. **Category Risk** — Product category-wise delay risk
5. **Payment Methods** — Distribution of payment types used by customers

---

## 🗂️ Dataset

[Olist Brazilian E-Commerce Public Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) — ~99,000 orders placed on the Olist marketplace between 2016 and 2018, across customers, orders, order items, payments, reviews, products, and sellers.

*(Geolocation data was excluded from this analysis as it was not required for the core business questions.)*

---

## 🚀 Running Locally

```bash
git clone https://github.com/siddharth-0309/olist-delivery-dashboard.git
cd olist-delivery-dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Project Structure

```
olist-delivery-dashboard/
├── app.py              # Streamlit dashboard application
├── olist.db            # SQLite database (Olist dataset)
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 💡 Solution Summary

This project converts raw, multi-table e-commerce transaction data into business-ready insights using SQL, and delivers them through a live, self-service Streamlit dashboard. Instead of static notebooks, the solution enables anyone — technical or non-technical — to explore delivery risk by seller, region, and product category in real time, without needing to write a single query.

The core finding — that a late delivery nearly halves a customer's review score (4.29 → 2.27) — demonstrates that delivery performance is not just an operations metric, but a direct driver of customer retention and brand trust.

---

## 📈 Business Growth Recommendations

Based on the analysis, the following actions could help improve customer satisfaction and reduce delivery-related churn:

1. **Prioritize seller accountability** — Introduce a minimum on-time delivery threshold for sellers; flag or restrict consistently underperforming sellers identified in the Seller Performance tab.
2. **Target high-risk regions** — Invest in additional courier partnerships or regional warehousing in states showing the highest late-delivery percentages, rather than applying a uniform logistics strategy nationwide.
3. **Set category-specific delivery buffers** — For product categories with higher delay rates, adjust estimated delivery dates upward to manage customer expectations, or improve packaging/handling processes for fragile or bulky items.
4. **Monitor delay in real time, not retrospectively** — Use a dashboard like this to catch delay trends early (e.g., weekly), rather than discovering the impact only after reviews have already dropped.
5. **Tie delivery performance to seller incentives** — Reward top-ranked sellers (from the on-time rate leaderboard) with better marketplace visibility, encouraging healthy competition around delivery reliability.

Together, these steps shift delivery management from a reactive, post-complaint process to a proactive, data-driven one — directly protecting customer satisfaction and long-term revenue.

---

## 👤 Author

**Siddharth Singh**
B.Sc (Hons.) Data Science — Swami Rama Himalayan University
[GitHub](https://github.com/siddharth-0309)
