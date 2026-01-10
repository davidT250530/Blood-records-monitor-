import requests

# 1. https://api.day.app/eRjoaMokHx5FK9qP4qRJu3/
BARK_URL = "https://api.day.app/eRjoaMokHx5FK9qP4qRJu3/"

def check():
    url = "https://blood-records.co.uk/products.json"
    try:
        r = requests.get(url, timeout=10)
        products = r.json().get('products', [])
        for p in products:
            # 逻辑：只要有任何变体有货且标题没写已售罄
            if any(v['available'] for v in p['variants']):
                v_id = next(v['id'] for v in p['variants'] if v['available'])
                buy_url = f"https://blood-records.co.uk/cart/{v_id}:1"
                msg = f"发现上新: {p['title']}"
                # 发送通知
                requests.get(f"{BARK_URL}{msg}?url={buy_url}&sound=calypso")
                print(f"通知已发送: {p['title']}")
                return 
    except Exception as e:
        print(f"检查出错: {e}")

if __name__ == "__main__":
    check()
