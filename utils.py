import string

import pandas as pd


def load_data():
    customers = pd.read_csv('data/customers.csv')
    geolocations = pd.read_csv('data/geolocations.csv')
    items = pd.read_csv('data/items.csv')
    items['shipping_limit_date'] = pd.to_datetime(items['shipping_limit_date'])
    payments = pd.read_csv('data/payments.csv')
    reviews = pd.read_csv('data/reviews.csv')
    reviews['review_creation_date'] = pd.to_datetime(reviews['review_creation_date'])
    reviews['review_answer_timestamp'] = pd.to_datetime(reviews['review_answer_timestamp'])
    # remove fake data
    reviews = reviews[reviews['review_score'].isin(['1', '2', '3', '4', '5'])]
    reviews['review_score'] = reviews['review_score'].astype('int')
    orders = pd.read_csv('data/orders.csv')
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
    orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
    orders['order_delivered_carrier_date'] = pd.to_datetime(orders['order_delivered_carrier_date'])
    orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
    orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])
    products = pd.read_csv('data/products.csv')
    sellers = pd.read_csv('data/sellers.csv')
    product_names_translations = pd.read_csv('data/translations.csv')
    # merge product_names_translations to products and replace it
    products = pd.merge(products, product_names_translations, on='product_category_name')
    products.drop(['product_category_name'], axis=1, inplace=True)
    products.rename(columns={'product_category_name_english': 'product_category_name'}, inplace=True)

    # preprocessing data
    order_values = items[['order_id', 'price']].groupby('order_id').sum()
    summed_orders = pd.merge(orders[['order_id', 'order_purchase_timestamp']], order_values, on='order_id')
    # creating purchase feature
    summed_orders['order_purchase_date'] = summed_orders['order_purchase_timestamp'].dt.date.apply(
        lambda x: x.strftime('%Y-%m-%d'))
    summed_orders['order_purchase_week'] = summed_orders['order_purchase_timestamp'].dt.date.apply(
        lambda x: x.strftime('%A'))
    # creating aggregations
    sales_per_purchase_date = summed_orders.groupby('order_purchase_date', as_index=False).sum()
    sales_per_purchase_date['price'] = sales_per_purchase_date['price'].apply(lambda x: float('%.2f' % x))
    sales_per_purchase_week = summed_orders.groupby('order_purchase_week', as_index=False).sum()
    sales_per_purchase_week['price'] = sales_per_purchase_week['price'].apply(lambda x: float('%.2f' % (x / 1000)))
    list_sorted = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    sales_per_purchase_week['order_purchase_week'] = sales_per_purchase_week['order_purchase_week'].astype(
        'category').cat.set_categories(list_sorted)
    sales_per_purchase_week = sales_per_purchase_week.sort_values(by=['order_purchase_week'], ascending=True)

    merged_reviews = pd.merge(reviews[['order_id', 'review_score']], items[['order_id', 'product_id']], how='left',
                              on='order_id')
    merged_reviews = pd.merge(merged_reviews, products[['product_id', 'product_category_name']], how='left',
                              on='product_id')
    # creating an aggregation
    avg_score_per_category = merged_reviews.groupby('product_category_name', as_index=False).agg(
        {'review_score': ['count', 'mean']})
    avg_score_per_category.columns = ['product_category_name', 'review_score_count', 'review_score_mean']
    # filtering to show only categories with more than 50 reviews
    avg_score_per_category = avg_score_per_category[avg_score_per_category['review_score_count'] > 50]
    avg_score_per_category['product_category_name'] = avg_score_per_category['product_category_name'].apply(
        lambda x: x.replace('_', ' '))
    avg_score_per_category['review_score_mean'] = avg_score_per_category['review_score_mean'].apply(
        lambda x: float('%.2f' % x))

    payments_values = payments[['payment_type', 'payment_value']].groupby('payment_type', as_index=False).sum()
    payments_values['payment_value'] = (
            payments_values['payment_value'] / payments_values['payment_value'].sum()).apply(
        lambda x: float('%.2f' % x))
    payments_values['payment_type'] = payments_values['payment_type'].apply(lambda x: x.replace('_', ' '))

    payments_numbers = payments[['order_id', 'payment_type']].drop_duplicates()
    payments_numbers = payments_numbers.groupby('payment_type', as_index=False).agg({'order_id': ['count']})
    payments_numbers.columns = ['payment_type', 'payment_type_count']
    payments_numbers['payment_type_count'] = (payments_numbers['payment_type_count'] / payments_numbers[
        'payment_type_count'].sum()).apply(lambda x: float('%.2f' % x))
    payments_numbers['payment_type'] = payments_numbers['payment_type'].apply(lambda x: x.replace('_', ' '))

    count_state = geolocations['geolocation_state'].value_counts()
    count_city = geolocations['geolocation_city'].value_counts()
    # fix the data error, the two rows are the single one same city
    count_city['sao paulo'] = count_city['são paulo'] + count_city['sao paulo']
    del count_city['são paulo']
    count_city['others'] = count_city[count_city < 10000].sum()
    count_city = count_city[count_city >= 10000]

    merged_products = pd.merge(items[['order_id', 'product_id']], products[['product_id', 'product_category_name']],
                               on='product_id')
    merged_products.dropna(inplace=True)
    merged_products['product_category_name'] = merged_products['product_category_name'].apply(
        lambda x: x.replace('_', ' '))
    count_product = merged_products['product_category_name'].value_counts()

    merged_comment = reviews[['review_id', 'review_comment_message']].dropna()
    exclude = set(string.punctuation)
    merged_comment['review_comment_message'] = merged_comment['review_comment_message'].apply(
        lambda x: x.lower())
    merged_comment['review_comment_message'] = merged_comment['review_comment_message'].apply(
        lambda x: ''.join(ch for ch in x if ch not in exclude))
    merged_comment = merged_comment[merged_comment['review_comment_message'] != '']
    merged_comment.dropna(inplace=True)
    a = ''
    for comment in merged_comment['review_comment_message']:
        a = a + ' ' + comment
    b = {}
    for ch in a.split():
        if len(ch) >= 3:
            if ch not in b:
                b[ch] = 1
            else:
                b[ch] = b[ch] + 1
    count_comment = pd.Series(b)

    # Removing some outliers
    # Brazils most Northern spot is at 5 deg 16′ 27.8″ N latitude.
    geo = geolocations[geolocations['geolocation_lat'] <= 5.27438888]
    # It’s most Western spot is at 73 deg, 58′ 58.19″W Long.
    geo = geo[geo['geolocation_lng'] >= -73.98283055]
    # It’s most Southern spot is at 33 deg, 45′ 04.21″ S Latitude.
    geo = geo[geo['geolocation_lat'] >= -33.75116944]
    # It’s most Eastern spot is 34 deg, 47′ 35.33″ W Long.
    geo = geo[geo['geolocation_lng'] <= -34.79314722]
    # fix the data error, the two rows are the single one same city
    geo['geolocation_city'].replace(['são paulo'], ['sao paulo'], inplace=True)
    customers['customer_city'].replace(['são paulo'], ['sao paulo'], inplace=True)
    sellers['seller_city'].replace(['são paulo'], ['sao paulo'], inplace=True)

    zip_code_geo = geo.groupby('geolocation_zip_code_prefix').mean()
    unique_customers = customers.drop_duplicates(subset=['customer_unique_id'])
    merged_customers = pd.merge(unique_customers[['customer_id', 'customer_zip_code_prefix']], zip_code_geo,
                                left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    merged_sellers = pd.merge(sellers[['seller_id', 'seller_zip_code_prefix']], zip_code_geo,
                              left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    merged_orders = pd.merge(orders[['order_id', 'customer_id']],
                             customers[['customer_id', 'customer_zip_code_prefix']], on='customer_id')
    merged_orders = pd.merge(merged_orders[['order_id', 'customer_zip_code_prefix']], zip_code_geo,
                             left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    sp_customers = unique_customers[unique_customers['customer_state'] == 'SP']
    merged_sp_customers = pd.merge(sp_customers[['customer_id', 'customer_zip_code_prefix']], zip_code_geo,
                                   left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    spc_customers = unique_customers[unique_customers['customer_city'] == 'sao paulo']
    merged_spc_customers = pd.merge(spc_customers[['customer_id', 'customer_zip_code_prefix']], zip_code_geo,
                                    left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')
    return sales_per_purchase_date, sales_per_purchase_week, payments_values, avg_score_per_category, payments_numbers, \
           count_state, count_city, count_product, count_comment, geo, merged_customers, merged_sellers, merged_orders, \
           merged_sp_customers, merged_spc_customers
