import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# توليد بيانات تجريبية
np.random.seed(42)
n_customers = 100
n_transactions = 500
customer_ids = np.random.choice(range(1, n_customers+1), size=n_transactions)
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
)

# إعطاء درجات لكل مقياس
rfm['R_Score'] = pd.qcut(rfm['Recency'], 4, labels=[4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'], 4, labels=[1, 2, 3, 4]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 4, labels=[1,_
