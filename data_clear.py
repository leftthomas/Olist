import pandas as pd

df = pd.read_csv('data/olist_classified_public_dataset.csv')
# select all votes columns and  drop them
votes_columns = [s for s in df.columns if "votes_" in s]
df.drop(votes_columns, axis=1, inplace=True)

# drop the first two columns
df.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)
# drop the review_comment_title column, because all values are null
df.drop(['review_comment_title'], axis=1, inplace=True)
# drop the duplicate rows
df.drop_duplicates(inplace=True)
# drop the rows which cantains NaN value
df.dropna(inplace=True)

# convert datetime features to the correct format
df.order_purchase_timestamp = pd.to_datetime(df.order_purchase_timestamp)
df.order_aproved_at = pd.to_datetime(df.order_aproved_at)
df.order_estimated_delivery_date = pd.to_datetime(df.order_estimated_delivery_date)
df.order_delivered_customer_date = pd.to_datetime(df.order_delivered_customer_date)
df.review_creation_date = pd.to_datetime(df.review_creation_date)
df.review_answer_timestamp = pd.to_datetime(df.review_answer_timestamp)
# print the info of this dataset
# print(df.info())
# save this file
df.to_csv('data/classified_orders.csv', index_label='id')
