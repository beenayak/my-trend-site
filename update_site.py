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
   # Inside your update_site.py:
    with open("course.html", "w") as f:
        f.write(f"""
        <html><head><script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700&display=swap" rel="stylesheet">
        <style>body {{ background:#050505; color:#fff; font-family:'Space Grotesk', sans-serif; }}</style></head>
        <body class="p-10 md:p-24">
            <div class="max-w-4xl mx-auto">
                <nav class="mb-20 flex justify-between items-center border-b border-white/5 pb-10">
                    <div class="text-xl font-black italic uppercase tracking-tighter">Signal Academy.</div>
                    <div class="text-[10px] text-green-400 font-bold uppercase tracking-widest">Protocol ID: {datetime.now().strftime('%Y%m%d')}</div>
                </nav>
                <span class="text-white/20 uppercase tracking-[0.5em] text-[10px] font-bold">Daily Intelligence Masterclass</span>
                <h1 class="text-6xl md:text-8xl font-black mt-6 mb-12 leading-tight tracking-tighter uppercase italic">The Shift<br>Protocol.</h1>
                <div class="bg-white/5 p-12 rounded-[2rem] border border-white/5 text-xl leading-relaxed text-slate-300 mb-20 shadow-2xl">
                    {course_lesson}
                </div>
                <div class="bg-white text-black p-16 rounded-[3rem] text-center shadow-[0_0_50px_rgba(255,255,255,0.1)]">
                    <h2 class="text-5xl font-black uppercase mb-6 tracking-tighter">Own the Intelligence.</h2>
                    <p class="mb-12 text-black/50 font-bold uppercase tracking-widest text-xs">Unlock the full 365-day archive + private group access.</p>
                    <a href="https://gumroad.com" class="inline-block bg-black text-white px-12 py-6 rounded-full font-black uppercase tracking-widest hover:scale-105 transition shadow-2xl">Get Certified // $97</a>
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
