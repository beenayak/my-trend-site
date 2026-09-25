import os
import google.generativeai as genai
from datetime import datetime
import csv

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Define categories
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

for cat in categories:
    print(f"Analyzing {cat} signal...")
    
    prompt = f"""
    ACT AS: Lead Strategic Analyst at SIGNAL. Research Labs.
    TASK: Research one breakthrough trend specifically regarding {cat}.
    
    [GENERATE_STORY_FOR_WEBSITE]
    Return ONLY an HTML block with a 3-word title and 3-sentence summary.
    Use the 'Access Protocol' button format.
    """

    response = model.generate_content(prompt)
    content = response.text
    all_new_content += content + "\n"

    # Extract a simple title for the spreadsheet (first 5 words of the response)
    # This part helps us "see" what the AI wrote in the log
    simple_title = " ".join(content.split()[:5]).replace("<", "").replace("div", "")
    
    # Store the log entry
    log_entries.append([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        cat.upper(),
        simple_title,
        "PUBLISHED"
    ])

# 1. Update the Website (HTML)
with open("index.html", "r") as f:
    html = f.read()

marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-24" id="trend-container">'
updated_html = html.replace(marker, marker + "\n" + all_new_content)

with open("index.html", "w") as f:
    f.write(updated_html)

# 2. Update the Spreadsheet (CSV)
file_exists = os.path.isfile('log.csv')
with open('log.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    # Write header if the file is new
    if not file_exists:
        writer.writerow(['Timestamp', 'Category', 'Subject/Title', 'Status'])
    # Write the new entries
    writer.writerows(log_entries)

print("SIGNAL update complete. Spreadsheet synced.")
