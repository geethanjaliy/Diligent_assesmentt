import pandas as pd
import sqlite3

def run_complex_queries():
    """Run complex queries joining multiple tables"""
    conn = sqlite3.connect('ecommerce.db')
    
    print("🚀 STEP 3: Running Complex Queries")
    print("=" * 50)
    
    # Query 1: Customer purchasing behavior with reviews
    query1 = '''
    SELECT 
        c.customer_id,
        c.first_name || ' ' || c.last_name AS customer_name,
        c.customer_tier,
        COUNT(DISTINCT o.order_id) AS total_orders,
        ROUND(SUM(oi.total_price), 2) AS total_spent,
        ROUND(AVG(r.rating), 2) AS avg_rating_given,
        COUNT(r.review_id) AS reviews_written
    FROM customers c
    LEFT JOIN orders o ON c.customer_id = o.customer_id
    LEFT JOIN order_items oi ON o.order_id = oi.order_id
    LEFT JOIN reviews r ON oi.order_item_id = r.order_item_id
    GROUP BY c.customer_id, customer_name, c.customer_tier
    HAVING total_orders > 0
    ORDER BY total_spent DESC
    LIMIT 10
    '''
    
    print("\n📊 QUERY 1: Top 10 Customers by Spending with Review Activity")
    print("-" * 60)
    result1 = pd.read_sql_query(query1, conn)
    print(result1.to_string(index=False))
    result1.to_csv('query1_top_customers.csv', index=False)
    print("✅ Saved as: query1_top_customers.csv")
    
    # Query 2: Product performance analysis
    query2 = '''
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.brand,
        COUNT(oi.order_item_id) AS times_ordered,
        SUM(oi.quantity) AS total_units_sold,
        ROUND(SUM(oi.total_price), 2) AS total_revenue,
        ROUND(AVG(r.rating), 2) AS avg_rating,
        COUNT(r.review_id) AS review_count
    FROM products p
    LEFT JOIN order_items oi ON p.product_id = oi.product_id
    LEFT JOIN reviews r ON p.product_id = r.product_id
    WHERE p.is_active = 1
    GROUP BY p.product_id, p.product_name, p.category, p.brand
    HAVING times_ordered > 0
    ORDER BY total_revenue DESC
    LIMIT 15
    '''
    
    print("\n📈 QUERY 2: Top 15 Products by Revenue")
    print("-" * 60)
    result2 = pd.read_sql_query(query2, conn)
    print(result2.to_string(index=False))
    result2.to_csv('query2_top_products.csv', index=False)
    print("✅ Saved as: query2_top_products.csv")
    
    # Query 3: Monthly sales performance by category
    query3 = '''
    SELECT 
        strftime('%Y-%m', o.order_date) AS sales_month,
        p.category,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.quantity) AS units_sold,
        ROUND(SUM(oi.total_price), 2) AS total_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.status = 'delivered'
    GROUP BY sales_month, p.category
    ORDER BY sales_month DESC, total_revenue DESC
    LIMIT 20
    '''
    
    print("\n📅 QUERY 3: Monthly Sales Performance by Category")
    print("-" * 60)
    result3 = pd.read_sql_query(query3, conn)
    print(result3.to_string(index=False))
    result3.to_csv('query3_monthly_sales.csv', index=False)
    print("✅ Saved as: query3_monthly_sales.csv")
    
    # Query 4: Customer lifetime value analysis
    query4 = '''
    SELECT 
        c.customer_tier,
        COUNT(DISTINCT c.customer_id) AS customer_count,
        ROUND(AVG(orders_per_customer), 2) AS avg_orders_per_customer,
        ROUND(AVG(total_spent), 2) AS avg_lifetime_value,
        ROUND(AVG(order_frequency_days), 2) AS avg_order_frequency_days
    FROM (
        SELECT 
            c.customer_id,
            c.customer_tier,
            COUNT(o.order_id) AS orders_per_customer,
            SUM(oi.total_price) AS total_spent,
            JULIANDAY(MAX(o.order_date)) - JULIANDAY(MIN(o.order_date)) AS order_frequency_days
        FROM customers c
        JOIN orders o ON c.customer_id = o.customer_id
        JOIN order_items oi ON o.order_id = oi.order_id
        GROUP BY c.customer_id, c.customer_tier
        HAVING orders_per_customer > 1
    ) AS customer_stats
    JOIN customers c ON customer_stats.customer_id = c.customer_id
    GROUP BY c.customer_tier
    ORDER BY avg_lifetime_value DESC
    '''
    
    print("\n💰 QUERY 4: Customer Lifetime Value by Tier")
    print("-" * 60)
    result4 = pd.read_sql_query(query4, conn)
    print(result4.to_string(index=False))
    result4.to_csv('query4_customer_lifetime_value.csv', index=False)
    print("✅ Saved as: query4_customer_lifetime_value.csv")
    
    conn.close()
    
    print(f"\n🎉 All queries executed successfully!")
    print(f"📁 Query results saved as CSV files")

def main():
    run_complex_queries()

if __name__ == "__main__":
    main()