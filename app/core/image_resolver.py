import re
import urllib.request
import logging

logger = logging.getLogger(__name__)

def resolve_image_url(url: str | None) -> str | None:
    """
    Automatically converts webpage sharing URLs (e.g. Kommodo, Google Drive, Dropbox, Postimages)
    into direct raw image URLs so that browsers can display them inside <img> tags.
    """
    if not url or not isinstance(url, str):
        return url

    url = url.strip()
    if not url:
        return None

    # If it's already a direct CDN or image link, return as-is
    # (e.g., ends with .png, .jpg, .jpeg, .svg, .webp and is from a direct CDN)
    if "komododecks.com" in url and any(url.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".webp"]):
        return url

    # 1. Kommodo sharing links: https://kommodo.ai/i/<ID> or https://komododecks.com/i/<ID>
    kommodo_match = re.search(r'https?://(?:www\.)?kom(?:m)?odo(?:decks)?\.(?:ai|com)/i/([a-zA-Z0-9_-]+)', url)
    if kommodo_match:
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                content = response.read().decode('utf-8', errors='ignore')
                # Try finding og:image
                og_match = re.search(r'<meta\s+(?:property|name)=["\']og:image["\']\s+content=["\']([^"\']+)["\']', content)
                if og_match and og_match.group(1).startswith('http'):
                    return og_match.group(1)
                
                # Try finding Next.js JSON data
                next_match = re.search(r'"(?:ogImageUrl|imageUrl)":\s*"([^"]+)"', content)
                if next_match:
                    return next_match.group(1).replace(r'\/', '/')
        except Exception as e:
            logger.warning(f"Failed to auto-resolve Kommodo URL {url}: {e}")

    # 2. Google Drive sharing links: drive.google.com/file/d/<ID>/view or ?id=<ID>
    gdrive_match = re.search(r'drive\.google\.com/(?:file/d/|open\?id=)([a-zA-Z0-9_-]+)', url)
    if gdrive_match:
        file_id = gdrive_match.group(1)
        return f"https://lh3.googleusercontent.com/d/{file_id}"

    # 3. Dropbox links: www.dropbox.com/s/... -> raw=1
    if "dropbox.com" in url:
        if "dl=0" in url:
            return url.replace("dl=0", "raw=1")
        elif "raw=1" not in url:
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}raw=1"

    # 4. Postimages sharing page: https://postimg.cc/<ID>
    if "postimg.cc" in url and "i.postimg.cc" not in url:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=4) as response:
                content = response.read().decode('utf-8', errors='ignore')
                og_match = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\']([^"\']+)["\']', content)
                if og_match and og_match.group(1).startswith('http'):
                    return og_match.group(1)
        except Exception as e:
            logger.warning(f"Failed to auto-resolve Postimg URL {url}: {e}")

    return url
