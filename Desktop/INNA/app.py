from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import time

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    url = request.form.get('url')
    
    # URL check karne ke liye logic
    if not url.startswith('http'):
        url = 'https://' + url

    start_time = time.time()
    
    try:
        response = requests.get(url, timeout=10)
        end_time = time.time()
        
        # 1. Performance (Node Speed)
        response_time = round((end_time - start_time) * 1000, 2)
        
        # 2. Content Analysis (Intelligent Scanning)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "No Title Found"
        
        # 3. Growth & SEO Logic (The New Part)
        score = 100
        suggestions = []

        # Title check
        if len(title) < 10:
            score -= 10
            suggestions.append("Title bahut chota hai, keywords dalo.")

        # Meta Description check
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if not meta_desc:
            score -= 20
            suggestions.append("Meta Description missing hai. Isse reach badhti hai!")
        
        # H1 Tag check
        if not soup.find('h1'):
            score -= 15
            suggestions.append("H1 tag missing hai. Page ka main heading zaroori hai.")

        data = {
            "url": url,
            "status": "Healthy" if response.status_code == 200 else "Down",
            "speed": f"{response_time} ms",
            "title": title,
            "seo_score": score,
            "suggestions": suggestions,
            "code": response.status_code
        }
        return render_template('index.html', result=data)
        
    except Exception as e:
        return render_template('index.html', error=f"Bhai link sahi nahi hai ya site block kar rahi hai: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)