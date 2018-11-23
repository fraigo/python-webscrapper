import sys
from web import scrapper 

search = "Python"
if sys.argv[1]:
    search = sys.argv[1]
location = "Vancouver, BC"
url = scrapper.get_url(search, location)
res = scrapper.scrappe(url)
scrapper.save(search, res)
