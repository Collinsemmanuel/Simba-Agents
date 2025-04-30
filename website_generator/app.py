from flask import Flask, request, render_template, send_file, jsonify
import os
import requests
import zipfile
from io import BytesIO

app = Flask(__name__)

# Create folder to save generated files if it doesn't exist
if not os.path.exists('generated_sites'):
    os.makedirs('generated_sites')

# === Replace with your real API KEY ===
API_KEY = 'api ...'
API_URL = 'https://api.deepseek.com/v1/chat/completions'  # Example, adjust if needed

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_website():
    user_prompt = request.json.get('prompt')
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json',
    }
    
    payload = {
        "model": "deepseek-chat",  # or another model
        "messages": [
            {"role": "system", "content": "You are a web developer. Return clean HTML, CSS, and JS separately."},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.7
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    generated_text = data['choices'][0]['message']['content']

    # Parse generated text into HTML, CSS, JS
    html_code, css_code, js_code = split_code(generated_text)

    site_folder = 'generated_sites/site'
    if not os.path.exists(site_folder):
        os.makedirs(site_folder)

    with open(os.path.join(site_folder, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(html_code)
    with open(os.path.join(site_folder, 'style.css'), 'w', encoding='utf-8') as f:
        f.write(css_code)
    with open(os.path.join(site_folder, 'script.js'), 'w', encoding='utf-8') as f:
        f.write(js_code)

    return jsonify({"message": "Website generated successfully!"})

@app.route('/download')
def download_website():
    memory_file = BytesIO()
    with zipfile.ZipFile(memory_file, 'w') as zf:
        for root, _, files in os.walk('generated_sites/site'):
            for file in files:
                filepath = os.path.join(root, file)
                zf.write(filepath, arcname=file)
    memory_file.seek(0)
    return send_file(memory_file, download_name='website.zip', as_attachment=True)

def split_code(full_text):
    """Very basic splitting — later we can make it smarter."""
    html_code = css_code = js_code = ''

    if "<html>" in full_text:
        html_code = full_text.split("<html>")[1].split("</html>")[0]
        html_code = "<html>" + html_code + "</html>"
    if "<style>" in full_text:
        css_code = full_text.split("<style>")[1].split("</style>")[0]
    if "<script>" in full_text:
        js_code = full_text.split("<script>")[1].split("</script>")[0]

    return html_code, css_code, js_code

if __name__ == '__main__':
    app.run(debug=True)
