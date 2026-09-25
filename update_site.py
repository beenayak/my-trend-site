import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# Added 'ai' to the list
categories = ['health', 'capital', 'tech', 'ai']
for cat in categories:
    prompt = f"""
    ACT AS: Lead Strategic Analyst at SIGNAL. Research Labs.
    IDENTITY: You find "Signals" (trends) before they become "Noise" (mainstream).
    TONE: Sharp, clinical, high-status.

    HTML FORMATTING:
    <div class="filter-item filter-{cat} group mb-20" data-aos="fade-up">
        <div class="aspect-square overflow-hidden bg-slate-900 mb-8 rounded-none">
            <img src="[UNSPLASH_URL]" class="object-cover w-full h-full grayscale group-hover:grayscale-0 transition-all duration-700 opacity-80 group-hover:opacity-100">
        </div>
        <div class="flex items-center space-x-2 mb-6">
            <span class="w-4 h-4 bg-black rounded-full flex items-center justify-center text-[8px] text-white font-bold">!</span>
            <span class="text-[9px] font-black uppercase tracking-[0.3em]">{cat if cat != 'ai' else 'Intelligence'} // Verified Signal</span>
        </div>
        <h3 class="text-3xl font-black mb-6 leading-tight uppercase tracking-tighter">[TREND_TITLE]</h3>
        <p class="text-slate-500 text-xs leading-relaxed mb-8 uppercase tracking-wider font-medium">[STORY_CONTENT]</p>
        <a href="recommendations.html" class="text-[9px] font-black uppercase tracking-[0.4em] border-b-2 border-black pb-1 hover:text-slate-400 hover:border-slate-400 transition-all">Decipher Report →</a>
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
