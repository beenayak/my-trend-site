import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. SETUP
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# We use gemini-1.5-flash for maximum stability in automation
model = genai.GenerativeModel('gemini-1.5-flash')

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

for cat in categories:
    print(f"Researching {cat}...")
    display_name = "Synthetic Intelligence" if cat == 'ai' else cat.capitalize()
    
    prompt = f"Research a breakthrough trend in {cat}. Return ONLY a luxury HTML div for SIGNAL Labs. No markdown code blocks, just the HTML code."

    try:
        response = model.generate_content(prompt)
        # CLEANER: Removes ```html or ``` if the AI accidentally adds them
        clean_content = response.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_content + "\n"
        log_entries.append([datetime.now().strftime("%Y-%m-%d"), cat.upper(), "Update Successful", "LIVE"])
    except Exception as e:
        print(f"Error with {cat}: {e}")

# 2. INJECTION
try:
    with open("index.html", "r") as f:
        html = f.read()

    # MUST match your index.html exactly
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-32" id="trend-container">'
    
    if marker in html:
        updated_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(updated_html)
    
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(log_entries)

except Exception as e:
    print(f"File Error: {e}")

print("Automation Complete.")
