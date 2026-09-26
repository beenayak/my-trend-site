import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. AUTHENTICATION & SETUP
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("SIGNAL Error: GEMINI_API_KEY not found in GitHub Secrets.")

genai.configure(api_key=api_key)
# Using Gemini 1.5 Pro for higher-quality, long-form intelligence
model = genai.GenerativeModel('gemini-1.5-pro')

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

# 2. THE INTELLIGENCE ENGINE
for cat in categories:
    print(f"SIGNAL: Analyzing {cat} trajectory...")
    
    # Custom naming for the AI category to stay fancy
    display_name = "Synthetic Intelligence" if cat == 'ai' else cat.capitalize()
    
    prompt = f"""
    ACT AS: Lead Strategic Analyst at SIGNAL. Research Labs.
    TASK: Decipher one breakthrough trend regarding {cat}. 
    TONE: Clinical, sophisticated, high-status. Avoid all AI cliches (delve, unleash, etc).
    
    HTML STRUCTURE (MANDATORY):
    <div class="filter-item filter-{cat} group mb-20" data-aos="fade-up">
        <div class="aspect-[3/4] overflow-hidden bg-slate-100 mb-10">
            <img src="https://images.unsplash.com/photo-1?auto=format&fit=crop&q=80&w=800&q={cat},luxury" class="object-cover w-full h-full grayscale group-hover:grayscale-0 transition-all duration-1000 opacity-90">
        </div>
        <div class="flex items-center space-x-2 mb-6">
            <span class="w-4 h-[1px] bg-black"></span>
            <span class="text-[9px] font-black uppercase tracking-[0.3em]">{display_name} // Verified Signal</span>
        </div>
        <h3 class="text-4xl font-black mb-8 leading-tight uppercase tracking-tighter italic">[TREND_TITLE]</h3>
        <p class="text-slate-500 text-xs leading-relaxed mb-10 uppercase tracking-[0.1em] font-medium">[400_WORDS_OF_INTEL]</p>
        <a href="recommendations.html" class="inline-block w-full text-center bg-black text-white text-[10px] font-black uppercase tracking-[0.4em] py-6 hover:bg-slate-800 transition-all shadow-2xl">
            Access Protocol →
        </a>
    </div>

    INSTRUCTIONS:
    - Replace [TREND_TITLE] with a punchy, 3-word title.
    - Replace [400_WORDS_OF_INTEL] with deep, SEO-optimized synthesis.
    - Replace the Unsplash ID in the URL with a real ID related to {cat} or luxury tech.
    - RETURN ONLY THE HTML DIV.
    """

    try:
        response = model.generate_content(prompt)
        content = response.text
        all_new_content += content + "\n"
        
        # Log entry for spreadsheet
        log_entries.append([
            datetime.now().strftime("%Y-%m-%d %H:%M"),
            cat.upper(),
            "Deciphered",
            "SIGNAL LIVE"
        ])
    except Exception as e:
        print(f"SIGNAL Alert: Category {cat} failed: {e}")

# 3. WEBSITE INJECTION
try:
    with open("index.html", "r") as f:
        html = f.read()

    # Matches the exact new gap-y-32 marker you just added
    marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-32" id="trend-container">'
    
    if marker in html:
        updated_html = html.replace(marker, marker + "\n" + all_new_content)
        with open("index.html", "w") as f:
            f.write(updated_html)
        print("SIGNAL: index.html updated successfully.")
    else:
        print("SIGNAL Warning: Marker not found. Automation skipped injection.")

    # 4. LOG.CSV SYNC
    with open('log.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(log_entries)

    # 5. SITEMAP GENERATION (For Google Ranking)
    user = os.environ.get('GITHUB_ACTOR', 'user')
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{user}.github.io/SIGNAL/</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>
  <url><loc>https://{user}.github.io/SIGNAL/recommendations.html</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>
</urlset>"""
    with open("sitemap.xml", "w") as f:
        f.write(sitemap)

except Exception as e:
    print(f"SIGNAL Critical Error: {e}")

print("Automation sequence complete. System is active.")
