from flask import Flask, jsonify, request
from flask_cors import CORS
from database_manager import DatabaseManager 
import requests
from bs4 import BeautifulSoup
import re
import google.generativeai as genai
from flask import Flask, jsonify, request, render_template # <-- أضف render_template

# ... (باقي الكود)

app = Flask(__name__)
# CORS(app)  <-- في السيرفر الحقيقي قد لا نحتاج CORS إذا كان الفرونت والباك في نفس المكان، لكن اتركها

# المسار الرئيسي لفتح الموقع
@app.route('/')
def home():
    return render_template('index.html')

# ... (باقي الـ API routes كما هي)

# --- 1. إعدادات Gemini ---
# تنبيه: لا تشارك مفتاح API الخاص بك علناً
GEMINI_API_KEY = "AIzaSyAO055e5e3xklxrPGD6hloN9wIOp06TP3c" 
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

# --- 2. إعدادات قاعدة البيانات ---
DB_CONFIG = {
    'user': 'root',
    'password': '',         
    'host': '127.0.0.1',
    'database': 'smartzone_db'
}

app = Flask(__name__)
CORS(app) 
db_manager = DatabaseManager(DB_CONFIG)

# --- 3. دالة الـ Scraping (بحث الويب) ---
def get_specs_from_gsmarena(phone_name):
    # (نفس الكود السابق للـ scraping لم يتغير)
    print(f"[Scraper] Searching for: {phone_name}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        search_url = f"https://www.gsmarena.com/res.php3?sSearch={phone_name.replace(' ', '+')}"
        search_page = requests.get(search_url, headers=headers, timeout=10)
        search_soup = BeautifulSoup(search_page.content, 'html.parser')
        
        results_div = search_soup.find('div', class_='makers')
        if not results_div: return None
            
        first_result = results_div.find('li')
        if not first_result or not first_result.find('a'): return None
            
        phone_page_url = "https://www.gsmarena.com/" + first_result.find('a')['href']
        spec_page = requests.get(phone_page_url, headers=headers, timeout=10)
        spec_soup = BeautifulSoup(spec_page.content, 'html.parser')

        def clean_text(text): return text.strip() if text else 'N/A'
        def get_val(data_spec):
            el = spec_soup.find('td', {'data-spec': data_spec})
            return clean_text(el.get_text() if el else None)

        full_name = clean_text(spec_soup.find('h1', {'data-spec': 'modelname'}).get_text())
        parts = full_name.split(' ', 1)
        brand_name = parts[0] if len(parts) > 1 else "Unknown"
        model_name = parts[1] if len(parts) > 1 else full_name

        image_url = None
        img_div = spec_soup.find('div', class_='specs-photo-main')
        if img_div and img_div.find('img'):
            image_url = img_div.find('img')['src']

        release_date = '1970-01-01'
        raw_date = get_val('released-hl')
        match = re.search(r'(\d{4}), (\w+)', raw_date)
        if match: release_date = f"{match.group(1)}-01-01"

        specs_list = [
            {"category": "Display", "name": "Screen Size", "value": get_val('displaysize')},
            {"category": "Display", "name": "Type", "value": get_val('displaytype')},
            {"category": "Performance", "name": "Chipset", "value": get_val('chipset')},
            {"category": "Performance", "name": "RAM", "value": get_val('internalmemory')},
            {"category": "Battery", "name": "Capacity", "value": get_val('batdescription1')},
            {"category": "Camera", "name": "Main Camera", "value": get_val('cam1modules')},
        ]

        return {
            "brand_name": brand_name,
            "model_name": model_name,
            "release_date": release_date,
            "image_url": image_url,
            "price": 0.00,
            "specs": specs_list
        }
    except Exception as e:
        print(f"[Scraper] Error: {e}")
        return None

def get_or_create_phone_id(phone_name):
    phone_id = db_manager.find_phone_by_name(phone_name)
    if phone_id: return phone_id
        
    print(f"Phone '{phone_name}' not in DB. Trying scraper...")
    ai_data = get_specs_from_gsmarena(phone_name)
    if not ai_data: return None
        
    brand_id = db_manager.find_or_create_brand(ai_data['brand_name'])
    new_id = db_manager.add_phone(
        ai_data['model_name'], brand_id, ai_data['release_date'], 
        ai_data['specs'], ai_data['price'], ai_data['image_url']
    )
    return new_id

# --- 4. API Routes ---

# ** جديد: API لجلب الشركات **
@app.route('/api/brands')
def get_brands():
    brands = db_manager.get_all_brands()
    return jsonify(brands)

@app.route('/api/phones')
def get_all_phones():
    phones = db_manager.get_all_phones()
    if phones is None: return jsonify({"error": "Database Error"}), 500
    
    detailed = []
    for p in phones:
        d = db_manager.get_phone_details(p['phone_id'])
        if d:
            detailed.append({
                "phone_id": p['phone_id'],
                "full_name": f"{d['brand_name']} {d['model_name']}",
                "brand_name": d['brand_name'], # مهم للفلتر
                "ram": d['specs'].get('RAM', 'N/A').split(',')[0],
                "camera": d['specs'].get('Main Camera', 'N/A'),
                "battery": d['specs'].get('Capacity', 'N/A'),
                "screen": d['specs'].get('Screen Size', 'N/A'), # عرض الشاشة
                "price": d['price'],
                "image_url": d['image_url']
            })
    return jsonify(detailed)

@app.route('/api/compare-by-name')
def compare_phones():
    p1_name = request.args.get('phone1_name')
    p2_name = request.args.get('phone2_name')
    if not p1_name or not p2_name: return jsonify({"error": "Missing phone names"}), 400

    id1 = get_or_create_phone_id(p1_name)
    id2 = get_or_create_phone_id(p2_name)
    
    if not id1 or not id2: return jsonify({"error": "Phone not found locally or online"}), 404

    data1 = db_manager.get_phone_details(id1)
    data2 = db_manager.get_phone_details(id2)
    all_specs = sorted(list(set(data1["specs"].keys()) | set(data2["specs"].keys())))
    
    return jsonify({"phone1": data1, "phone2": data2, "all_specs": all_specs})

@app.route('/api/chat', methods=['POST'])
def chat_gemini():
    data = request.json
    user_message = data.get("message", "")
    if not user_message: return jsonify({"error": "Empty message"}), 400

    system_prompt = "أنت مساعد ذكي متخصص في الهواتف الذكية. تحدث باختصار وإفادة."
    try:
        full_prompt = f"{system_prompt}\n\nالمستخدم: {user_message}\nالمساعد:"
        response = gemini_model.generate_content(full_prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        print(f"Gemini Error: {e}")
        return jsonify({"error": "AI Error"}), 500

if __name__ == '__main__':

    app.run(debug=True, port=5000)
