import requests
import json
from datetime import datetime, timedelta

API_KEY = os.environ['NEWSAPI_KEY']
today = datetime.utcnow().strftime('%Y-%m-%d')
yesterday = (datetime.utcnow() - timedelta(1)).strftime('%Y-%m-%d')

# 获取地缘与经济新闻
url = f'https://newsapi.org/v2/everything?q=(geopolitics OR "central bank" OR economy OR oil)&from={yesterday}&to={today}&sortBy=publishedAt&language=en&pageSize=10'
resp = requests.get(url, headers={'X-Api-Key': API_KEY})
articles = resp.json().get('articles', [])

geopolitical = []
fed = []
china = []
for a in articles[:8]:
    t = a['title'] or ''
    desc = a['description'] or ''
    item = {'tag': a['source']['name'], 'text': t}
    if any(w in t.lower() for w in ['fed', 'inflation', 'interest rate', 'powell']):
        fed.append(item)
    elif any(w in t.lower() for w in ['china', 'beijing', 'xi', 'pla']):
        china.append(item)
    else:
        geopolitical.append(item)

# 确保每个类别至少有占位
if not geopolitical:
    geopolitical = [{'tag':'地缘','text':'暂无重大地缘新闻'}]
if not fed:
    fed = [{'tag':'美联储','text':'暂无最新货币政策动态'}]
if not china:
    china = [{'tag':'中国','text':'暂无中国经济要闻'}]

report = {
    "date": today,
    "generatedAt": datetime.utcnow().isoformat() + 'Z',
    "geopolitical": geopolitical[:4],
    "fedPolicy": fed[:3],
    "chinaEconomy": china[:3],
    "marketReview": {
        "may6": "节后修复行情，科技与资源领涨。",
        "may7": "情绪维持积极，涨价链与AI线轮动。"
    },
    "may8Outlook": {
        "trend": "震荡偏强，科技线存内生调整压力。",
        "sectors": [
            {"name":"科技主线","reason":"AI资本开支上修"},
            {"name":"涨价链条","reason":"PPI转正，油价高位"},
            {"name":"新能源","reason":"替代需求提升"},
            {"name":"高股息","reason":"防御配置"}
        ],
        "risks": ["科技过热","美联储鹰派","地缘升级"]
    },
    "nextWeekOutlook": {
        "trend": "特朗普访华成关键变量，若积极则上冲，反之震荡。",
        "keyEvent": "5.14-15特朗普访华 + 美联储换帅",
        "sectorsToWatch": ["国产算力","AI应用","有色","新能源"],
        "risks": [
            {"scenario":"访华不及预期","impact":"股市短期承压"},
            {"scenario":"中东停火破裂","impact":"油价飙升冲击情绪"}
        ]
    },
    "marketSentiment": {
        "current": "谨慎乐观",
        "score": 72,
        "description": "政策面与基本面改善，等待关键外交事件落地"
    }
}

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
