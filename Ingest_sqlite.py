import pandas as pd
import sqlite3

def create_database_and_tables():
    """Create SQLite database and tables"""
    print("Creating database and tables...")
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS customers (
        customer_id TEXT PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        city TEXT,
        state TEXT,
        zip_code TEXT,
        country TEXT,
        join_date DATE,
        customer_tier TEXT,
        loyalty_points INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT,
        category TEXT,
        subcategory TEXT,
        brand TEXT,
        cost_price REAL,
        selling_price REAL,
        stock_quantity INTEGER,
        supplier TEXT,
        is_active BOOLEAN,
        created_date DATE
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        order_id TEXT PRIMARY KEY,
        customer_id TEXT,
        order_date DATE,
        shipped_date DATE,
        delivered_date DATE,
        status TEXT,
        shipping_address TEXT,
        payment_method TEXT,
        payment_status TEXT,
        FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        order_item_id INTEGER PRIMARY KEY,
        order_id TEXT,
        product_id TEXT,
        quantity INTEGER,
        unit_price REAL,
        total_price REAL,
        FOREIGN KEY (order_id) REFERENCES orders (order_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reviews (
        review_id TEXT PRIMARY KEY,
        order_item_id INTEGER,
        product_id TEXT,
        rating INTEGER,
        review_text TEXT,
        review_date DATE,
        helpful_votes INTEGER,
        verified_purchase BOOLEAN,
        FOREIGN KEY (order_item_id) REFERENCES order_items (order_item_id),
        FOREIGN KEY (product_id) REFERENCES products (product_id)
    )
    ''')
    
    conn.commit()
    return conn

def import_data_to_database():
    """Import CSV data into database tables"""
    conn = create_database_and_tables()
    
    tables = ['customers', 'products', 'orders', 'order_items', 'reviews']
    
    for table in tables:
        print(f"Importing {table}...")
        df = pd.read_csv(f'{table}.csv')
        df.to_sql(table, conn, if_exists='replace', index=False)
        print(f"   ✅ {len(df)} records imported")
    
    # Verify data import
    cursor = conn.cursor()
    print("\n📊 Database Summary:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   {table}: {count} records")
    
    conn.close()
    print("\n✅ All data imported into SQLite database (ecommerce.db)!")

def main():
    print("🚀 STEP 2: Creating SQLite Database and Importing Data")
    print("=" * 50)
    import_data_to_database()

if __name__ == "__main__":
    main()