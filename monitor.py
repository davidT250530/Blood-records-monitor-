import requests
import os

# ================= 配置区 =================
# 替换为你自己的 Bark Key
BARK_BASE_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3"

# 2026 重点理财名单
MY_FAVORITES = ["Sabrina Carpenter", "Joji", "Gorillaz", "Bad World", "Lana Del Rey", "Taylor Swift", "Chappell Roan", "The 1975", "Zoetrope"]

# 排除不感兴趣的关键词
BLACKLIST = ["Rio Kosta",“doves”,"Celeste”]
# ==========================================

def get_value_score(title):
    """
    智能评分系统：
    - 基础分 40 (保证 Blood Records 只要上新就有通知)
    - 关键词加分 (Zoetrope, Signed)
    - 艺人命中直接拉满
    """
    score = 0
    title_lower = title.lower()
    
    # 基础分：只要是 Blood Records 的产品就给 40 分起步
    score += 40 
    
    # 特性加分
    if "zoetrope" in title_lower or "bad world" in title_lower:
        score += 50
    if "signed" in title_lower or "autographed" in title_lower:
        score += 60
    if "exclusive" in title_lower or "numbered" in title_lower:
        score += 30
        
    # 艺人加分：只要匹配到名单里的艺人，分数直接过百触发【特急】
    if any(fav.lower() in title_lower for fav in MY_FAVORITES):
        score += 100
        
    return score

def send_bark(header, title, link):
    """发送通知到 Bark"""
    # 如果分数高（含🔥），响报警音，否则响清脆音
    sound = "alarm" if "🔥" in header else "choochoo"
    # 对标题进行简单的编码处理
    push_url = f"{BARK_BASE_URL}/{header}/{title}?url={link}&sound={sound}&group=Vinyl2026"
    try:
        requests.get(push_url, timeout=10)
    except:
        print("推送发送失败")

def check_blood_records():
    print("--- 正在巡逻 Blood Records (Bad World) ---")
    url = "https://www.blood-records.co.uk/products.json"
    try:
        res = requests.get(url, timeout=15)
        data = res.json()
        for p in data['products']:
            # 1. 库存检查：只要有一个版本有货就报
            variants = p.get('variants', [])
            is_available = any(v.get('available', False) for v in variants)
            if not is_available:
                continue 
            
            title = p['title']
            # 2. 过滤黑名单
            if any(b.lower() in title.lower() for b in BLACKLIST):
                continue
            
            score = get_value_score(title)
            
            # 3. 构造快速加购链接 (半自动核心)
            v_id = variants[0].get('id') if variants else ""
            quick_link = f"https://www.blood-records.co.uk/cart/add?id={v_id}"
            
            # 4. 根据分数决定推送级别
            if score >= 100:
                send_bark("🔥【重磅特急】", title, quick_link)
            elif score >= 40:
                send_bark("🚀【检测到上新】", title, quick_link)
                
    except Exception as e:
        print(f"Blood Records 访问失败: {e}")

def check_rough_trade():
    print("--- 正在巡逻 Rough Trade (UK) ---")
    # 这里保持基础逻辑，因为 RT 结构较复杂，先用简单的 JSON 模式
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
        print("Rough Trade 访问受限或失败")

if __name__ == "__main__":
    check_blood_records()
    check_rough_trade()
