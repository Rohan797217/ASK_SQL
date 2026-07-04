"""
Database Initialization Script
Run this once to set up the Northwind schema and sample data in your Neon Postgres database.

Usage:
    cd backend
    python -m scripts.init_db
"""

import sys
import os

# Add parent directory to path so we can import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import init_database, check_connection


def main():
    print("=" * 50)
    print("AskSQL — Database Initialization")
    print("=" * 50)
    print()

    # Check connection first
    print("Checking database connection...")
    status = check_connection()

    if status != "connected":
        print(f"❌ Cannot connect to database: {status}")
        print()
        print("Make sure your .env file has a valid DATABASE_URL:")
        print("  DATABASE_URL=postgresql://user:pass@host/dbname?sslmode=require")
        sys.exit(1)

    print("✅ Database connected!")
    print()

    # Confirm before proceeding
    print("⚠️  This will DROP existing tables and recreate them with sample data.")
    response = input("Continue? (y/n): ").strip().lower()

    if response != "y":
        print("Cancelled.")
        sys.exit(0)

    print()
    print("Creating Northwind schema and loading sample data...")
    print()

    try:
        init_database()
        print()
        print("=" * 50)
        print("✅ Database initialized successfully!")
        print()
        print("Tables created:")
        print("  • categories (8 rows)")
        print("  • customers (30 rows)")
        print("  • employees (9 rows)")
        print("  • suppliers (10 rows)")
        print("  • shippers (3 rows)")
        print("  • products (25 rows)")
        print("  • orders (35 rows)")
        print("  • order_details (~90 rows)")
        print()
        print("You can now start the backend:")
        print("  uvicorn app.main:app --reload")
        print("=" * 50)
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
