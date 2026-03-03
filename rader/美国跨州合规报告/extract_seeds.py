import csv
import os

def extract_seeds():
    input_file = '../scenro/professions.csv'
    output_file = 'heavy_mine_20260113.csv'
    
    unique_professions = set()
    
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                profession = row['profession'].strip()
                if profession:
                    unique_professions.add(profession)
    except FileNotFoundError:
        print(f"Error: File {input_file} not found.")
        return

    print(f"Found {len(unique_professions)} unique professions.")
    
    # Generate optimized seed keywords
    # Strategies:
    # 1. The profession itself
    # 2. "best [profession]"
    # 3. "[profession] near me"
    # 4. "cheap [profession]"
    # 5. "how to find [profession]"
    # 6. "[profession] cost"
    
    seed_keywords = []
    
    # Sort for consistency
    sorted_professions = sorted(list(unique_professions))
    
    for profession in sorted_professions:
        # Core term
        seed_keywords.append(profession)
        
        # Intent-based variations (high volume potential)
        seed_keywords.append(f"best {profession}")
        seed_keywords.append(f"{profession} near me")
        seed_keywords.append(f"cheap {profession}")
        seed_keywords.append(f"affordable {profession}")
        
        # Information seeking
        seed_keywords.append(f"{profession} cost")
        seed_keywords.append(f"{profession} prices")
        seed_keywords.append(f"{profession} salary") # Often searched
        seed_keywords.append(f"{profession} requirements")
        seed_keywords.append(f"how to become a {profession}")

    # Write to output file
    with open(output_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['seed_keyword'])
        for keyword in seed_keywords:
            writer.writerow([keyword])
            
    print(f"Generated {len(seed_keywords)} seed keywords in {output_file}")
    
    # Print a sample
    print("\nSample seeds:")
    for i in range(min(10, len(seed_keywords))):
        print(seed_keywords[i])

if __name__ == "__main__":
    extract_seeds()
