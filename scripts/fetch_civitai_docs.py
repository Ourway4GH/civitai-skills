import os
import re
import time
import urllib.request
from pathlib import Path

BASE_INDEX = "https://developer.civitai.com/site/llms.txt"
PROJECT_DOCS = Path(__file__).resolve().parent.parent / "docs"
PROJECT_DOCS.mkdir(parents=True, exist_ok=True)

print("Fetching index from", BASE_INDEX)
req = urllib.request.Request(BASE_INDEX, headers={"User-Agent": "Mozilla/5.0"})
index_content = urllib.request.urlopen(req).read().decode("utf-8")

raw_urls = re.findall(r'https://developer\.civitai\.com/site/[^\s\)\>]+?\.md', index_content)
urls = sorted(list(set(raw_urls)))

print(f"Discovered {len(urls)} unique markdown pages to fetch:")

for idx, url in enumerate(urls, 1):
    rel_path = url.replace("https://developer.civitai.com/site/", "")
    proj_target = PROJECT_DOCS / rel_path
    proj_target.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[{idx}/{len(urls)}] Fetching {rel_path}...")
    try:
        r = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/markdown"
            }
        )
        with urllib.request.urlopen(r, timeout=15) as resp:
            md_bytes = resp.read()
            proj_target.write_bytes(md_bytes)
            print(f"    Saved {len(md_bytes)} bytes -> {proj_target}")
    except Exception as e:
        print(f"    ERROR fetching {url}: {e}")
    time.sleep(0.3)

print("All downloads finished!")
