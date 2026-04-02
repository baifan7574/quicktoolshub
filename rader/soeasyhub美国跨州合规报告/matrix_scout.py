import os
import time
import random
import re
import json
import requests
import csv
import sys
from datetime import datetime, timezone
from supabase import create_client, Client

# Force UTF-8 output for Windows CMD
sys.stdout.reconfigure(encoding='utf-8')

# ================= Configuration & Constants =================
TOKEN_FILE = os.path.join(".agent", "Token..txt")  # Fallback for local development
SKILL_FILE = os.path.join(".agent", "skills", "01-grich-miner", "SKILL.md")
SEED_CSV = "heavy_mine_20260113.csv"

# Environment variable names for cloud deployment
ENV_SUPABASE_URL = "SUPABASE_URL"
ENV_SUPABASE_KEY = "SUPABASE_KEY"
ENV_DEEPSEEK_API_KEY = "DEEPSEEK_API_KEY"
ENV_GROQ_API_KEY = "GROQ_API_KEY"

# V42.4 Dyeing Protocol
DYE_MAP = [
    (r"lawyer|attorney|bar\s?exam|legal|juris", "Law", "Blue"),
    (r"nurse|doctor|medical|clinic|rn|lpn|physician|health|surgery", "Medical", "Green"),
    (r"accountant|cpa|finance|audit|tax|acc", "Finance", "Black"),
    (r"teacher|education|school|pedagog|tutor|tefl", "Education", "Orange"),
    (r"real\s?estate|realtor|broker|property", "RealEstate", "Red"),
    (r"engineer|architect|civil|structur|mechanic", "Engineer", "Cyan"),
    (r"electrician|hvac|plumb|welder|construct|wireman|journeyman", "Trades", "Yellow")
]

STATES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
    "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS", "missouri": "MO",
    "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH",
    "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
    "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
    "dc": "DC", "district of columbia": "DC"
}

