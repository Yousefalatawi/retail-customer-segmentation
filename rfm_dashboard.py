import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

# عنوان الصفحة
st.title("Retail Customer Segmentation with RFM Analysis")

# توليد بيانات تجريبية
np.random.seed(42)
n_customers = 100
n_transactions = 500

customer_ids = np.random.choice(range(1, n_customers + 1), size=n_transactions)
invoice_dates = [datetime(2024, 9, 30) - timedelta(days=np.random.randint(1, 180)) for _ in range(n_transactions)]
amounts = np.round(np.random.exponential(100, size=n_transactions), 2)

df = pd.DataFrame({
    'CustomerID': customer_ids,
    'InvoiceDate': invoice_dates,
    'Amount': amounts
})

# حساب تاريخ المرجع
snapshot_date = datetime(2024, 9, 30)

# حساب مؤشرات RFM
rfm = df.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (snapshot_date - x.max()).days),
    Frequency=('InvoiceDate', 'count'),
    Monetary=('Amount', 'sum')
).reset_index()

# إعطاء درجات لكل مقياس (1-4)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1, 2, 3, 4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1, 2, 3, 4]).astype(int)

# دمج الدرجات لتكوين RFM Score
rfm['RFM_Score'] = rfm['R_Score'].map(str) + rfm['F_Score'].map(str) + rfm['M_Score'].map(str)

# تقسيم الشرائح (Segments) بناء على RFM Score
def segment_customer(df):
    if df['RFM_Score'] == '444':
        return 'Best Customers'
    elif df['R_Score'] == 4 and df['F_Score'] >= 3:
        return 'Loyal Customers'
    elif df['R_Score'] >= 3 and df['M_Score'] >= 3:
        return 'Big Spenders'
    else:
        return 'Others'

rfm['Segment'] = rfm.apply(segment_customer, axis=1)

# عرض الجدول الرئيسي
st.subheader("RFM Table")
st.dataframe(rfm)

# إحصائيات عن الشرائح
st.subheader("Segment Distribution")
segment_counts = rfm['Segment'].value_counts()
st.bar_chart(segment_counts)

# ملخص
st.write(f"عدد العملاء: {len(rfm)}")
st.write(f"عدد شرائح العملاء: {segment_counts.shape[0]}")

