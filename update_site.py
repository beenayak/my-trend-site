import os
import google.generativeai as genai

# Setup Gemini
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. Ask Gemini for the latest trend
prompt = """
Find a trending 'AI Productivity' or 'Bio-hacking' topic for today. 
Write a website HTML block for it. 
Include: 
- A catchy title
- A 2-sentence summary
- A placeholder for a relevant Unsplash image URL.
Format it exactly as a <div> block using Tailwind CSS classes.
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
