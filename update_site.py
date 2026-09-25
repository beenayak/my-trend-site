import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Added 'ai' to the list
categories = ['health', 'capital', 'tech', 'ai']
all_new_content = ""

for cat in categories:
    print(f"Generating report for {cat}...")
    
    # Specific instruction for the AI category to keep it fancy
    topic_focus = "breakthroughs in neural networks and synthetic logic" if cat == 'ai' else f"breakthroughs in the {cat} sector"

    prompt = f"""
    ACT AS: A Lead Editor at 'Monograph Private Lab'.
    TASK: Research one breakthrough trend specifically regarding {topic_focus}.
    
    HTML OUTPUT REQUIREMENTS:
    <div class="filter-item filter-{cat} group cursor-pointer mb-20" data-aos="fade-up">
        <div class="aspect-[3/4] overflow-hidden bg-slate-100 mb-8">
            <img src="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=800" class="object-cover w-full h-full grayscale group-hover:grayscale-0 group-hover:scale-105 transition-all duration-1000">
        </div>
        <div class="flex items-center space-x-2 mb-4">
            <span class="w-8 h-[1px] bg-slate-900"></span>
            <span class="text-[10px] font-bold uppercase tracking-widest">{cat if cat != 'ai' else 'Synthetic Intelligence'} // Dispatch</span>
        </div>
        <h3 class="text-4xl font-bold mb-6 leading-[1.1]">[TREND_TITLE]</h3>
        <p class="text-slate-500 text-sm leading-relaxed mb-8">[STORY_CONTENT]</p>
        <a href="recommendations.html" class="text-[10px] font-black uppercase tracking-widest border-b-2 border-black pb-1 hover:text-slate-400 hover:border-slate-400 transition-all">Open Report →</a>
    </div>

    WRITING RULES:
    - If the category is 'ai', talk about it as a 'shift in synthetic reasoning' or 'computational evolution'.
    - DO NOT use words like 'chatbot', 'AI-powered', or 'revolutionary'.
    - Use sophisticated, punchy language.
    - Find a high-end, abstract Unsplash image URL that fits the {cat} theme.
    """

    response = model.generate_content(prompt)
    all_new_content += response.text + "\n"
# New Social Media Logic
    social_prompt = f"""
    Write a 'Hook' for a social media post about this {cat} trend.
    Tone: Provocative, exclusive, and high-status.
    Format: 
    1. A shocking headline (max 7 words)
    2. A bullet point of what the reader is missing.
    3. The link: 'Read the full Dispatch at monograph.intelligence' (replace with your URL)
    """
    social_response = model.generate_content(social_prompt)
    print(f"--- SOCIAL HOOK FOR {cat.upper()} ---")
    print(social_response.text)
# Read and Update HTML
with open("index.html", "r") as f:
    html = f.read()

marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-12 gap-y-24" id="trend-container">'
updated_html = html.replace(marker, marker + "\n" + all_new_content)

with open("index.html", "w") as f:
    f.write(updated_html)

print("Dispatch Updated: Health, Capital, Tech, and Intelligence.")
