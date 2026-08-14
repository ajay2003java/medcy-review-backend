import urllib.request
import re

try:
    req = urllib.request.Request('https://kommodo.ai/i/eXVQP11nnRbLTYDOeJaN', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'<img[^>]+src="([^">]+)"', html)
    print("Found image URLs on the page:")
    for img in images:
        if img.startswith('http'):
            print(img)
except Exception as e:
    print(f"Error fetching URL: {e}")
