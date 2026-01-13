import requests
import time

# ================= 配置区 =================
# 1. 你的 Bark 推送链接
BARK_BASE_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3"

# 2. 你的黑名单
BLACKLIST = ["Rio Kosta", "Another Artist"]

# 3. 你的心头好名单
MY_FAVORITES = ["Lana Del Rey", "Taylor Swift", "The 1975", "Fontaines D.C.", "Harry Styles", "Billie Eilish"]


# 4. Rough Trade API
RT_API_URL = "https://www.roughtrade.com/en-gb/api/products?page=1&per_page=40"
# ==========================================

def get_value_score(title):
    score = 0
    title_lower = title.lower()
    if "signed" in title_lower or "autographed" in title_lower:
        score += 60
    if "exclusive" in title_lower:
        score += 30
    if "limited" in title_lower:
        score += 10
    if any(fav.lower() in title_lower for fav in MY_FAVORITES):
        score += 100
    return score

def send_bark(header, title, link):
    sound = "alarm" if "🔥" in header else "choochoo"
    push_url = f"{BARK_BASE_URL}/{header}/{title}?url={link}&sound={sound}&group=VinylMonitor"
    try:
        requests.get(push_url, timeout=10)
    except Exception as e:
        print(f"推送失败: {e}")

def check_blood_records():
    print("--- 正在巡逻 Blood Records ---")
    url = "https://www.blood-records.co.uk/products.json"
    try:
        data = requests.get(url, timeout=15).json()
        for p in data['products']:
            title = p['title']
            if any(b.lower() in title.lower() for b in BLACKLIST):
                continue
            score = get_value_score(title)
            link = f"https://www.blood-records.co.uk/products/{p['handle']}"
            if score >= 60:
                send_bark("🔥【重磅签名】Blood Records", title, link)
            elif score >= 30:
                send_bark("📢【独家限量】Blood Records", title, link)
    except Exception as e:
        print(f"Blood Records 错误: {e}")

def check_rough_trade():
    print("--- 正在巡逻 Rough Trade ---")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        res = requests.get(RT_API_URL, headers=headers, timeout=15).json()
        products = res.get('data', []) if isinstance(res, dict) else []
        for p in products:
            title = p.get('name', p.get('title', ''))
            if not title or any(b.lower() in title.lower() for b in BLACKLIST):
                continue
            score = get_value_score(title)
            slug = p.get('slug', '')
            link = f"https://www.roughtrade.com/en-gb/product/{slug}"
            if score >= 60:
                send_bark("🔥【极稀有签名】Rough Trade", title, link)
            elif score >= 30:
                send_bark("📢【值得关注】Rough Trade", title, link)
    except Exception as e:
        print(f"Rough Trade 错误: {e}")

if __name__ == "__main__":
    check_blood_records()
    check_rough_trade()
