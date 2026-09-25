import os
import google.generativeai as genai
from datetime import datetime
import csv

# 1. SETUP
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-pro') # Using Pro for deeper research

categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""
log_entries = []

# 2. THE SEO-OPTIMIZED ENGINE
for cat in categories:
    print(f"Deep-researching {cat} for SEO ranking...")
    
    # We ask for "Search Intent" keywords and "LSI" keywords to beat the algorithm
    prompt = f"""
    ACT AS: A World-Class SEO Content Strategist and Lead Analyst at SIGNAL. Labs.
    TASK: Identify a 'zero-volume' but high-intent breakthrough in {cat}. 
    
    SEO REQUIREMENTS:
    - Focus on a specific long-tail keyword.
    - Use Semantic keywords (related terms) naturally.
    - Write 400 words of high-authority, plagiarism-free content.
    - DO NOT use AI-clichés. 
    
    HTML OUTPUT:
    <div class="filter-item filter-{cat} group mb-32" data-aos="fade-up">
        <div class="aspect-square overflow-hidden bg-slate-900 mb-8 rounded-none">
            <img src="https://source.unsplash.com/featured/?{cat},luxury" class="object-cover w-full h-full grayscale group-hover:grayscale-0 transition-all duration-1000 opacity-80">
        </div>
        <div class="flex items-center space-x-2 mb-6">
            <span class="w-4 h-4 bg-black rounded-full flex items-center justify-center text-[8px] text-white font-bold">!</span>
            <span class="text-[9px] font-black uppercase tracking-[0.3em]">{cat} // Verified Signal</span>
        </div>
        <h3 class="text-4xl md:text-5xl font-black mb-8 leading-tight uppercase tracking-tighter">[SEO_TITLE]</h3>
        <div class="text-slate-500 text-xs leading-relaxed mb-10 uppercase tracking-widest space-y-4">
            [CONTENT_PARAGRAPH_1]
            [CONTENT_PARAGRAPH_2]
        </div>
        <a href="recommendations.html" class="inline-block w-full text-center bg-black text-white text-[10px] font-black uppercase tracking-[0.4em] py-6 hover:bg-slate-800 transition-all shadow-2xl">
            Access Protocol →
        </a>
    </div>
    """

    response = model.generate_content(prompt)
    content = response.text
    all_new_content += content + "\n"
    
    # Capture for Log
    log_entries.append([datetime.now().strftime("%Y-%m-%d"), cat.upper(), "Deep Search Done", "LIVE"])

# 3. UPDATE WEBSITE
with open("index.html", "r") as f:
    html = f.read()

marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-24" id="trend-container">'
updated_html = html.replace(marker, marker + "\n" + all_new_content)

with open("index.html", "w") as f:
    f.write(updated_html)

# 4. UPDATE LOG
with open('log.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(log_entries)

# 5. GENERATE SITEMAP (SEO GOLD)
# This helps Google index your site 10x faster
sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>https://{os.environ.get('GITHUB_REPOSITORY_OWNER', 'user')}.github.io/SIGNAL/</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>
  <url><loc>https://{os.environ.get('GITHUB_REPOSITORY_OWNER', 'user')}.github.io/SIGNAL/recommendations.html</loc><lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod></url>
</urlset>"""

with open("sitemap.xml", "w") as f:
    f.write(sitemap_content)

print("SIGNAL Deep Update Complete. Sitemap.xml updated.")
