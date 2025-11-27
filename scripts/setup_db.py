import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import sys

def setup_database():
    print("🚀 Starting Database Setup...")
    
    # Default connection to 'postgres' database to create new DB/User
    # Trying default credentials. If this fails, user needs to provide them.
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="password", # Trying empty password
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Could not connect to 'postgres' DB: {e}")
        print("Please ensure PostgreSQL is running and the password for 'postgres' user is 'password'.")
        sys.exit(1)

    # 1. Create User (if not exists)
    try:
        cur.execute("CREATE USER postgres WITH PASSWORD 'password';")
        print("✅ User 'postgres' created (or already exists).")
    except psycopg2.errors.DuplicateObject:
        print("ℹ️  User 'postgres' already exists.")
    except Exception as e:
        print(f"⚠️  Error creating user: {e}")

    # 2. Create Database
    try:
        cur.execute("CREATE DATABASE xpulse_tribunal OWNER postgres;")
        print("✅ Database 'xpulse_tribunal' created.")
    except psycopg2.errors.DuplicateDatabase:
        print("ℹ️  Database 'xpulse_tribunal' already exists.")
    except Exception as e:
        print(f"❌ Error creating database: {e}")
    
    cur.close()
    conn.close()

    # 3. Connect to the new database
    print("🔄 Connecting to 'xpulse_tribunal'...")
    try:
        conn = psycopg2.connect(
            dbname="xpulse_tribunal",
            user="postgres",
            password="password",
            host="localhost",
            port="5432"
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
    except Exception as e:
        print(f"❌ Could not connect to 'xpulse_tribunal': {e}")
        sys.exit(1)

    # 4. Create Table
    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS env_vars (
                id SERIAL PRIMARY KEY,
                key TEXT NOT NULL UNIQUE,
                value TEXT NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
            );
        """)
        print("✅ Table 'env_vars' created.")
    except Exception as e:
        print(f"❌ Error creating table: {e}")
        sys.exit(1)

    # 5. Insert Values
    # Using ON CONFLICT DO UPDATE to handle re-runs
    values = [
        ('POSTGRES_USER','postgres'),
        ('POSTGRES_PASSWORD','password'),
        ('POSTGRES_SERVER','localhost'),
        ('POSTGRES_PORT','5432'),
        ('POSTGRES_DB','xpulse_tribunal'),
        ('REDIS_HOST','localhost'),
        ('REDIS_PORT','6379')
    ]
    
    print("📝 Inserting environment variables...")
    for key, val in values:
        try:
            cur.execute("""
                INSERT INTO env_vars (key, value) 
                VALUES (%s, %s)
                ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;
            """, (key, val))
        except Exception as e:
            print(f"❌ Error inserting {key}: {e}")

    # 6. Verify
    cur.execute("SELECT * FROM env_vars ORDER BY id;")
    rows = cur.fetchall()
    print("\n📊 Current env_vars:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()
    print("\n✅ Database setup complete!")

if __name__ == "__main__":
    setup_database()
