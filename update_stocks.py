import json
import urllib.request
from datetime import datetime

def update_stocks():
    stocks = {}

    try:
        twse_url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'
        req = urllib.request.Request(twse_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                code = item.get('Code', '').strip()
                name = item.get('Name', '').strip()
                price_str = item.get('ClosingPrice', '').replace(',', '').strip()
                if code and price_str and price_str != '--':
                    try:
                        stocks[code] = {"n": name, "p": float(price_str)}
                    except ValueError:
                        pass
    except Exception as e:
        print(f"TWSE Fetch Error: {e}")

    try:
        tpex_url = 'https://www.tpex.org.tw/openapi/v1/tpex_mainboard_daily_close_quotes'
        req = urllib.request.Request(tpex_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            for item in data:
                code = item.get('SecuritiesCompanyCode', '').strip()
                name = item.get('CompanyName', '').strip()
                price_str = item.get('Close', '').replace(',', '').strip()
                if code and price_str and price_str != '--':
                    try:
                        stocks[code] = {"n": name, "p": float(price_str)}
                    except ValueError:
                        pass
    except Exception as e:
        print(f"TPEx Fetch Error: {e}")

    output = {
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "stocks": stocks
    }

    with open('stocks.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, separators=(',', ':'))

if __name__ == '__main__':
    update_stocks()