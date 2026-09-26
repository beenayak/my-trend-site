import os
import google.generativeai as genai
from datetime import datetime
import csv

def run_protocol():
    # 1. CHECK API KEY
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY is not set in GitHub Secrets.")
        return

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        print(f"❌ ERROR: Failed to initialize Gemini: {e}")
        return

    # 2. CHECK index.html
    if not os.path.exists("index.html"):
        print("❌ ERROR: index.html not found in the repository.")
        return

    with open("index.html", "r") as f:
        html = f.read()

    # THE MARKER - This must match your index.html exactly
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-32" id="trend-container">'
    
    if marker not in html:
        print("❌ ERROR: Could not find the 'trend-container' marker in index.html.")
        print("Ensure your index.html has the EXACT line: " + marker)
        return

    # 3. GENERATE CONTENT
    categories = ['health', 'capital', 'tech', 'ai']
    all_new_content = ""
    log_entries = []

    for cat in categories:
        try:
            print(f"--- Researching {cat.upper()} ---")
            display_name = "Synthetic Intelligence" if cat == 'ai' else cat.capitalize()
            prompt = f"Write a luxury 400-word SEO article for {cat}. Output only the HTML div for SIGNAL Labs."
            
            response = model.generate_content(prompt)
            all_new_content += response.text + "\n"
            log_entries.append([datetime.now().strftime("%Y-%m-%d"), cat.upper(), "SUCCESS", "LIVE"])
        except Exception as e:
            print(f"⚠️ WARNING: Failed to get content for {cat}: {e}")

    # 4. UPDATE FILES
    try:
        # Update HTML
        new_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(new_html)

        # Update CSV
        with open('log.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(log_entries)
            
        print("✅ SUCCESS: Website and Log updated.")
    except Exception as e:
        print(f"❌ ERROR: Failed to write files: {e}")

if __name__ == "__main__":
    run_protocol()
