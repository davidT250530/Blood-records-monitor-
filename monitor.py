import requests

# ===========================================
# 配置区域
# ===========================================

# 1. 你的 Bark 链接（请务必确认结尾有斜杠 /）
BARK_URL = "https://api.day.app/eRjoaMokHx5FK9qP4OxSNH/"

# 2. 屏蔽列表：不想收到的专辑关键词（不区分大小写）
BLACKLIST = ["Rio Kosta", "Unicorn", "test product"]

# 3. Rough Trade 关键词：只有包含这些词且不在黑名单的才提醒
RT_KEYWORDS = ["exclusive", "signed", "limited", "numbered", "vinyl"]

# ===========================================

def send_bark(title, buy_url, site_name):
    """发送 Bark 通知"""
    print(f"[{site_name}] 发现目标，尝试发送通知: {title}")
    target_url = f"{BARK_URL}{title}"
    payload = {
        "url": buy_url,
        "group": site_name,
        "sound": "calypso",
        "isArchive": "1" 
    }
    try:
        r = requests.get(target_url, params=payload, timeout=5)
        print(f"Bark 返回状态: {r.status_code}")
    except Exception as e:
        print(f"Bark 发送失败: {e}")

def check_blood_records():
    """监控 Blood Records"""
    print("开始检查 Blood Records...")
    url = "https://blood-records.co.uk/products.json"
    try:
        r = requests.get(url, timeout=10)
        products = r.json().get('products', [])
        for p in products:
            title = p['title']
            # 过滤黑名单
            if any(word.lower() in title.lower() for word in BLACKLIST):
                continue
            
            # 检查是否有货
            if any(v['available'] for v in p['variants']):
                # 获取第一个有货的变体 ID 构造快捷购买链接
                v_id = next(v['id'] for v in p['variants'] if v['available'])
                buy_url = f"https://blood-records.co.uk/cart/{v_id}:1"
                send_bark(f"BloodRecords有货: {title}", buy_url, "BloodRecords")
                return # 每次只报一个最新的
    except Exception as e:
        print(f"Blood Records 检查出错: {e}")

def check_rough_trade():
    """监控 Rough Trade"""
    print("开始检查 Rough Trade...")
    # 使用 API 获取按创建时间排序的最新的 5 个产品
    api_url = "https://api.roughtrade.com/search/products?sort=created_at_desc&per_page=5"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
        'Accept': 'application/json'
    }
    try:
        r = requests.get(api_url, headers=headers, timeout=15)
        data = r.json().get('data', [])
        
        for item in data:
            attr = item['attributes']
            title = attr['name']
            description = attr.get('description', '') or ""
            
            # 1. 过滤黑名单
            if any(word.lower() in title.lower() for word in BLACKLIST):
                continue
            
            # 2. 匹配限量关键词
            full_text = (title + description).lower()
            if any(k in full_text for k in RT_KEYWORDS):
                slug = attr['slug']
                product_url = f"https://www.roughtrade.com/en-gb/product/{slug}"
                send_bark(f"RoughTrade限量: {title}", product_url, "RoughTrade")
                return # 找到最新的限量版就停止
    except Exception as e:
        print(f"Rough Trade 检查出错: {e}")

if __name__ == "__main__":
    # 执行两个网站的检查
    check_blood_records()
    check_rough_trade()
