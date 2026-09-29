import os
import google.generativeai as genai
from datetime import datetime
import csv

# --- PREPARE ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
course_lesson = "Analyzing latest signals..."

for cat in categories:
    try:
        res = model.generate_content(f"Luxury HTML report for {cat} trend. Wrap in <div class='filter-item filter-{cat}'>. No markdown.")
        clean_html = res.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_html + "\n"
        if cat == 'ai':
            lesson_res = model.generate_content(f"Write a 3-step masterclass lesson based on {cat} trends.")
            course_lesson = lesson_res.text
    except Exception as e:
        print(f"Error researching {cat}: {e}")

# --- THE INJECTION ---
try:
    with open("index.html", "r") as f:
        html = f.read()

    # THE NEW BULLETPROOF MARKER
    marker = '<!-- SIGNAL_INJECTION_MARKER -->'
    
    if marker in html:
        print("✅ Marker found. Injecting content...")
        # We replace the marker with the new content + the marker again (so it's ready for tomorrow)
        new_html = html.replace(marker, all_new_content + "\n" + marker)
        with open("index.html", "w") as f:
            f.write(new_html)
    else:
        print("❌ ERROR: Marker NOT found in index.html. Check your HTML file.")

    # Update Course
    with open("course.html", "w") as f:
        f.write(f"<html><body style='background:#000;color:#fff;padding:50px;'><h1>Academy</h1>{course_lesson}</body></html>")

    # Update Log
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), "AUTOMATION_RUN", "SUCCESS"])

except Exception as e:
    print(f"File Error: {e}")
