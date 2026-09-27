import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. MODEL RECOVERY LOGIC (Prevents 404)
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model_name = 'gemini-1.5-flash' # Default
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name # Finds the model your account is allowed to use
            break
except:
    pass

model = genai.GenerativeModel(model_name)

# 2. CATEGORIES & COURSE LOGIC
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
course_lesson = "Today's lesson is being prepared..."

for cat in categories:
    try:
        # Website Content
        res = model.generate_content(f"Luxury HTML report for {cat} trend. No markdown.")
        clean_html = res.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_html + "\n"
        
        # If it's AI, turn it into a Course Lesson
        if cat == 'ai':
            lesson_res = model.generate_content(f"Based on {cat} trends, write a 3-step business lesson for a $1,000 course.")
            course_lesson = lesson_res.text
    except:
        continue

# 3. WRITE THE FILES (Creating them if they don't exist)
try:
    # Update Homepage
    with open("index.html", "r") as f:
        html = f.read()
    marker = 'id="trend-container">'
    if marker in html:
        with open("index.html", "w") as f:
            f.write(html.replace(marker, marker + "\n" + all_new_content))

    # Update Course Page
    with open("course.html", "w") as f:
        f.write(f"<html><body style='background:#000;color:#fff;font-family:serif;padding:50px;'>")
        f.write(f"<h1>SIGNAL ACADEMY</h1><p>Lesson: {datetime.now().date()}</p>")
        f.write(f"<div style='border:1px solid #333;padding:20px;'>{course_lesson}</div>")
        f.write(f"<br><a href='#' style='color:gold;'>Unlock Full Certification</a></body></html>")

    # Create dummy sitemap if missing to satisfy Git
    if not os.path.exists("sitemap.xml"):
        with open("sitemap.xml", "w") as f:
            f.write("<urlset></urlset>")

except Exception as e:
    print(f"Error: {e}")
