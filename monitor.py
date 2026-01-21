import requests
import os

# ================= 配置区 =================
# 请确保这里的引号是英文半角的 ""
BARK_BASE_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3"

# 2026 重点监控名单
MY_FAVORITES = ["Sabrina Carpenter", "Joji", "Gorillaz", "Bad World", "Lana Del Rey", "Taylor Swift", "Chappell Roan", "The 1975", "Zoetrope"]

# 排除不感兴趣的关键词
BLACKLIST = ["Rio Kosta", "doves", "Celeste"]
# ==========================================

def get_value_score(title):
    score = 0
    title_lower = title.lower()
    
    # 基础分
    score += 40 
    
    # 关键词加分
    if "zoetrope" in title_lower or "bad world" in title_lower:
        score += 50
    if "signed" in title_lower or "autographed" in title_lower:
        score += 60
    if "exclusive" in title_lower or "numbered" in title_lower:
        score += 30
        
    # 艺人匹配直接满分
    if any(fav.lower() in title_lower for fav in MY_FAVORITES):
        score += 100
        
    return score

def send_bark(header, title, link):
    sound = "alarm" if "🔥" in header else "choochoo"
    push_url = f"{BARK_BASE_URL}/{header}/{title}?url={link}&sound={sound}&group=Vinyl2026"
    try:
        requests.get(push_url, timeout=10)
    except:
        print("Bark 推送失败")

def check_blood_records():
    print("--- 巡逻 Blood Records ---")
    url = "https://www.blood-records.co.uk/products.json"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        for p in data['products']:
            # 只有有货才报
            variants = p.get('variants', [])
            is_available = any(v.get('available', False) for v in variants)
            if not is_available:
                continue 
            
            title = p['title']
            if any(b.lower() in title.lower() for b in BLACKLIST):
                continue
            
            score = get_value_score(title)
            v_id = variants[0].get('id') if variants else ""
            quick_link = f"https://www.blood-records.co.uk/cart/add?id={v_id}"
            
            if score >= 100:
                send_bark("🔥【重磅特急】", title, quick_link)
            elif score >= 40:
                send_bark("🚀【检测到上新】", title, quick_link)
    except Exception as e:
        print(f"Blood 访问失败: {e}")

def check_rough_trade():
    print("--- 巡逻 Rough Trade ---")
    url = "https://www.roughtrade.com/en-gb/products.json"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        for p in data['products']:
            title = p['title']
            if any(fav.lower() in title.lower() for fav in MY_FAVORITES):
                link = f"https://www.roughtrade.com/en-gb/products/{p['handle']}"
                send_bark("🔥【RT 重点关注】", title, link)
    except:
        print("Rough Trade 访问受限")

if __name__ == "__main__":
    check_blood_records()
    check_rough_trade()
