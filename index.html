import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. SETUP
# Make sure GEMINI_API_KEY is in your GitHub Secrets!
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("API Key missing! Check your GitHub Secrets.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

# 2. THE ENGINE
for cat in categories:
    try:
        print(f"Researching {cat}...")
        prompt = f"""
        ACT AS: Lead Strategic Analyst at SIGNAL. Labs.
        TASK: Research one breakthrough trend regarding {cat}. 
        Format as a luxury HTML block. Replace [IMAGE] with a real Unsplash URL like https://images.unsplash.com/photo-[ID]?auto=format&fit=crop&q=80&w=800.
        
        OUTPUT ONLY THE HTML DIV with class 'filter-item filter-{cat}'. 
        Include a black 'Access Protocol' button.
        """

        response = model.generate_content(prompt)
        content = response.text
        all_new_content += content + "\n"
        
        log_entries.append([datetime.now().strftime("%Y-%m-%d"), cat.upper(), "Update Successful", "LIVE"])
    except Exception as e:
        print(f"Error researching {cat}: {e}")

# 3. UPDATE index.html
try:
    with open("index.html", "r") as f:
        html = f.read()

    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-24" id="trend-container">'
    if marker in html:
        updated_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(updated_html)
    else:
        print("Marker not found in index.html. Check your HTML structure.")

    # 4. UPDATE log.csv
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(log_entries)

    # 5. SITEMAP
    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
      <url><loc>https://{os.environ.get('GITHUB_ACTOR', 'user')}.github.io/SIGNAL/</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>
    </urlset>"""
    with open("sitemap.xml", "w") as f:
        f.write(sitemap_content)

except Exception as e:
    print(f"File writing error: {e}")

print("Automation sequence complete.")
