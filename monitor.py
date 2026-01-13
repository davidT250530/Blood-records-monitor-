import requests
import time

# ================= 配置区 =================
# 1. 你的 Bark 推送链接
BARK_BASE_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3"

# 2. 你的黑名单
BLACKLIST = ["Rio Kosta", "Another Artist"]

# 3. 你的心头好名单
MY_FAVORITES = ["Lana Del Rey","joji","sabrina carpenter ","Taylor Swift", "The 1975", "Fontaines D.C.", "Harry Styles", "Billie Eilish"]


# 4. Rough Trade API
RT_API_URL = "https://www.roughtrade.com/en-gb/api/products?page=1&per_page=40"
# ==========================================

def get_value_score(title):
    """
    智能打分系统 2.0：
    - 动效黑胶 (Zoetrope) 和 签名 (Signed) 权重最高
    - 热门艺人直接触发警报
    """
    score = 0
    title_lower = title.lower()
    
    # 1. 核心理财关键词（高权重）
    if "zoetrope" in title_lower:
        score += 80  # 动效黑胶（Bad World / Blood Records 特色），溢价极高
    if "signed" in title_lower or "autographed" in title_lower:
        score += 70  # 签名版
        
    # 2. 版本稀缺度关键词
    if "exclusive" in title_lower:
        score += 30  # 独家配色
    if "numbered" in title_lower:
        score += 40  # 独立编号（理财关键）
    if "limited" in title_lower:
        score += 10  # 普通限量
        
    # 3. 艺人白名单（只要出现即拉满分）
    # 建议名单：Joji, Gorillaz, Lana Del Rey, Taylor Swift, Fontaines D.C.
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
