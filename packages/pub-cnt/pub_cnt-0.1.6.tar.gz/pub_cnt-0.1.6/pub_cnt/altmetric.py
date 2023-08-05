import time
import requests, json
import pandas as pd
import logging
from functools import reduce

def parse_data(data, keys):
  try:
    return reduce(lambda data, key: data[key], keys, data)
  except:
    return 'Not Available'

def construct_data_frame(data, id_type, _id):
  get_value = lambda field: [data[field]] if field in data.keys() else 'Not Available'
  
  df = pd.DataFrame({
    'given_' + id_type + '_id': _id,
    'doi': get_value('doi'),
    'pmid': get_value('pmid'),
    'title': get_value('title'),
    'journal': get_value('journal'),
    'published_on': get_value('published_on'),
    'score': get_value('score'),
    'one_year_old_score': parse_data(data, ['history', '1y']),
    'readers_count': get_value('readers_count'),
    'cited_by_posts_count': get_value('cited_by_posts_count'),
    'cited_by_tweeters_count': get_value('cited_by_tweeters_count'),
    'cited_by_feeds_count': get_value('cited_by_feeds_count'),
    'cited_by_msm_count': get_value('cited_by_msm_count'),
    'cited_by_accounts_count': get_value('cited_by_accounts_count'),
    'type': get_value('type'),
    'altmetric_id': get_value('altmetric_id'),
    'publication_url': get_value('url')
  }, index = [0])
  
  return df

def handle_user_input(doi = None, pmid = None, dois = None, pmids = None):
  if doi:
    return 'doi', [str(doi)]
  if pmid:
    return 'pmid', [str(pmid)]
  if dois:
    return 'doi', list(map(str, dois))
  if pmids:
    return 'pmid', list(map(str, pmids))
  
  return '', list('')

def get_response(id_type, _id):
  return requests.get('https://api.altmetric.com/v1/%s/%s' % (id_type, _id),
    headers = {'Accept': 'application/json'})

def get_data(doi = None, pmid = None, dois = None, pmids = None):
  id_type, ids = handle_user_input(doi, pmid, dois, pmids)
  result_df = pd.DataFrame({})
  
  for _id in ids:
    try:
      response = get_response(id_type, _id)
      
      while response.status_code == 429:
        logging.error('Rate is limited, waiting for renew rate...')
        time.sleep(3600)
        response = get_response(id_type, _id)
      
      while response.status_code == 502:
        logging.error('API under maintenance, waiting...')
        time.sleep(3600)
        response = get_response(id_type, _id)
      
      json_data = json.loads(response.text.encode('utf-8'))
    
    except:
      json_data = {}
      logging.error('Data unavailable for %s %s' % (id_type, _id))
    
    result_df = result_df.append(construct_data_frame(json_data, id_type, _id))
  
  return result_df
