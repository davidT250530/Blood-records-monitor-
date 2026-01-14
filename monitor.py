import requests
import time

# ================= 配置区 =================
BARK_BASE_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3"
# 加上 Bad World 和其他理财艺人
MY_FAVORITES = ["Sabrina Carpenter", "Joji", "Gorillaz", "Bad World", "Lana Del Rey", "Taylor Swift", "Zoetrope"]
BLACKLIST = ["Rio Kosta"]
# ==========================================

def get_value_score(title):
    score = 0
    title_lower = title.lower()
    
    # 只要是 Blood Records 的东西，默认给一个基础分，保证必推
    score += 40 
    
    if "zoetrope" in title_lower or "bad world" in title_lower:
        score += 50
    if "signed" in title_lower or "autographed" in title_lower:
        score += 60
    if "exclusive" in title_lower or "numbered" in title_lower:
        score += 30
    if any(fav.lower() in title_lower for fav in MY_FAVORITES):
        score += 100
    return score

def send_bark(header, title, link):
    # 如果分数极高（比如包含艺人名），使用报警音
    sound = "alarm" if "🔥" in header else "choochoo"
    push_url = f"{BARK_BASE_URL}/{header}/{title}?url={link}&sound={sound}&group=VinylMonitor"
    requests.get(push_url, timeout=10)

def check_blood_records():
    print("--- 正在巡逻 Blood Records ---")
    url = "https://www.blood-records.co.uk/products.json"
    try:
        data = requests.get(url, timeout=15).json()
        for p in data['products']:
            title = p['title']
            if any(b.lower() in title.lower() for b in BLACKLIST): continue
            
            score = get_value_score(title)
            link = f"https://www.blood-records.co.uk/products/{p['handle']}"
            
            # 降低门槛：只要分数达到 40（即所有上新）就推送
            if score >= 100:
                send_bark("🔥【重磅特急】", title, link)
            elif score >= 40:
                send_bark("📢【Blood新上新】", title, link)
    except Exception as e:
        print(f"错误: {e}")

# ... (保持 check_rough_trade 不变) ...

if __name__ == "__main__":
    check_blood_records()
    # check_rough_trade() # 如果只想盯Blood可以先注释掉这行
