import os
from xhtml2pdf import pisa

# Mock Data
mock_data = {
    "keyword": "California Electrician Reciprocity",
    "header_no": "GR-2026-TEST-001",
    "date": "2026-02-22",
    "disclaimer_points": [
        "This report is for informational purposes only and does not constitute legal advice.",
        "Regulations are subject to change without notice. Verify with the official board.",
        "The use of this report is at your own risk."
    ],
    "red_lines": [
        ["Criminal History", "CRITICAL", "Must disclose all convictions per Board Rule 12.4."],
        ["Experience Verification", "HIGH RISK", "Only W-2 forms accepted as proof of hours."],
        ["Reciprocity Agreement", "PASS", "California has no direct reciprocity with Texas."]
    ],
    "budget_items": [
        ["Application Fee", "$175.00", "Non-refundable"],
        ["Examination Fee", "$100.00", "Per attempt"],
        ["License Activation", "$200.00", "Upon passing"]
    ],
    "insider_insights": "The Board is currently rejecting 40% of applications due to incomplete experience verification forms. Ensure your Social Security Administration earnings report matches your claimed hours exactly.",
    "sop": [
        ["Phase 1: Preparation", "Gather W-2s and SSA Report", "Self-Audit"],
        ["Phase 2: Application", "Submit Form 123-E Online", "Pending Board Review"],
        ["Phase 3: Examination", "Schedule with PSI Exams", "Score 70%+"]
    ],
    "audit_table": [
        {"item": "Age Requirement", "status": "PASS", "notes": "Must be 18+"},
        {"item": "High School Diploma", "status": "PASS", "notes": "Required"},
        {"item": "Apprenticeship", "status": "CRITICAL", "notes": "8000 Hours Required"},
        {"item": "Exam Score", "status": "PENDING", "notes": "70% Minimum"},
        {"item": "Background Check", "status": "REQUIRED", "notes": "Live Scan Fingerprinting"},
        {"item": "Experience Affidavit", "status": "CRITICAL", "notes": "Signed by Master Electrician"},
        {"item": "Reciprocity State", "status": "FAIL", "notes": "No direct agreement"}
    ]
}

# HTML Template with "Industrial Grade" CSS
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

def render_template(template, data):
    html = template
    html = html.replace("{{header_no}}", data["header_no"])
    html = html.replace("{{date}}", data["date"])
    html = html.replace("{{keyword}}", data["keyword"])
    html = html.replace("{{insider_insights}}", data["insider_insights"])

    # Disclaimer Loop
    disclaimer_html = ""
    for point in data["disclaimer_points"]:
        disclaimer_html += f"<li>{point}</li>"
    html = html.replace("{{DISCLAIMER_POINTS}}", disclaimer_html)
    
    # Red Lines Loop
    rows = ""
    for row in data["red_lines"]:
        status_class = "status-pass" if "PASS" in row[1] else "status-critical" if "CRITICAL" in row[1] or "FAIL" in row[1] else "status-review"
        rows += f"<tr><td>{row[0]}</td><td class='{status_class}'>{row[1]}</td><td>{row[2]}</td></tr>"
    html = html.replace("{{RED_LINES}}", rows)

    # Audit Table Loop
    rows = ""
    for item in data["audit_table"]:
        status_class = "status-critical" if "CRITICAL" in item['status'] or "FAIL" in item['status'] else "status-pass" if "PASS" in item['status'] else "status-review" if "REQUIRED" in item['status'] else "status-info"
        rows += f"<tr><td>{item['item']}</td><td class='{status_class}'>{item['status']}</td><td>{item['notes']}</td></tr>"
    html = html.replace("{{AUDIT_TABLE}}", rows)

    # Budget Loop
    rows = ""
    for row in data["budget_items"]:
        rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html = html.replace("{{BUDGET_ITEMS}}", rows)

    # SOP Loop
    rows = ""
    for row in data["sop"]:
        rows += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    html = html.replace("{{SOP}}", rows)
    
    return html

def main():
    print("Generating PDF...")
    final_html = render_template(HTML_TEMPLATE, mock_data)
    
    output_filename = "test_audit_report.pdf"
    with open(output_filename, "wb") as f:
        pisa_status = pisa.CreatePDF(final_html, dest=f)
    
    if pisa_status.err:
        print("Error generating PDF")
    else:
        print(f"PDF generated successfully: {output_filename}")

if __name__ == "__main__":
    main()
