"""Utility script to create database tables for development."""
from db import create_all_tables, get_engine

def main():
    print("Creating database tables...")
    ok = create_all_tables()
    if ok:
        print("✅ Tables created successfully")
    else:
        print("❌ Failed to create tables")

if __name__ == '__main__':
    main()
