import pandas as pd
import random
import os

def sample_papers_to_files(csv_file='biorxiv_filtered.csv', output_dir='papers', num_samples=10):
    df = pd.read_csv(csv_file)
    
    sampled_papers = df.sample(n=num_samples, random_state=42)
    
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, row in sampled_papers.iterrows():
        paper_id = row['paper_id']
        title = row['title']
        authors = row['authors']
        abstract = row['abstract']
        text_content = row['text'] if pd.notna(row['text']) else ""
        
        content = f"Title: {title}\n\n"
        content += f"Authors: {authors}\n\n"
        content += f"Abstract:\n{abstract}\n\n"
        
        if text_content:
            content += f"Full Text:\n{text_content}\n"
        
        safe_title = str(title) if pd.notna(title) else f"paper_{paper_id[:8]}"
        safe_title = "".join(c for c in safe_title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:100]
        filename = f"{safe_title}.txt"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Created: {filepath}")

if __name__ == "__main__":
    sample_papers_to_files()
    print("Sampling complete!")