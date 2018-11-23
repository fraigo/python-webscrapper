import sys
import os, bs4, requests
import pandas as pd
import urllib
import hashlib
import time

CACHE_EXPIRES = 60

def list_ids(container):
  return [item.get('id') for item in container]

def list_attribute(container, tag, attr, filter = {}):
  return [item.find(tag, attrs=filter ).get(attr) for item in container]

def list_text(container, tag, filter = {}):
  return [item.find(tag, attrs=filter ).text.strip() for item in container]

def parse_content(container): 
  organic = container.findAll('div', attrs={'data-tn-component':'organicJob'})
  ids = list_ids(organic)
  text = list_text(organic, 'a')
  links = list_attribute(organic, 'a', 'href')
  companies = list_text(organic, 'span', {'class':'company'})
  locations = list_text(organic, 'span', {'class':'location'})
  description = list_text(organic, 'span', {'class':'summary'})
  published = list_text(organic, 'span', {'class':'date'})
  frm = pd.DataFrame()
  frm['id'] = ids
  frm['text'] = text
  frm['link'] = links
  frm['comp'] = companies
  frm['loc'] = locations
  frm['desc'] = description
  frm['pub'] = published
  frm.set_index('id')
  #frm['rat'] = rating
  return frm

def get_response(url):
  PATH = os.path.join("cache")
  md5 = hashlib.md5()
  md5.update(url.encode('utf-8'))
  id = md5.hexdigest()
  
  PATH = os.path.join("cache",id)
  cached = False
  if os.path.exists(PATH):
    time1 = os.path.getmtime(PATH)
    time2 = time.time()
    if time2-time1 < CACHE_EXPIRES:
      cached = True
  if cached:
    print("Reading", PATH)
    with open(PATH, 'r') as content_file:
      response = content_file.read()
  else:
    print("Requesting", url)
    page = requests.get(url)
    response = page.text
    file = open(PATH, "w")
    file.write(response)
    file.close() 
  return response

def scrappe(url):
  response = get_response(url)
  soup = bs4.BeautifulSoup(response, 'lxml')
  container = soup.find(name='td', attrs={'id':'resultsCol'})
  res = pd.DataFrame()
  res = res.append(parse_content(container))
  return res

def get_name(name):
  filteredName = ''.join(x for x in name if x.isalpha())
  return filteredName

def save(name,res):
  PATH = os.path.join("data") 
  NAME = get_name(name)
  res.to_csv(os.path.join(os.path.join(PATH,NAME + ".csv")), index=None, sep=';', encoding='utf-8')
  res.to_json(os.path.join(os.path.join(PATH,NAME + ".json")), orient='records')

def get_url(search, location):
    QUERY = urllib.parse.urlencode({ 
        'as_and' : search, 
        'l' : location ,
        'radius' : 50,
        'limit' : 50,
        'sort' : 'date'
        })
    return "https://ca.indeed.com/jobs?" + QUERY + "&jt=all&fromage=any&psf=advsrch" 

