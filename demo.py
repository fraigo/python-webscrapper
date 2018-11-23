import sys
from web import scrapper 

search = "Python"
if sys.argv[1]:
    search = sys.argv[1]
LOCATION = "Vancouver, BC"
url = scrapper.get_url(search, LOCATION)
scrapper.scrappe(search,url)