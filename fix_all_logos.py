import urllib.request
import re
from sqlalchemy import create_engine, text

# Connection pooling URI for Production
DB_URL = "postgresql://postgres.saoawnguumcsnmmzudgv:RebT4aswj8raE6yB@aws-0-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, name, logo_url FROM clinic"))
        clinics = result.fetchall()
        
        for c in clinics:
            if c.logo_url and 'kommodo.ai' in c.logo_url:
                print(f"Fixing {c.name} with URL {c.logo_url}")
                try:
                    req = urllib.request.Request(c.logo_url, headers={'User-Agent': 'Mozilla/5.0'})
                    html = urllib.request.urlopen(req).read().decode('utf-8')
                    images = re.findall(r'<img[^>]+src="([^">]+)"', html)
                    
                    for img in images:
                        if img.startswith('http'):
                            true_logo = img
                            conn.execute(text("UPDATE clinic SET logo_url = :logo WHERE id = :id"), {"logo": true_logo, "id": c.id})
                            conn.commit()
                            print(f" -> Updated {c.name} successfully to {true_logo}")
                            break
                except Exception as ex:
                    print(f" -> Failed to fix {c.name}: {ex}")
            else:
                print(f"Skipping {c.name} (URL OK or None: {c.logo_url})")
except Exception as e:
    print(f"Error: {e}")
