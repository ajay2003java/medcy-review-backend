import urllib.request
import re

url = 'https://kommodo.ai/i/p3NyglOoQsrkeA1M6z5T'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    for line in html.split('\n'):
        if 'image' in line or 'plain-apac' in line or 'komodo' in line:
            print(line.strip())
except Exception as e:
    print(e)
