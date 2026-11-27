"""Ping IndexNow (Bing, Yandex, Seznam, Naver; used by ChatGPT and Copilot search) with every blog URL."""
import glob, json, os, re, urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
HOST = "blog.emerald.dating"
key = [os.path.basename(f)[:-4] for f in glob.glob(os.path.join(ROOT, "static", "*.txt")) if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(f))][0]
urls = re.findall(r"<loc>([^<]+)</loc>", open(os.path.join(ROOT, "docs", "sitemap.xml")).read())
body = json.dumps({"host": HOST, "key": key, "keyLocation": f"https://{HOST}/{key}.txt", "urlList": urls}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
try:
    r = urllib.request.urlopen(req, timeout=30)
    print("IndexNow", r.status, len(urls), "urls")
except urllib.error.HTTPError as e:
    print("IndexNow", e.code, e.read()[:200])
