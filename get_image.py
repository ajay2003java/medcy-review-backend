import urllib.request
import re

try:
    req = urllib.request.Request('https://kommodo.ai/i/HC4TTimm9fPrPd7AivDZ', headers={'User-Agent': 'Mozilla/5.0'})
    html = urllib.request.urlopen(req).read().decode('utf-8')
    images = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html)
    print("Images found on kommodo.ai page:")
    for img in images:
        print(img)
    
    # Also look for og:image meta tags
    meta_images = re.findall(r'<meta[^>]+property=[\'"]og:image[\'"][^>]+content=[\'"]([^\'"]+)[\'"]', html)
    print("Meta images found:")
    for img in meta_images:
        print(img)
except Exception as e:
    print("Error:", e)
