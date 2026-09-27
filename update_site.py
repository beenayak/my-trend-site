import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. THE BULLETPROOF SETUP
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# This block automatically finds the best available model to avoid the 404 error
model_name = 'gemini-1.5-flash' 
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            model_name = m.name
            break
except:
    model_name = 'models/gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""

# 2. COURSE AUTOMATION LOGIC (New!)
# We will generate one "Course Module" based on the day's top signal
course_module = ""

for cat in categories:
    prompt = f"Research a {cat} trend. Return ONLY a luxury HTML div for SIGNAL Labs. No markdown."
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_text + "\n"
        
        # If this is the AI or Capital category, let's also make a course module
        if cat == 'ai' or cat == 'capital':
            course_prompt = f"Based on the trend '{clean_text[:50]}', write a 3-step 'Actionable Lesson' for a paid course. Use high-end business language."
            course_res = model.generate_content(course_prompt)
            course_module = course_res.text
    except:
        continue

# 3. UPDATE WEBSITE & COURSE PAGE
try:
    # Update Homepage
    with open("index.html", "r") as f:
        html = f.read()
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-32" id="trend-container">'
    if marker in html:
        new_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(new_html)

    # Update Course Page (New!)
    with open("course.html", "w") as f:
        f.write(f"""
        <html><head><script src="https://cdn.tailwindcss.com"></script></head>
        <body class="bg-black text-white p-20 font-serif">
            <h1 class="text-6xl mb-10 italic font-black uppercase">The Intelligence Protocol</h1>
            <p class="text-slate-400 mb-20 uppercase tracking-widest">Daily Masterclass // {datetime.now().strftime('%Y-%m-%d')}</p>
            <div class="max-w-2xl border-l border-white pl-10">
                {course_module}
            </div>
            <br><br>
            <a href="https://gumroad.com" class="bg-white text-black px-10 py-5 font-bold uppercase">Buy Full Certification</a>
        </body></html>
        """)
except Exception as e:
    print(f"Error: {e}")
