import os
import csv
import sys
from supabase import create_client, Client

# Force UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# --- Configuration ---
ENV_SUPABASE_URL = "SUPABASE_URL"
ENV_SUPABASE_KEY = "SUPABASE_KEY"
TOKEN_FILE = os.path.join(".agent", "Token..txt")
SEED_CSV = "heavy_mine_20260113.csv"
DB_TABLE = "grich_keywords_pool"

def get_supabase_client():
    """Loads Supabase credentials from environment variables or local file."""
    supabase_url = os.environ.get(ENV_SUPABASE_URL)
    supabase_key = os.environ.get(ENV_SUPABASE_KEY)
    
    if supabase_url and supabase_key:
        print("✅ Found credentials in environment variables.")
        return create_client(supabase_url, supabase_key)

    print("⚠️  Could not find environment variables, trying local token file...")
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(f"Local token file not found at {TOKEN_FILE}")

    config = {}
    with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if "Project URL:" in line:
                config['url'] = line.split("Project URL:")[1].strip()
            if "Secret keys:" in line:
                config['key'] = line.split("Secret keys:")[1].strip()
    
    if 'url' not in config or 'key' not in config:
        raise ValueError("Token file is incomplete.")
        
    print(f"✅ Found credentials in {TOKEN_FILE}.")
    return create_client(config['url'], config['key'])

def read_seed_keywords():
    """Reads seed keywords from the specified CSV file."""
    if not os.path.exists(SEED_CSV):
        raise FileNotFoundError(f"Seed file not found: {SEED_CSV}")
    
    with open(SEED_CSV, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        seeds = [row[0].strip().lower() for row in reader if row and row[0].strip()]
    print(f"🧬 Read {len(seeds)} seed keywords from {SEED_CSV}.")
    return seeds

def audit_database(supabase, seeds):
    """Compares seeds with database content and prints a report."""
    print("\nDATABASE AUDIT REPORT")
    print("=======================")
    
    try:
        # Fetch all keywords from the database
        print("⏳ Fetching all keywords from the database... (this may take a moment)")
        response = supabase.table(DB_TABLE).select("keyword").execute()
        
        if not response.data:
            print("❌ Database is empty. No keywords found.")
            return

        db_keywords = {item['keyword'].lower() for item in response.data if item.get('keyword')}
        print(f"📊 Found {len(db_keywords)} total keywords in the database.")
        print("---")

        total_matches = 0
        seeds_with_matches = 0

        # Check each seed
        for seed in seeds:
            matches = [kw for kw in db_keywords if kw.startswith(seed)]
            match_count = len(matches)
            
            if match_count > 0:
                print(f"✅ Found {match_count} keywords derived from seed: '{seed}'")
                total_matches += match_count
                seeds_with_matches += 1
            else:
                print(f"❌ No keywords found for seed: '{seed}'")
        
        print("\n--- AUDIT SUMMARY ---")
        print(f"Total Seed Keywords Analyzed: {len(seeds)}")
        print(f"Seeds that produced results: {seeds_with_matches} ({seeds_with_matches/len(seeds):.1%})")
        print(f"Total keywords in DB derived from these seeds: {total_matches}")

    except Exception as e:
        print(f"🔥 An error occurred during the audit: {e}")


if __name__ == "__main__":
    try:
        supabase_client = get_supabase_client()
        seed_keywords = read_seed_keywords()
        audit_database(supabase_client, seed_keywords)
    except Exception as e:
        print(f"🔥 A critical error occurred: {e}")
