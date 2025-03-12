import os
from typing import List

import requests
from ratelimit import limits, RateLimitException
from backoff import on_exception, expo
import streamlit as st
from requests_cache import CachedSession
from requests_ratelimiter import LimiterAdapter

BASE_API_URL = 'https://graph.instagram.com'

access_token = os.getenv('INSTAGRAM_APP_ID') + '|' + os.getenv('INSTAGRAM_ACCESS_TOKEN')

# use cached session to avoid api calls on every update
session = CachedSession('instagram_cache', backend='sqlite', expire_after=360, allowable_codes=(200, 400))

# limit request rate
# limiter_adapter = LimiterAdapter(per_second=5, per_hour=10)
# session.mount('https://graph.instagram.com')


# @on_exception(expo, RateLimitException, max_tries=3)
# @limits(calls=5, period=1)
# def fresh_api_request(url):
#     print(url)
#     r = session.get(url, timeout=5)
#     if not r.ok:
#         print('Instagram api error: ', r.text)
#     print(r.from_cache)
#     return r


def api_request(url_template, **params):
    """
    Makes a GET request to the API.
    :param url_template: url string with parameters enclosed in {}
    :param params: parameters to insert into the url template. access_token and base_url are already provided
    :return: json contents of the response
    """
    url = url_template.format(**params, access_token=access_token, api_url=BASE_API_URL)
    r = session.get(url, timeout=5)
    # if not r:
    #     r = fresh_api_request(url)

    if not r or not r.ok:
        raise Exception('Instagram api error')
    print(r.from_cache)
    return r.json()


def get_feed():
    url = '{api_url}/me/media?fields=id,caption,media_type&access_token={access_token}'
    return api_request(url)['data']


def get_media(media_id: str):
    url = '{api_url}/{media_id}?fields=caption,media_type,media_url,permalink,timestamp,' \
          'children&access_token={access_token}'
    response = api_request(url, media_id=media_id)
    return response


def get_simple_media(media_id: str):
    url = '{api_url}/{media_id}?fields=media_type,media_url' \
          '&access_token={access_token}'
    response = api_request(url, media_id=media_id)
    return response


def get_carousel_children(media_id: str) -> List[str]:
    url = '{api_url}/{media_id}?fields=children&access_token={access_token}'
    response = api_request(url, media_id=media_id)
    return [child['id'] for child in response['children']['data']]


def display_carousel(media_id: str):
    displayed_child = get_simple_media(get_carousel_children(media_id)[0])
    st.image(displayed_child['media_url'])


def display_image(media_id: str):
    st.image(get_simple_media(media_id)['media_url'])


def form_feed():
    response = get_feed()
    last_media = response[0]
    if last_media['media_type'] == 'CAROUSEL_ALBUM':
        display_carousel(last_media['id'])
    else:
        display_image(last_media['id'])
    st.text(last_media['caption'])


def widget():
    st.markdown('## Instagram')
    try:
        form_feed()
    except Exception:
        st.error('Failed to load Instagram feed.')
