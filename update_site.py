import os
import google.generativeai as genai
from datetime import datetime
import csv

# --- PHASE 1: FORCE FILE CREATION (Prevents the Git Error) ---
required_files = {
    'log.csv': 'Timestamp,Category,Status\n',
    'sitemap.xml': '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"></urlset>',
    'course.html': '<html><body style="background:black;color:white;">Initializing Academy...</body></html>'
}

for filename, content in required_files.items():
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(content)
        print(f"✅ Created missing file: {filename}")

# --- PHASE 2: AI BRAIN SETUP ---
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

try:
    # Auto-select the best model available on your account
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    model_name = models[0] if models else 'gemini-1.5-flash'
except:
    model_name = 'gemini-1.5-flash'

model = genai.GenerativeModel(model_name)

# --- PHASE 3: RESEARCH & CONTENT ---
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
course_lesson = "Analyzing latest signals..."

for cat in categories:
    try:
        # Website Report
        res = model.generate_content(f"Luxury HTML report for {cat} trend. Use 'Access Protocol' button. No markdown.")
        clean_html = res.text.replace("```html", "").replace("```", "").strip()
        all_new_content += clean_html + "\n"
        
        # Course Lesson (For Selling)
        if cat == 'ai':
            lesson_res = model.generate_content(f"Write a 3-step 'Masterclass Lesson' for {cat} trends.")
            course_lesson = lesson_res.text
    except Exception as e:
        print(f"Error researching {cat}: {e}")

# --- PHASE 4: SECURE INJECTION ---
try:
    # Update Homepage
    if os.path.exists("index.html"):
        with open("index.html", "r") as f:
            html = f.read()
        marker = 'id="trend-container">'
        if marker in html:
            with open("index.html", "w") as f:
                f.write(html.replace(marker, marker + "\n" + all_new_content))

    # Update Course Page
   # Inside the "Update Course Page" section of your update_site.py:
    with open("course.html", "w") as f:
        f.write(f"""
        <html><head><script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;700&display=swap" rel="stylesheet">
        <style>body {{ font-family: 'Space Grotesk', sans-serif; background: #000; color: #fff; }}</style></head>
        <body class="p-10 md:p-24">
            <nav class="mb-20 flex justify-between border-b border-white/10 pb-10">
                <div class="text-2xl font-black italic uppercase">Signal Academy.</div>
                <div class="text-[10px] text-green-400 font-bold uppercase tracking-widest">Session ID: {datetime.now().strftime('%Y%m%d')}</div>
            </nav>
            <div class="max-w-3xl mx-auto">
                <span class="text-white/30 uppercase tracking-[0.5em] text-[10px]">Current Module // Intelligence Synthesis</span>
                <h1 class="text-6xl font-black mt-4 mb-10 leading-none tracking-tighter uppercase">The Intelligence <br>Protocol.</h1>
                <div class="glass p-10 rounded-2xl border border-white/10 text-xl leading-relaxed text-white/80 mb-20">
                    {course_lesson}
                </div>
                <div class="bg-white text-black p-12 rounded-3xl text-center">
                    <h2 class="text-4xl font-black uppercase mb-4 tracking-tighter">Get the Full 365-Day Curriculum</h2>
                    <p class="mb-10 text-black/60 font-bold uppercase tracking-widest text-xs">Unlock all signals + private community access</p>
                    <a href="https://gumroad.com" class="inline-block bg-black text-white px-10 py-5 rounded-full font-black uppercase tracking-widest hover:bg-green-500 transition shadow-2xl">Buy Full Certification // $97</a>
                </div>
            </div>
        </body></html>
        """)

    # Update Log
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now(), "AUTOMATION_RUN", "SUCCESS"])

    # Finalize Sitemap
    user = os.environ.get('GITHUB_ACTOR', 'user')
    with open("sitemap.xml", "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://{user}.github.io/my-trend-site/</loc></url></urlset>')

except Exception as e:
    print(f"Critical writing error: {e}")
