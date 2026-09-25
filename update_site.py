import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. Ask Gemini for the latest trend
prompt = """
ACT AS: A senior investigative tech journalist with a sharp, punchy, and slightly cynical tone (like Wired or Vice).

TASK:
1. Research one micro-trend in AI or Biohacking.
2. Write a 400-word article. 
3. HUMAN-LIKE WRITING RULES:
   - START with a provocative question or a startling fact.
   - NO "In conclusion," "Furthermore," or "Moreover." (Those are AI dead giveaways).
   - USE "Burstiness": Mix very short sentences (under 5 words) with longer, descriptive ones.
   - USE "Perplexity": Use rare adjectives and specific industry jargon.
   - PLAGIARISM CHECK: Do not summarize one article; synthesize data from three imaginary sources to create a unique perspective.

4. THE BRIDGE: 
   - At the end, add a button: <a href="recommendations.html" class="inline-block bg-blue-600 text-white px-6 py-3 rounded-2xl font-bold hover:bg-blue-700 transition mt-6">Access the Research Stack →</a>

OUTPUT: 
- Return ONLY the HTML <div> block. 
- Ensure all text is inside the div.
"""

response = model.generate_content(prompt)
new_content = response.text

# 2. Read the current index.html
with open("index.html", "r") as f:
    html = f.read()

# 3. Inject the new content into the 'trend-container' div
marker = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8" id="trend-container">'
updated_html = html.replace(marker, marker + "\n" + new_content)

# 4. Save the updated file
with open("index.html", "w") as f:
    f.write(updated_html)

print("Website updated with latest trend!")
