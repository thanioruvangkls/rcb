import time
import cloudscraper
from urllib.parse import urlparse
from bs4 import BeautifulSoup

# eg: https://gplinks.co/XXXX
url = input()

# =======================================

def gplinks_bypass(url: str):
    client = cloudscraper.create_scraper(allow_brotli=False)
    p = urlparse(url)
    final_url = f'{p.scheme}://{p.netloc}/links/go'

    res = client.head(url)
    header_loc = res.headers['location']
    param = header_loc.split('postid=')[-1]
    req_url = f'{p.scheme}://{p.netloc}/{param}'

    p = urlparse(header_loc)
    ref_url = f'{p.scheme}://{p.netloc}/'

    h = { 'referer': ref_url }
    res = client.get(req_url, headers=h, allow_redirects=False)
    bs4 = BeautifulSoup(res.content, 'html.parser')
    print ("\n\n\n",bs4)
    inputs = bs4.form.findAll("input", {"name": re.compile(r"token$")})
    data = { input.get('name'): input.get('value') for input in inputs }

    h = {
        'referer': ref_url,
        'x-requested-with': 'XMLHttpRequest',
    }
    time.sleep(10)
    print ("\n\n\n",req_url)
    print ("\n\n\n",final_url)
    print ("\n\n\n",data)
    res = client.post(final_url, headers=h, data=data)
    try:
        return res.json()['url'].replace('\/','/')
    except: return 'Something went wrong :('

# =======================================

print(gplinks_bypass(url))
