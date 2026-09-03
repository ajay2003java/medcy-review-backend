import urllib.request
import re

url = 'https://kommodo.ai/i/NgcbnRrEVe2pchily1Un'
try:
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    # Try to find a direct image link
    matches = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', html)
    og_match = re.search(r'<meta property="og:image" content="([^"]+)"', html)
    
    if og_match:
        print("OG Image:", og_match.group(1))
    
    print("Other images found:")
    for m in matches:
        if 'logo' in m.lower() or 'bansal' in m.lower() or 'upload' in m.lower():
            print(m)
        elif 'kommodo' not in m.lower():
            print(m)
except Exception as e:
    print(f"Error: {e}")