class GrichMiner:
    def __init__(self):
        self.config = self._load_config()
        self.supabase: Client = create_client(self.config['url'], self.config['key'])
        print(f"🔌 Connected to Supabase: {self.config['url']}", flush=True)
        
        self.ua_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        ]

    def _load_config(self):
        config = {}
        
        # Priority 1: Read from environment variables (cloud deployment)
        supabase_url = os.environ.get(ENV_SUPABASE_URL)
        supabase_key = os.environ.get(ENV_SUPABASE_KEY)
        
        if supabase_url and supabase_key:
            config['url'] = supabase_url
            config['key'] = supabase_key
            print("✅ Config loaded from environment variables.", flush=True)
            return config
        
        # Priority 2: Fallback to local Token file (development)
        token_path = None
        if os.path.exists(TOKEN_FILE):
            token_path = TOKEN_FILE
        else:
            # Try alternative relative path
            alt_path = os.path.join("..", ".agent", "Token..txt")
            if os.path.exists(alt_path):
                token_path = alt_path
        
        if not token_path:
            raise FileNotFoundError(
                f"Critical: {TOKEN_FILE} not found and environment variables {ENV_SUPABASE_URL}/{ENV_SUPABASE_KEY} not set."
            )
        
        with open(token_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                if "Project URL:" in line:
                    config['url'] = line.split("Project URL:")[1].strip()
                if "Secret keys:" in line:
                    config['key'] = line.split("Secret keys:")[1].strip()
        
        if 'url' not in config or 'key' not in config:
            raise ValueError("Configuration incomplete. Check Token..txt or environment variables.")
        
        print("⚠️  Config loaded from local Token file (development mode).", flush=True)
        return config

    def load_csv_seeds(self):
        """Inject Fuel from CSV"""
        seeds = []
        if not os.path.exists(SEED_CSV):
            print(f"⚠️ Warning: {SEED_CSV} not found. Falling back to defaults.")
            return ["nursing license reciprocity Texas"] # Fallback

        try:
            with open(SEED_CSV, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None) # Skip header
                for row in reader:
                    if row and row[0].strip():
                        seeds.append(row[0].strip())
            print(f"⛽ FUEL INJECTED: Loaded {len(seeds)} seeds from valid CSV source.")
            return seeds
        except Exception as e:
            print(f"❌ CSV Load Error: {e}")
            return []

    def fetch_suggestions(self, query):
        """Google Autocomplete API"""
        url = f"https://www.google.com/complete/search?client=chrome&q={query}"
        # Random User Agent Rotation
        headers = {"User-Agent": random.choice(self.ua_list)}
        try:
            res = requests.get(url, headers=headers, timeout=5)
            if res.status_code == 200:
                try:
                    suggestions = json.loads(res.text)[1]
                    # print(f"      🔍 Suggestions for '{query}': {suggestions}")
                    return suggestions
                except Exception as json_err:
                    print(f"      ⚠️  JSON Parse Error for '{query}': {json_err}")
                    return []
            else:
                print(f"      ⚠️  HTTP Error {res.status_code} for '{query}'")
                return []
        except Exception as e:
            print(f"      ⚠️  Request Error for '{query}': {e}")
            time.sleep(5) # Backoff on error
            return []

    def generate_slug(self, text):
        """Slug Processing"""
        text = text.lower().strip()
        text = re.sub(r'[^a-z0-9\s]', '', text)
        slug = re.sub(r'\s+', '-', text)
        return slug

    def extract_state(self, text):
        """Extract US State from text"""
        text_lower = text.lower()
        # Check for full names
        for state_name, state_code in STATES.items():
            if re.search(r'\b' + re.escape(state_name) + r'\b', text_lower):
                return state_code
        return None

    def dye_keyword(self, keyword, seed_context=None):
        """V42.4 Dyeing Protocol with Context Inheritance"""
        keyword_lower = keyword.lower()
        
        # 1. Direct Regex Match
        for pattern, category, color in DYE_MAP:
            if re.search(pattern, keyword_lower):
                return category, color
        
        # 2. Context Inheritance
        if seed_context:
            return seed_context.get('category'), seed_context.get('color')

        return "Uncategorized", "Gray" 

    def save_keyword(self, keyword, seed_context=None):
        """Upsert keyword to Supabase"""
        slug = self.generate_slug(keyword)
        # Inherit context safely
        category, color_tag = self.dye_keyword(keyword, seed_context)
        state = self.extract_state(keyword)
        
        if not state:
            if seed_context and seed_context.get('state'):
                state = seed_context['state']
            else:
               state = "Unknown"

        data = {
            "keyword": keyword,
            "slug": slug,
            "category": category,
            "color_tag": color_tag,
            "state": state,
            "is_downloaded": False,
            "is_refined": False,
            "last_mined_at": datetime.now(timezone.utc).isoformat()
        }

        try:
            self.supabase.table("grich_keywords_pool").upsert(data, on_conflict="slug").execute()
            print(f"      ✅ Saved: {keyword}")
            return True
        except Exception as e:
            print(f"      ❌ Failed to save '{keyword}': {e}")
            return False

    def analyze_seed_context(self, seed_text):
        """Determine category/color/state for a seed"""
        cat, col = self.dye_keyword(seed_text)
        st = self.extract_state(seed_text)
        return {"category": cat, "color": col, "state": st}

    def recursive_mine(self):
        """
        FULL THROTTLE: Seed + [a-z] + [a-z] (FULL)
        """
        print(f"🚀 Grich Miner V42.4 FULL THROTTLE MODE.")
        print("Protocol: CSV Injection | Full Alpha L3 | Anti-Ban Enabled")
        
        seeds = self.load_csv_seeds()
        if not seeds:
            print("No seeds loaded. Aborting.")
            return

        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        total_seeds = len(seeds)
        count = 0

        for seed in seeds:
            count += 1
            # Recalculate context for each seed to ensure accuracy
            seed_context = self.analyze_seed_context(seed)
            print(f"\n[{count}/{total_seeds}] 🔥 ROOT JOB: {seed} (Category: {seed_context.get('category')}, State: {seed_context.get('state')})")

            # === Layer 1: Base Suggestions ===
            l1_suggestions = self.fetch_suggestions(seed)
            self.process_batch(l1_suggestions, seed_context, layer=1)

            # === Layer 2: Alpha Expansion (Seed + a) ===
            shuffled_alpha = list(alphabet)
            random.shuffle(shuffled_alpha)
            
            for char1 in shuffled_alpha:
                query_l2 = f"{seed} {char1}"
                # print(f"   [L2] Querying: {query_l2}")
                l2_suggestions = self.fetch_suggestions(query_l2)
                self.process_batch(l2_suggestions, seed_context, layer=2)
                
                # === Layer 3: Full Alpha Expansion (Seed + a + b) ===
                if l2_suggestions:
                    # Full Alpha - Random Order
                    sub_alpha = list(alphabet)
                    random.shuffle(sub_alpha) 
                    
                    for char2 in sub_alpha:
                            query_l3 = f"{seed} {char1}{char2}"
                            # print(f"      [L3] Querying: {query_l3}")
                            l3_suggestions = self.fetch_suggestions(query_l3)
                            self.process_batch(l3_suggestions, seed_context, layer=3)
                            
                            # Anti-Ban Delay (1.2 - 2.5s)
                            time.sleep(random.uniform(1.2, 2.5)) 
                
                # Layer 2 Delay (2.0 - 4.0s)
                time.sleep(random.uniform(2.0, 4.0)) 

    def process_batch(self, keywords, context, layer):
        if not keywords: return
        print(f"   [L{layer}] Processing {len(keywords)} keywords...")
        for kw in keywords:
            self.save_keyword(kw, context)

if __name__ == "__main__":
    try:
        miner = GrichMiner()
        miner.recursive_mine()
    except Exception as e:
        print(f"🔥 CRITICAL FAILURE: {e}")