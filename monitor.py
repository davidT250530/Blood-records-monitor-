import requests
import time

# ================= 配置区 =================
# 1. 你的 Bark 推送链接 (末尾不需要斜杠)
BARK_BASE_URL = "你的Bark链接" 

# 2. 你的黑名单 (不想看到的艺人)
BLACKLIST = ["Rio Kosta", "Another Artist"]

# 3. 你的白名单 (只要出现这个艺人，不管是不是签名版，立刻最高级警报)
MY_FAVORITES = ["Lana Del Rey", "Taylor Swift", "The 1975"]

# 4. Rough Trade API 地址 (沿用你之前的成功路径)
RT_API_URL = "https://www.roughtrade.com/en-gb/api/products?page=1&per_page=40"
# ==========================================

def get_value_score(title):
    """智能打分系统：分数越高，越值得抢"""
    score = 0
    title_lower = title.lower()
    
    # 关键词加分
    if "signed" in title_lower or "autographed" in title_lower:
        score += 60  # 签名版（价值核心）
    if "exclusive" in title_lower:
        score += 30  # 独家版本
    if "limited" in title_lower:
        score += 10  # 限量标注
        
    # 白名单加分（心头好无脑冲）
    if any(fav.lower() in title_lower for fav in MY_FAVORITES):
        score += 100
        
    return score

def send_bark(header, title, link):
    """分级推送函数"""
    print(f"准备推送: {header} - {title}")
    
    # 根据标题判断是否包含火苗图标，如果是特级预警，可以设置更响亮的铃声
    sound = "alarm" if "🔥" in header else "choochoo"
    
    # 组装 Bark URL
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
            # 过滤黑名单
            if any(b.lower() in title.lower() for b in BLACKLIST):
                continue
            
            score = get_value_score(title)
            link = f"https://www.blood-records.co.uk/products/{p['handle']}"
            
            if score >= 60:
                send_bark("🔥【重磅签名】Blood Records", title, link)
            elif score >= 30:
                send_bark("📢【独家限量】Blood Records", title, link)
            # 普通款就不推送了，防止骚扰
    except Exception as e:
        print(f"Blood Records 错误: {e}")

def check_rough_trade():
    print("--- 正在巡逻 Rough Trade ---")
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        # 如果 RT 需要特定的 API 格式，请确保 URL 正确
        res = requests.get(RT_API_URL, headers=headers, timeout=15).json()
        # 注意：RT 的 JSON 结构可能与 Blood 不同，通常在 data 或 products 键下
        products = res.get('data', []) if isinstance(res, dict) else []
        
        for p in products:
            title = p.get('name', p.get('title', ''))
            if not title or any(b.lower() in title.lower() for b in BLACKLIST):
                continue
                
            score = get_value_score(title)
            # 自动生成链接，RT 通常使用 slug 或 sku
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

