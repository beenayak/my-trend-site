import os
import google.generativeai as genai
from datetime import datetime
import csv

# --- STEP 1: INITIALIZE FILES (Prevents Git Error 128) ---
files_to_ensure = ['log.csv', 'sitemap.xml', 'course.html']
for file in files_to_ensure:
    if not os.path.exists(file):
        with open(file, 'w') as f:
            if file == 'log.csv': f.write("Timestamp,Category,Status\n")
            else: f.write("")

# --- STEP 2: MODEL RECOVERY ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # This finds the best model available on your specific account
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = models[0] if models else 'gemini-1.5-flash'
except:
    model_name = 'gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# --- STEP 3: CONTENT & COURSE GENERATION ---
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
course_lesson = "Analyzing latest signals..."

for cat in categories:
    try:
        # Generate Website Article
        res = model.generate_content(f"Luxury HTML report for {cat} trend. No markdown.")
        clean_html = res.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_html + "\n"
        
        # Generate Course Lesson (Optimization for Selling)
        if cat == 'ai':
            lesson_prompt = f"Write a 3-step 'Masterclass Lesson' for a high-ticket course based on: {clean_html[:100]}"
            lesson_res = model.generate_content(lesson_prompt)
            course_lesson = lesson_res.text
    except:
        continue

# --- STEP 4: UPDATE FILES ---
try:
    # Update index.html
    with open("index.html", "r") as f:
        html = f.read()
    marker = 'id="trend-container">'
    if marker in html:
        with open("index.html", "w") as f:
            f.write(html.replace(marker, marker + "\n" + all_new_content))

    # Update course.html (The Sellable Asset)
    with open("course.html", "w") as f:
        f.write(f"""
        <html><head><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-black text-white p-10 md:p-20 font-serif">
            <h1 class="text-5xl italic font-black uppercase mb-5">Signal Academy</h1>
            <p class="text-slate-500 tracking-widest mb-10 underline">Module: {datetime.now().strftime('%Y-%m-%d')}</p>
            <div class="max-w-2xl text-xl leading-relaxed border-l-2 border-white pl-8">
                {course_lesson}
            </div>
            <div class="mt-20 p-10 border border-slate-800 bg-slate-900">
                <h3 class="text-2xl mb-4 font-bold">Optimize Your Knowledge</h3>
                <p class="mb-6 text-slate-400">Get the full 365-day automated curriculum and certification.</p>
                <a href="https://gumroad.com" class="inline-block bg-white text-black px-8 py-4 font-bold uppercase tracking-tighter">Buy Full Course $97</a>
            </div>
        </body></html>
        """)

    # Update Log
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), "DAILY_DISPATCH", "SUCCESS"])

except Exception as e:
    print(f"Error updating files: {e}")
