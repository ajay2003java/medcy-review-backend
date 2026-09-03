import urllib.request
import re

url = 'https://kommodo.ai/i/NgcbnRrEVe2pchily1Un'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Print lines that look like they have an image
    for line in html.split('\n'):
        if '.png' in line or '.jpg' in line or 'image' in line:
            print(line.strip())
except Exception as e:
    print(e)

