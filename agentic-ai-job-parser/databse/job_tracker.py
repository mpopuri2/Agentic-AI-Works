import psycopg2
from datetime import datetime
from config.settings import DB_CONFIG

from zoneinfo import ZoneInfo

est_time = datetime.now(ZoneInfo('America/New_York'))

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def initialize_db():

    conn = get_connection()
    cursor = conn.cursor()
    QUERY = """
        CREATE TABLE IF NOT EXISTS Job_Applications(
        id SERIAL PRIMARY KEY,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        link TEXT NOT NULL,
        date_applied TIMESTAMP NOT NULL,
        status TEXT DEFAULT 'APPLIED',
        resume TEXT,
        cover_letter TEXT,
        UNIQUE(link)

        );
    """

    cursor.execute(QUERY)
    conn.commit()
    cursor.close()
    conn.close()

    print("PostGRE SQL Table is Initialized Successfully.")

def application_exists(link):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Job_Applications where link = %s", (link))
    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return result is not None

def save_application(company,role, link, resume = None, cover_letter = None,status = "applied"):

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""INSERT INTO Job_Applications 
        (company, role, link, date_applied, resume, cover_letter, status) VALUES(%s,%s,%s,%s,%s,%s,%s)""",(company,role,link,est_time,resume,cover_letter,status))
        conn.commit()
        print(f"Saved application for {role} at {company}")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Application already exists. Skipped.")
    finally:
        cursor.close()
        conn.close()

def get_all_Applications():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT company,role, link, status, date_applied FROM Job_Applications ORDER BY date_applied DESC;")
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

