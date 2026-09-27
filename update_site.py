import os
import google.generativeai as genai
from datetime import datetime
import csv

# --- PHASE 1: IMMEDIATE FILE INITIALIZATION ---
# This ensures Git ALWAYS finds these files, even if the AI fails
required_files = {
    'log.csv': 'Timestamp,Category,Status\n',
    'sitemap.xml': '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>',
    'course.html': '<html><body>Initialising...</body></html>'
}

for filename, default_content in required_files.items():
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(default_content)
        print(f"Initialized missing file: {filename}")

# --- PHASE 2: AI SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # Auto-select best available model
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = models[0] if models else 'gemini-1.5-flash'
except:
    model_name = 'gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# --- PHASE 3: RESEARCH & COURSE GEN ---
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
course_lesson = "Masterclass content pending..."

for cat in categories:
    try:
        # Website Article
        res = model.generate_content(f"Luxury HTML report for {cat} trend. No markdown.")
        clean_html = res.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_html + "\n"
        
        # Course Lesson (Money Maker)
        if cat == 'ai':
            lesson_res = model.generate_content(f"Write a 3-step 'Masterclass Lesson' for a high-ticket course based on {cat} trends.")
            course_lesson = lesson_res.text
    except Exception as e:
        print(f"Error researching {cat}: {e}")

# --- PHASE 4: SECURE FILE WRITING ---
try:
    # Update Homepage
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            html = f.read()
        marker = 'id="trend-container">'
        if marker in html:
            with open("index.html", "w") as f:
                f.write(html.replace(marker, marker + "\n" + all_new_content))

    # Update Course Page (The Automated Product)
    with open("course.html", "w") as f:
        f.write(f"""
        <html><head><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-black text-white p-20 font-serif">
            <h1 class="text-5xl italic font-black uppercase mb-5">Signal Academy</h1>
            <p class="text-slate-500 tracking-widest mb-10">Module: {datetime.now().strftime('%Y-%m-%d')}</p>
            <div class="max-w-2xl text-xl leading-relaxed border-l-2 border-white pl-8">{course_lesson}</div>
            <div class="mt-20 p-10 border border-slate-800 bg-slate-900">
                <p class="mb-6 text-slate-400 font-bold uppercase tracking-widest">Enroll in the Full Protocol</p>
                <a href="https://gumroad.com" class="bg-white text-black px-8 py-4 font-bold uppercase">Unlock Certification $97</a>
            </div>
        </body></html>
        """)

    # Update Log
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), "AUTOMATION_RUN", "SUCCESS"])

except Exception as e:
    print(f"Writing error: {e}")
