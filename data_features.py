import pandas as pd
import seaborn as sns

sns.set(rc={'figure.figsize': (16, 9)})
import matplotlib.pyplot as plt

df = pd.read_csv('data/classified_orders.csv')
df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)
df.order_aproved_at = pd.to_datetime(df.order_aproved_at)
df.order_estimated_delivery_date = pd.to_datetime(df.order_estimated_delivery_date)
df.order_delivered_customer_date = pd.to_datetime(df.order_delivered_customer_date)
df.review_creation_date = pd.to_datetime(df.review_creation_date)
df.review_answer_timestamp = pd.to_datetime(df.review_answer_timestamp)

# creating a purchase day feature
df['order_purchase_date'] = df.order_purchase_timestamp.dt.date

# creating an aggregation
sales_per_purchase_date = df.groupby('order_purchase_date', as_index=False).order_products_value.sum()
ax = sns.lineplot(x="order_purchase_date", y="order_products_value", data=sales_per_purchase_date)
ax.set_title('Sales per day')
plt.show()

# creating a purchase day feature
df['order_purchase_week'] = df.order_purchase_timestamp.dt.to_period('W').astype(str)

# creating an aggregation
sales_per_purchase_month = df.groupby('order_purchase_week', as_index=False).order_products_value.sum()
ax = sns.lineplot(x="order_purchase_week", y="order_products_value", data=sales_per_purchase_month)
ax.set_title('Sales per week')
plt.show()

# creating an aggregation
avg_score_per_date = df.groupby('order_purchase_week', as_index=False).review_score.mean()
ax = sns.lineplot(x="order_purchase_week", y="review_score", data=avg_score_per_date)
ax.set_title('Average score per week')
plt.show()

# creating an aggregation
avg_score_per_category = df.groupby('product_category_name', as_index=False).agg({'review_score': ['count', 'mean']})
avg_score_per_category.columns = ['product_category_name', 'count', 'mean']

# filtering to show only categories with more than 50 reviews
avg_score_per_category = avg_score_per_category[avg_score_per_category['count'] > 50]
avg_score_per_category = avg_score_per_category.sort_values(by='mean', ascending=False)
ax = sns.barplot(x="mean", y="product_category_name", data=avg_score_per_category)
ax.set_title('Categories Review Score')
plt.show()

eletronicos = df[df.product_category_name == 'eletronicos']['most_voted_class'].value_counts().reset_index()
eletronicos.columns = ['class', 'qty']
eletronicos['percent_qty'] = eletronicos.qty / eletronicos.qty.sum()
ax = sns.barplot(x="percent_qty", y="class", data=eletronicos)
ax.set_title('Eletronicos Reviews Classes')
plt.show()

informatica_acessorios = df[df.product_category_name == 'informatica_acessorios'][
    'most_voted_class'].value_counts().reset_index()
informatica_acessorios.columns = ['class', 'qty']
informatica_acessorios['percent_qty'] = informatica_acessorios.qty / informatica_acessorios.qty.sum()
ax = sns.barplot(x="percent_qty", y="class", data=informatica_acessorios)
ax.set_title('Informatica Acessorios Reviews Classes')
plt.show()
