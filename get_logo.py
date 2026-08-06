import urllib.request
import re

try:
    html = urllib.request.urlopen('https://www.vizagivf.com/').read().decode('utf-8')
    images = re.findall(r'<img[^>]+src=[\'"]([^\'"]+)[\'"]', html)
    print("Images found:")
    for img in images:
        if 'logo' in img.lower():
            print("LOGO URL:", img)
except Exception as e:
    print("Error:", e)
