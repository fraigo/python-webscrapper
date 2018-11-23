import sys
import os, bs4, requests
import pandas as pd
import urllib

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
  ratings = container.findAll('div', attrs={'class':'sjcl'})
  #rating = list_text(ratings, 'span', {'class': 'slNoUnderline'})
  print(len(ratings))
  frm = pd.DataFrame()
  frm['id'] = ids
  frm['text'] = text
  frm['link'] = links
  frm['comp'] = companies
  frm['loc'] = locations
  frm['desc'] = description
  frm['pub'] = published
  #frm['rat'] = rating
  return frm

def scrappe( name, url):
  print(url)
  res = pd.DataFrame()
  PATH = os.path.join("data") 
  page = requests.get(url)
  soup = bs4.BeautifulSoup(page.content, 'lxml')
  container = soup.find(name='td', attrs={'id':'resultsCol'})
  res = res.append(parse_content(container))
  res.to_csv(os.path.join(os.path.join(PATH,name + ".csv")), index=None, sep=';', encoding='utf-8')
  res.to_json(os.path.join(os.path.join(PATH,name + ".json")), orient='records')

def get_url(search, location):
    QUERY = urllib.parse.urlencode({ 
        'as_and' : search, 
        'l' : location ,
        'radius' : 50,
        'limit' : 50,
        'sort' : 'date'
        })
    return "https://ca.indeed.com/jobs?" + QUERY + "&jt=all&fromage=any&psf=advsrch" 

