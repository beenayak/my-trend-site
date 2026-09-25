import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Define our 3 distinct categories
categories = ['health', 'capital', 'tech']
all_new_content = ""

for cat in categories:
    print(f"Generating report for {cat}...")
    
    # This is our MASTER PROMPT template
    prompt = f"""
    ACT AS: A Lead Editor at 'Monograph Private Lab'.
    TASK: Research one breakthrough trend specifically in the {cat} sector.
    
    HTML OUTPUT REQUIREMENTS:
    <div class="filter-item filter-{cat} group cursor-pointer mb-20" data-aos="fade-up">
        <div class="aspect-[3/4] overflow-hidden bg-slate-100 mb-8">
            <img src="https://images.unsplash.com/photo-1500000000000?auto=format&fit=crop&q=80&w=800" class="object-cover w-full h-full grayscale group-hover:grayscale-0 group-hover:scale-105 transition-all duration-1000">
        </div>
        <div class="flex items-center space-x-2 mb-4">
            <span class="w-8 h-[1px] bg-slate-900"></span>
            <span class="text-[10px] font-bold uppercase tracking-widest">{cat} // Intelligence Dispatch</span>
        </div>
        <h3 class="text-4xl font-bold mb-6 leading-[1.1]">[TREND_TITLE]</h3>
        <p class="text-slate-500 text-sm leading-relaxed mb-8">[STORY_CONTENT]</p>
        <a href="recommendations.html" class="text-[10px] font-black uppercase tracking-widest border-b-2 border-black pb-1 hover:text-slate-400 hover:border-slate-400 transition-all">Open Report →</a>
    </div>

    STORY CONTENT RULES:
    - Write 3-4 punchy, sophisticated sentences. 
    - Use "Burstiness" (mix of short and long sentences).
    - Avoid all AI-sounding words (no "delve," "unleash," or "comprehensive").
    - Replace the Unsplash URL with a real search-based URL for {cat} lifestyle.
    """

    response = model.generate_content(prompt)
    all_new_content += response.text + "\n"

# 2. Read the current index.html
with open("index.html", "r") as f:
    html = f.read()

# 3. Inject ALL the new reports into the container
marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-24" id="trend-container">'
updated_html = html.replace(marker, marker + "\n" + all_new_content)

# 4. Save
with open("index.html", "w") as f:
    f.write(updated_html)

print("Multi-category update complete.")
