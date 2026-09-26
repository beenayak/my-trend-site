import os
from google import genai # NEW SDK IMPORT
from datetime import datetime
import csv

# 1. INITIALIZE CLIENT
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) # NEW SYNTAX

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

# 2. THE ENGINE
for cat in categories:
    print(f"SIGNAL: Deep-researching {cat}...")
    display_name = "Synthetic Intelligence" if cat == 'ai' else cat.capitalize()
    
    # Updated Prompt for the new SDK
    prompt_text = f"Research a breakthrough trend in {cat}. Return ONLY a luxury HTML div for SIGNAL Labs. Focus on SEO."

    try:
        # NEW SYNTAX for generating content
        response = client.models.generate_content(
            model="gemini-1.5-flash", 
            contents=prompt_text
        )
        
        content = response.text
        all_new_content += content + "\n"
        
        log_entries.append([datetime.now().strftime("%Y-%m-%d"), cat.upper(), "Update Successful", "LIVE"])
    except Exception as e:
        print(f"Error researching {cat}: {e}")

# 3. FILE UPDATE LOGIC
try:
    with open("index.html", "r") as f:
        html = f.read()

    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-32" id="trend-container">'
    if marker in html:
        updated_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(updated_html)
    
    # Update CSV
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(log_entries)

    # Update Sitemap
    user = os.environ.get('GITHUB_ACTOR', 'user')
    sitemap = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{user}.github.io/SIGNAL/</loc></url></urlset>'
    with open("sitemap.xml", "w") as f:
        f.write(sitemap)

except Exception as e:
    print(f"File Error: {e}")

print("Protocol Complete.")
