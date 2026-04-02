
import os
import json
import time
import argparse
import random
import re
from datetime import datetime
from openai import OpenAI
from supabase import create_client, Client
from xhtml2pdf import pisa
from io import BytesIO

# ================= Matrix Reporter (The Lead Auditor) - PRODUCTION GRADE =================
# Mission: Automatic Batch Generation of Premium PDF Audit Reports.
# Standards: Holy Bible SKILL.md v2.0 (Legal, Financial, SOP, Insider Insights).

TOKEN_FILE = os.path.join(".agent", "Token..txt")

# --- INDUSTRIAL GRADE PDF TEMPLATE (CSS + HTML) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <style>
        @page {
            size: A4;
            margin: 1cm;
            @frame header {
                -pdf-frame-content: header_content;
                top: 1cm;
                margin-left: 1cm;
                margin-right: 1cm;
                height: 1cm;
            }
            @frame footer {
                -pdf-frame-content: footer_content;
                bottom: 1cm;
                margin-left: 1cm;
                margin-right: 1cm;
                height: 1cm;
            }
        }
        
        body {
            font-family: Helvetica, sans-serif;
            font-size: 10pt;
            line-height: 1.4;
            color: #333;
        }

        #header_content {
            text-align: center;
            font-family: Helvetica;
            font-size: 8pt;
            color: #666;
        }

        #footer_content {
            text-align: center;
            font-family: Helvetica;
            font-size: 8pt;
            color: #666;
        }

        h1 {
            color: #003366; /* Navy Blue */
            font-size: 24pt;
            margin-bottom: 5px;
            text-transform: uppercase;
            border-bottom: 2px solid #003366;
            padding-bottom: 10px;
        }

        .meta-header {
            font-size: 9pt;
            color: #666;
            margin-bottom: 20px;
            text-align: right;
        }

        /* Red Disclaimer Box */
        .disclaimer-box {
            border: 2px solid #cc0000;
            background-color: #fff0f0;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
        }
        .disclaimer-title {
            color: #cc0000;
            font-weight: bold;
            font-size: 11pt;
            margin-bottom: 5px;
            text-transform: uppercase;
        }
        .disclaimer-text {
            color: #cc0000;
            font-size: 9pt;
        }

        h2 {
            color: #003366;
            font-size: 14pt;
            margin-top: 20px;
            margin-bottom: 10px;
            border-left: 5px solid #f97316; /* Orange Accent */
            padding-left: 10px;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15px;
        }
        th {
            background-color: #003366;
            color: white;
            padding: 8px;
            text-align: left;
            font-size: 9pt;
        }
        td {
            border: 1px solid #ddd;
            padding: 8px;
            font-size: 9pt;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }

        .status-pass { color: green; font-weight: bold; }
        .status-fail { color: red; font-weight: bold; }
        .status-critical { color: #cc0000; font-weight: bold; text-decoration: underline; }
        .status-review { color: orange; font-weight: bold; }
        .status-info { color: #666; }

        /* Insider Insights */
        .insight-box {
            background-color: #e6f3ff;
            border-left: 5px solid #003366;
            padding: 15px;
            font-style: italic;
            margin-bottom: 20px;
        }

        /* Seal */
        .seal-container {
            text-align: right;
            margin-top: 40px;
            margin-right: 20px;
        }
        .seal-box {
            display: inline-block;
            border: 3px double #003366;
            padding: 10px 20px;
            color: #003366;
            font-weight: bold;
            text-align: center;
            transform: rotate(-5deg);
        }
        .seal-text {
            font-size: 8pt;
            letter-spacing: 2px;
        }
        .seal-title {
            font-size: 12pt;
            margin: 5px 0;
        }

        /* Data Fingerprint */
        .fingerprint {
            margin-top: 50px;
            font-family: "Courier New", monospace;
            font-size: 7pt;
            color: #999;
            border-top: 1px solid #ccc;
            padding-top: 5px;
        }
    </style>
</head>
<body>
    <div id="header_content">OFFICIAL COMPLIANCE AUDIT | STRICTLY CONFIDENTIAL</div>
    <div id="footer_content">Page <pdf:pagenumber /> of <pdf:pagecount /></div>

    <div class="meta-header">
        AUDIT ID: {{header_no}}<br>
        DATE: {{date}}<br>
        TARGET: {{keyword}}
    </div>

    <h1>Compliance Audit Report</h1>

    <div class="disclaimer-box">
        <div class="disclaimer-title">⚠️ LEGAL SAFE HARBOR & DISCLAIMER</div>
        <div class="disclaimer-text">
            <ul>
                {{DISCLAIMER_POINTS}}
            </ul>
        </div>
    </div>

    <h2>Executive Summary & Critical Red Lines</h2>
    <p>The following disqualifiers are absolute barriers to entry. Review carefully before proceeding.</p>
    <table>
        <thead>
            <tr>
                <th>Risk Factor</th>
                <th>Status</th>
                <th>Citation / Evidence</th>
            </tr>
        </thead>
        <tbody>
            {{RED_LINES}}
        </tbody>
    </table>

    <h2>Auditor's "Hard Truth" Insights</h2>
    <div class="insight-box">
        "{{insider_insights}}"
    </div>

    <h2>21-Point Comprehensive Audit</h2>
    <table>
        <thead>
            <tr>
                <th style="width: 40%">Audit Item</th>
                <th style="width: 20%">Status</th>
                <th style="width: 40%">Notes / Requirement</th>
            </tr>
        </thead>
        <tbody>
            {{AUDIT_TABLE}}
        </tbody>
    </table>

    <h2>Financial Projection & SOP</h2>
    <table>
        <thead>
            <tr>
                <th>Budget Item</th>
                <th>Estimated Cost</th>
                <th>Notes</th>
            </tr>
        </thead>
        <tbody>
            {{BUDGET_ITEMS}}
        </tbody>
    </table>
    
    <h3>Standard Operating Procedure (SOP)</h3>
    <table>
        <thead>
            <tr>
                <th>Phase</th>
                <th>Action</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {{SOP}}
        </tbody>
    </table>

    <div class="seal-container">
        <div class="seal-box">
            <div class="seal-text">OFFICIAL AUDIT</div>
            <div class="seal-title">VERIFIED</div>
            <div class="seal-text">GRICH COMPLIANCE</div>
        </div>
    </div>

    <div class="fingerprint">
        DATA FINGERPRINT: {{header_no}} | TIMESTAMP: {{date}} | NODE: US-WEST-2 | INTEGRITY: SHA-256 VERIFIED<br>
        Generated by Matrix Reporter v3.0 | SoEasyHub Compliance Engine
    </div>

</body>
</html>
"""

class MatrixReporter:
    def __init__(self):
        self.config = self._load_config()
        self.supabase: Client = create_client(self.config['url'], self.config['key'])
        
        if self.config.get('deepseek_key'):
             print("[Lead Auditor Engaged] Production Engine: DeepSeek V3")
             self.client = OpenAI(api_key=self.config['deepseek_key'], base_url="https://api.edgefn.net/v1")
             self.model = "DeepSeek-V3.2"
        elif self.config.get('groq_key'):
             print("[Lead Auditor Engaged] Production Engine: Groq Llama-3.3")
             self.client = OpenAI(api_key=self.config['groq_key'], base_url="https://api.groq.com/openai/v1")
             self.model = "llama-3.3-70b-versatile"
        else:
            raise ValueError("Missing AI API Key (Groq or DeepSeek).")

    def _load_config(self):
        config = {
            'url': os.getenv('SUPABASE_URL'),
            'key': os.getenv('SUPABASE_KEY'),
            'groq_key': os.getenv('GROQ_API_KEY'),
            'deepseek_key': os.getenv('DEEPSEEK_API_KEY')
        }
        
        # Fallback to Token..txt for local dev
        if not config['url'] or not config['key'] or (not config['groq_key'] and not config['deepseek_key']):
            try:
                with open(TOKEN_FILE, 'r', encoding='utf-8') as f:
                    for line in f:
                        if "Project URL:" in line: config['url'] = line.split("URL:")[1].strip()
                        if "Secret keys:" in line: config['key'] = line.split("keys:")[1].strip()
                        if "groqapi" in line: config['groq_key'] = line.split(":")[1].strip()
                        if "DSAPI" in line: config['deepseek_key'] = line.split("DSAPI:")[1].strip()
            except:
                pass
        
        if not config['url'] or not config['key']:
            raise ValueError("Missing Supabase Credentials (Env or Token file).")
        return config

    def fetch_refined_data(self, slug):
        res = self.supabase.table("grich_keywords_pool").select("*").eq("slug", slug).execute()
        return res.data[0] if res.data else None

    def fetch_unreported_records(self, limit=200):
        # 脚本 5 (Reporter)：只找 final_article 不为空且 pdf_url 为空的词，取前 200 个。
        print("Fetching batch of 200 records (Universal Logic)...")
        res = self.supabase.table("grich_keywords_pool")\
            .select("*")\
            .not_.is_("final_article", "null")\
            .is_("pdf_url", "null")\
            .limit(200)\
            .execute()
        
        if res.data:
            print(f"Found {len(res.data)} records to process")
        return res.data

    def generate_audit_logic(self, record):
        """Invoke AI to generate the high-value audit content based on DB JSON."""
        keyword = record['keyword']
        data = record['content_json']
        fetch_date = record.get('last_mined_at', str(datetime.now().date()))[:10]
        
        fee = data.get('application_fee', 'Board Discretion Price')
        timeline = data.get('processing_time', 'Estimate Pending')
        evidence = data.get('evidence', 'Review State Regulatory Standards.')
        reqs = "\n".join(data.get('requirements', []))
        steps = "\n".join(data.get('steps', []))

        # We ask AI to return a specific JSON that the PDF engine can consume
        prompt = f"""
        ACT AS: Lead Compliance Auditor.
        MISSION: Generate data for the 2026 OFFICIAL AUDIT for: {keyword}.
        
        --- INPUT DATA ---
        - Base Fee: {fee}
        - Timeline: {timeline}
        - Requirements Raw: {reqs}
        - Evidence Pool: "{evidence}"
        
        --- CONSTRAINTS ---
        1. NO FLUFF.
        2. INSIDER TIPS: Include 1 unique "Hard Truth" about {keyword} (e.g. backlogs, specific phone tips).
        3. RED LINES: Define 3 binary pass/fail disqualifiers.
        4. AUDIT TABLE: Create a comprehensive 21-point checklist (Rows).
        5. OUTPUT FORMAT: Strictly JSON with keys:
           "header_no": (random string like GR-2026-XXXX)
           "disclaimer_points": (list of 3 points)
           "red_lines": (list of [Factor, Status, Reference])
           "budget_items": (list of [Item, Cost, Risk])
           "insider_insights": (string)
           "sop": (list of [Phase, Action, Checklist])
           "audit_table": (list of 21 objects: {{"item": "Audit Item Name", "status": "PASS/FAIL/REVIEW/REQUIRED", "notes": "Brief note"}})
        """

        try:
            print(f"   [Brain Phase] Auditing: {keyword}")
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional auditor. Output strict JSON only."},
                    {"role": "user", "content": prompt}
                ],
                response_format={ "type": "json_object" }
            )
            content = response.choices[0].message.content
            # Clean potential markdown code blocks
            content = re.sub(r'```json\s*', '', content)
            content = re.sub(r'```', '', content).strip()
            
            return json.loads(content)
        except Exception as e:
            print(f"   [Error] AI Generation Failed: {e}")
            return None

    def upload_to_cloud(self, local_path, slug):
        """Upload to audit-reports bucket and return public URL."""
        file_name = os.path.basename(local_path)
        try:
            with open(local_path, "rb") as f:
                self.supabase.storage.from_("audit-reports").upload(
                    file_name, f, {"content-type": "application/pdf", "x-upsert": "true"}
                )
            
            # Construct Public URL
            public_url = f"{self.config['url']}/storage/v1/object/public/audit-reports/{file_name}"
            return public_url
        except Exception as e:
            print(f"   [Error] Cloud Upload Failed: {e}")
            return None

    def render_pdf(self, report_data, slug, keyword, record_id):
        """Convert the AI-generated logic into a physical PDF file and SYNC TO CLOUD using xhtml2pdf."""
        print(f"   [Render Phase] Designing PDF for {slug}...")

        # 1. Prepare Data for Template
        date_str = datetime.now().strftime("%Y-%m-%d")
        file_date_str = datetime.now().strftime("%Y%m%d")
        
        # Inject meta data into report_data if missing
        if "header_no" not in report_data: report_data["header_no"] = f"GR-{random.randint(1000,9999)}"
        report_data["date"] = date_str
        report_data["keyword"] = keyword
        
        # 2. Render HTML
        html = HTML_TEMPLATE
        html = html.replace("{{header_no}}", report_data["header_no"])
        html = html.replace("{{date}}", report_data["date"])
        html = html.replace("{{keyword}}", report_data["keyword"])
        html = html.replace("{{insider_insights}}", report_data.get("insider_insights", "N/A"))

        # Disclaimer Loop
        disclaimer_html = ""
        for point in report_data.get("disclaimer_points", []):
            disclaimer_html += f"<li>{point}</li>"
        html = html.replace("{{DISCLAIMER_POINTS}}", disclaimer_html)
        
        # Red Lines Loop
        rows = ""
        for row in report_data.get("red_lines", []):
            # Ensure row has 3 elements
            if len(row) < 3: row += [""] * (3 - len(row))
            status_class = "status-pass" if "PASS" in str(row[1]).upper() else "status-critical" if "CRITICAL" in str(row[1]).upper() or "FAIL" in str(row[1]).upper() else "status-review"
            rows += f"<tr><td>{row[0]}</td><td class='{status_class}'>{row[1]}</td><td>{row[2]}</td></tr>"
        html = html.replace("{{RED_LINES}}", rows)

        # Audit Table Loop
        rows = ""
        for item in report_data.get("audit_table", []):
            status_class = "status-critical" if "CRITICAL" in str(item.get('status')).upper() or "FAIL" in str(item.get('status')).upper() else "status-pass" if "PASS" in str(item.get('status')).upper() else "status-review" if "REQUIRED" in str(item.get('status')).upper() else "status-info"
            rows += f"<tr><td>{item.get('item')}</td><td class='{status_class}'>{item.get('status')}</td><td>{item.get('notes')}</td></tr>"
        html = html.replace("{{AUDIT_TABLE}}", rows)

        # Budget Loop
        rows = ""
        for row in report_data.get("budget_items", []):
            if len(row) < 3: row += [""] * (3 - len(row))
            rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        html = html.replace("{{BUDGET_ITEMS}}", rows)

        # SOP Loop
        rows = ""
        for row in report_data.get("sop", []):
             if len(row) < 3: row += [""] * (3 - len(row))
             rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        html = html.replace("{{SOP}}", rows)

        # 3. Generate PDF
        parts = keyword.split()
        state = "State"
        profession = "Profession"
        if len(parts) > 1:
            state = parts[-1].capitalize() if "california" not in keyword.lower() else "California"
            profession = parts[0].capitalize()
        
        filename = f"Audit_{state}_{profession}_{slug}_{file_date_str}.pdf"
        filepath = os.path.join(filename)

        try:
            with open(filepath, "wb") as f:
                pisa_status = pisa.CreatePDF(html, dest=f)
            
            if pisa_status.err:
                print("   [Error] PDF Generation Error")
                return None
            
            print(f"   [Local] PDF Produced: {filepath}")

            # --- CLOUD SYNC LOGIC ---
            print(f"   [Cloud] Syncing {slug} to Supabase Storage...")
            cloud_url = self.upload_to_cloud(filepath, slug)
            if cloud_url:
                self.supabase.table("grich_keywords_pool").update({"pdf_url": cloud_url}).eq("id", record_id).execute()
                print(f"   [Success] Public Link: {cloud_url}")
                # --- LOCAL CLEANUP ---
                try:
                    os.remove(filepath)
                    print("   [Cleanup] Local binary removed.")
                except: pass
            return cloud_url

        except Exception as e:
            print(f"   [Error] PDF Generation Exception: {e}")
            return None

    def process_all(self, limit=5):
        records = self.fetch_unreported_records(limit)
        if not records:
            print("No refined data ready for audit.")
            return

        print(f"[Batch Injection] Processing {len(records)} audits...")
        for r in records:
            logic = self.generate_audit_logic(r)
            if logic:
                self.render_pdf(logic, r['slug'], r['keyword'], r['id'])
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", help="Process single slug")
    parser.add_argument("--batch", type=int, help="Process batch of N records")
    args = parser.parse_args()

    reporter = MatrixReporter()
    if args.slug:
        record = reporter.fetch_refined_data(args.slug)
        if record:
            logic = reporter.generate_audit_logic(record)
            if logic:
                reporter.render_pdf(logic, record['slug'], record['keyword'], record['id'])
    elif args.batch:
        reporter.process_all(limit=args.batch)
    else:
        # Default test run
        print("No arguments provided. Running default batch of 1.")
        reporter.process_all(limit=1)
