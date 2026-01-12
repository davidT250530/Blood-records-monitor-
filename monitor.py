import requests

# 1. 你的 Bark 链接
BARK_URL = "https://api.day.app/eRjoaMokHx5FK9qP4OxSNH/" 

# 2. 在这里填入你想屏蔽的专辑标题关键词（大小写不敏感）
# 比如你想屏蔽 Rio Kosta，就填入 ["Rio Kosta"]
BLACKLIST = ["Rio Kosta", "Unicorn"]

def check():
    url = "https://blood-records.co.uk/products.json"
    try:
        r = requests.get(url, timeout=10)
        products = r.json().get('products', [])
        for p in products:
            title = p['title']
            
            # 检查标题是否包含黑名单里的关键词
            if any(word.lower() in title.lower() for word in BLACKLIST):
                print(f"已跳过屏蔽专辑: {title}")
                continue
            
            # 只有不在黑名单里，且有货的情况下才发送通知
            if any(v['available'] for v in p['variants']):
                v_id = next(v['id'] for v in p['variants'] if v['available'])
                buy_url = f"https://blood-records.co.uk/cart/{v_id}:1"
                msg = f"发现上新: {title}"
                
                # 发送通知
                target_url = f"{BARK_URL}{msg}"
                payload = {
                    "url": buy_url,
                    "group": "BloodRecords",
                    "sound": "calypso"
                }
                requests.get(target_url, params=payload)
                print(f"通知已发送: {title}")
                return # 每次只发一个最靠前的，防止刷屏
    except Exception as e:
        print(f"检查出错: {e}")

if __name__ == "__main__":
    check()
