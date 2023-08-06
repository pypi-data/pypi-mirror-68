def clean_text(text):
  import string
  punctuations = string.punctuation.replace('-', '').replace("'", '') + '\n'
  text = [i for i in text if i not in punctuations]
  text = ''.join(text)
  text = text.strip()
  return text

def clean_stipend(text):
  import numpy as np
  text = text.lower().strip()
  text = [i for i in text]
  a = ''
  final_text = ''
  for i in text:
    a += i
    try:
      np.float64(a)
      final_text = a
    except:
      break
  if final_text:
    return np.float64(final_text)
  return np.nan

def clean_apply_by(text):
  import numpy as np
  f = text.find("'")
  text = text[:f] + ' 2020'
  if text == 'Not Provide 2020':
    return np.nan
  return text

def apply_by_to_date(text):
  import numpy as np
  from datetime import datetime
  try:
    a = datetime.strptime(text, '%d %b %Y')
    return a
  except:
    return np.nan

def get_internshala_internships(url, n = 0):
  import numpy as np
  import pandas as pd
  import requests 
  from bs4 import BeautifulSoup
  all_items = []
  no_internship_text = ":( Sorry, We couldn't find internships matching your requirements."
  while True:
    print(f'n is {n}')
    if n:
      url = url + f'/page-{n}'
    try:
      html = requests.get(url)
      soup = BeautifulSoup(html.content, 'lxml')
      all_internship = soup.find_all('div', class_ = 'individual_internship')
      text = all_internship[0].find('h4').text
      if text == no_internship_text:
        print(no_internship_text)
        break
      l = len(all_internship)
      n2 = 0
      for i in all_internship:
        try:
          id = i.get('internshipid')
          location = i.find_all('a', class_ = 'location_link')[0].text
          link = 'https://internshala.com/' + i.find_all('a')[0].get('href')
          td = i.find_all('table')[0].find_all('td')
          start_date = td[0].text
          duration = td[1].text
          stipend = td[2].text
          posted_on = td[3].text
          apply_by = td[4].text
          items = [id, location, start_date, duration, stipend, posted_on, apply_by]
          items = list(map(clean_text, items))
          items.insert(2, link)
          del id, location, link, start_date, duration, stipend, posted_on, apply_by
          all_items.append(items)
          n2 += 1
        except:
          continue
      n += 1
    except Exception as e:
      print(f'{e.__class__.__name__}:--- {e.args[0]}')
      break
  if len(all_items) == 0:
    return no_internship_text
  df = pd.DataFrame(np.array(all_items), columns = ['id', 'location', 'link', 'start_date', 'duration', 'stipend', 'posted_on', 'apply_by'])
  df.drop_duplicates(inplace = True)
  df['stipend'] = df.stipend.apply(clean_stipend)
  df['apply_by'] = df['apply_by'].apply(clean_apply_by)
  df['apply_by'] = df['apply_by'].apply(apply_by_to_date)
  df.dropna(inplace = True)
  return df
