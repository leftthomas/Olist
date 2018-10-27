import pandas as pd

product_names_table = pd.read_csv('data/product_category_name_translation.csv')
customers_table = pd.read_csv('data/olist_public_dataset_v2_customers.csv')
payment_table = pd.read_csv('data/olist_public_dataset_v2_payments.csv')
geolocation_table = pd.read_csv('data/geolocation_olist_public_dataset.csv')
unclassified_orders = pd.read_csv('data/olist_public_dataset_v2.csv')
classified_orders = pd.read_csv('data/olist_classified_public_dataset.csv')

# merge translations for category names
unclassified_orders = unclassified_orders.merge(product_names_table, on='product_category_name').drop(
    'product_category_name', axis=1)
unclassified_orders.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)
classified_orders = classified_orders.merge(product_names_table, on='product_category_name').drop(
    'product_category_name', axis=1)
classified_orders.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)

# merge customer ids
unclassified_orders = unclassified_orders.merge(customers_table, on='customer_id').drop('customer_id', axis=1)
unclassified_orders.rename(columns={'customer_unique_id': 'customer_id'}, inplace=True)

# drop the first two columns
classified_orders.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)
# drop the review_comment_title column, because all values are null
classified_orders.drop(['review_comment_title'], axis=1, inplace=True)
# drop the review_id column, because this value is same as order_id
unclassified_orders.drop(['review_id'], axis=1, inplace=True)
# drop the duplicate rows
print(payment_table.info())
payment_table.drop_duplicates(inplace=True)
print(payment_table.info())

# payment_table.dropna(inplace=True)
# df.to_csv('data/classified_orders.csv', index=False)
