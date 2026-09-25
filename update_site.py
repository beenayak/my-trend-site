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
    TASK: Research one breakthrough trend specifically regarding {cat}.
    
    HTML OUTPUT REQUIREMENTS (YOU MUST INCLUDE THE BUTTON):
    <div class="filter-item filter-{cat} group mb-20" data-aos="fade-up">
        <div class="aspect-square overflow-hidden bg-slate-900 mb-8">
            <img src="[UNSPLASH_URL]" class="object-cover w-full h-full grayscale group-hover:grayscale-0 transition-all duration-700 opacity-80 group-hover:opacity-100">
        </div>
        <div class="flex items-center space-x-2 mb-6">
            <span class="w-4 h-4 bg-black rounded-full flex items-center justify-center text-[8px] text-white font-bold">!</span>
            <span class="text-[9px] font-black uppercase tracking-[0.3em]">{cat if cat != 'ai' else 'Intelligence'} // Verified Signal</span>
        </div>
        <h3 class="text-3xl font-black mb-6 leading-tight uppercase tracking-tighter">[TREND_TITLE]</h3>
        <p class="text-slate-500 text-xs leading-relaxed mb-10 uppercase tracking-wider font-medium">[STORY_CONTENT]</p>
        
        <!-- THE REDESIGNED BUTTON -->
        <a href="recommendations.html" class="inline-block w-full text-center bg-black text-white text-[10px] font-black uppercase tracking-[0.4em] py-5 hover:bg-slate-800 transition-all shadow-xl">
            Access Protocol →
        </a>
    </div>

    WRITING RULES:
    - Replace [TREND_TITLE] with a 3-word aggressive title.
    - Replace [STORY_CONTENT] with 3 sophisticated sentences.
    - Use a real Unsplash URL for {cat}.
    
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
