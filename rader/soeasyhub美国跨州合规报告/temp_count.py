import os
import json
from supabase import create_client

def main():
    config = {}
    try:
        with open('.agent/Token..txt', 'r', encoding='utf-8') as f:
            for line in f:
                if 'Project URL:' in line:
                    config['url'] = line.split('URL:')[1].strip()
                if 'Secret keys:' in line:
                    config['key'] = line.split('keys:')[1].strip()
    except Exception as e:
        print("Error reading token file:", e)
        return

    try:
        sb = create_client(config['url'], config['key'])
    except Exception as e:
        print("Error creating client:", e)
        return

    both_count = 0
    article_only = 0
    pdf_only = 0
    total = 0

    try:
        # Loop to get all
        offset = 0
        limit = 1000
        while True:
            res = sb.table('grich_keywords_pool').select('id, final_article, pdf_url').range(offset, offset + limit - 1).execute()
            data = res.data
            if not data:
                break
            
            for row in data:
                total += 1
                has_article = row.get('final_article') is not None
                has_pdf = row.get('pdf_url') is not None
                if has_article and has_pdf:
                    both_count += 1
                elif has_article:
                    article_only += 1
                elif has_pdf:
                    pdf_only += 1
            
            if len(data) < limit:
                break
            offset += limit

        print(f"Total rows retrieved: {total}")
        print(f"Rows with BOTH Article AND PDF: {both_count}")
        print(f"Rows with Article ONLY: {article_only}")
        print(f"Rows with PDF ONLY: {pdf_only}")
    except Exception as e:
        print("Error fetching data:", e)

if __name__ == '__main__':
    main()
