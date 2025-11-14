import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

# Initialize Faker
fake = Faker()

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_customers_data(n_customers=1000):
    """Generate customer data"""
    print("Generating customers data...")
    customers = []
    for i in range(n_customers):
        join_date = fake.date_between(start_date='-3y', end_date='today')
        customers.append({
            'customer_id': f'CUST_{i+1:04d}',
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'state': fake.state_abbr(),
            'zip_code': fake.zipcode(),
            'country': 'US',
            'join_date': join_date,
            'customer_tier': random.choice(['Basic', 'Silver', 'Gold', 'Platinum']),
            'loyalty_points': random.randint(0, 5000)
        })
    return pd.DataFrame(customers)

def generate_products_data(n_products=500):
    """Generate product catalog"""
    print("Generating products data...")
    categories = {
        'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Cameras'],
        'Clothing': ['Men', 'Women', 'Kids', 'Shoes', 'Accessories'],
        'Home': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Garden'],
        'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Yoga', 'Cycling'],
        'Beauty': ['Skincare', 'Makeup', 'Haircare', 'Fragrance', 'Bath & Body']
    }
    
    products = []
    for i in range(n_products):
        category = random.choice(list(categories.keys()))
        subcategory = random.choice(categories[category])
        cost = round(random.uniform(5, 500), 2)
        price = round(cost * random.uniform(1.2, 2.5), 2)
        
        products.append({
            'product_id': f'PROD_{i+1:04d}',
            'product_name': fake.catch_phrase(),
            'category': category,
            'subcategory': subcategory,
            'brand': fake.company(),
            'cost_price': cost,
            'selling_price': price,
            'stock_quantity': random.randint(0, 1000),
            'supplier': fake.company(),
            'is_active': random.choice([True, False]),
            'created_date': fake.date_between(start_date='-2y', end_date='today')
        })
    return pd.DataFrame(products)

def generate_orders_data(n_orders=5000, customers_df=None):
    """Generate orders data"""
    print("Generating orders data...")
    orders = []
    customer_ids = customers_df['customer_id'].tolist()
    
    for i in range(n_orders):
        customer_id = random.choice(customer_ids)
        order_date = fake.date_between(start_date='-1y', end_date='today')
        
        # Sometimes orders are shipped/delivered, sometimes not
        status_weights = ['delivered'] * 70 + ['shipped'] * 15 + ['processing'] * 10 + ['cancelled'] * 5
        status = random.choice(status_weights)
        
        if status in ['delivered', 'shipped']:
            shipped_date = order_date + timedelta(days=random.randint(1, 7))
            if status == 'delivered':
                delivered_date = shipped_date + timedelta(days=random.randint(1, 5))
            else:
                delivered_date = None
        else:
            shipped_date = None
            delivered_date = None
        
        orders.append({
            'order_id': f'ORD_{i+1:05d}',
            'customer_id': customer_id,
            'order_date': order_date,
            'shipped_date': shipped_date,
            'delivered_date': delivered_date,
            'status': status,
            'shipping_address': fake.address().replace('\n', ', '),
            'payment_method': random.choice(['Credit Card', 'PayPal', 'Debit Card', 'Apple Pay', 'Google Pay']),
            'payment_status': random.choice(['paid', 'pending', 'failed', 'refunded'])
        })
    return pd.DataFrame(orders)

def generate_order_items_data(orders_df=None, products_df=None, n_items=15000):
    """Generate order items data"""
    print("Generating order items data...")
    order_items = []
    order_ids = orders_df['order_id'].tolist()
    product_ids = products_df[products_df['is_active'] == True]['product_id'].tolist()
    products_dict = products_df.set_index('product_id')['selling_price'].to_dict()
    
    item_id = 1
    for order_id in order_ids:
        n_items_in_order = random.randint(1, 8)  # 1-8 items per order
        for _ in range(n_items_in_order):
            if item_id > n_items:
                break
                
            product_id = random.choice(product_ids)
            quantity = random.randint(1, 5)
            unit_price = products_dict[product_id]
            
            order_items.append({
                'order_item_id': item_id,
                'order_id': order_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': unit_price,
                'total_price': round(quantity * unit_price, 2)
            })
            item_id += 1
            
        if item_id > n_items:
            break
            
    return pd.DataFrame(order_items)

def generate_reviews_data(order_items_df=None, n_reviews=8000):
    """Generate product reviews data"""
    print("Generating reviews data...")
    reviews = []
    order_items_sample = order_items_df.sample(n=min(n_reviews, len(order_items_df)), random_state=42)
    
    for idx, row in order_items_sample.iterrows():
        review_date = fake.date_between(start_date='-1y', end_date='today')
        rating = random.choices([1, 2, 3, 4, 5], weights=[1, 2, 3, 4, 5])[0]
        
        reviews.append({
            'review_id': f'REV_{idx+1:05d}',
            'order_item_id': int(row['order_item_id']),
            'product_id': row['product_id'],
            'rating': rating,
            'review_text': fake.paragraph(nb_sentences=random.randint(1, 3)),
            'review_date': review_date,
            'helpful_votes': random.randint(0, 50),
            'verified_purchase': random.choice([True, False])
        })
    
    return pd.DataFrame(reviews)

def main():
    print("🚀 STEP 1: Generating Synthetic Ecommerce Data")
    print("=" * 50)
    
    # Generate all data
    customers_df = generate_customers_data(1000)
    products_df = generate_products_data(500)
    orders_df = generate_orders_data(5000, customers_df)
    order_items_df = generate_order_items_data(orders_df, products_df, 15000)
    reviews_df = generate_reviews_data(order_items_df, 8000)
    
    # Save to CSV files
    customers_df.to_csv('customers.csv', index=False)
    products_df.to_csv('products.csv', index=False)
    orders_df.to_csv('orders.csv', index=False)
    order_items_df.to_csv('order_items.csv', index=False)
    reviews_df.to_csv('reviews.csv', index=False)
    
    print("\n✅ Data generation completed! 5 files created:")
    print("   - customers.csv")
    print("   - products.csv")
    print("   - orders.csv")
    print("   - order_items.csv")
    print("   - reviews.csv")
    
    # Show sample data
    print(f"\n📊 Sample data sizes:")
    print(f"   Customers: {len(customers_df)}")
    print(f"   Products: {len(products_df)}")
    print(f"   Orders: {len(orders_df)}")
    print(f"   Order Items: {len(order_items_df)}")
    print(f"   Reviews: {len(reviews_df)}")

if __name__ == "__main__":
    main()