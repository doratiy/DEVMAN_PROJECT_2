from urllib.parse import urlparse
from Tools.scripts.make_ctype import method
import requests
from dotenv import load_dotenv
from requests.exceptions import HTTPError
import os


def shorten_link(vk_token, url):
    params = {
        'access_token': vk_token,
        'v': 5.199,
        "private": 0,
        "url": url,
    }
    method_url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(method_url, params=params)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(vk_token, parsed_key):
    method_url = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': vk_token,
        'v': 5.199,
        "key": parsed_key,
        "interval": "forever",
        "extended": 0
    }
    response = requests.get(method_url , params)
    response.raise_for_status()
    if 'error'  in response.text:
        raise HTTPError
    else:
        clicks_count = response.json()['response']["stats"]
        return clicks_count


def is_shorten_link(vk_token, parsed_key):
    method_url  = "https://api.vk.ru/method/utils.getLinkStats"
    params = {
        'access_token': vk_token,
        'v': 5.199,
        "key": parsed_key,
        "interval": "forever",
        "extended": 0
    }
    response = requests.get(method_url, params)
    response.raise_for_status()
    return 'error' not in response.text


if __name__ == "__main__":
    load_dotenv()
    vk_token = os.environ["VK_TOKEN"]
    url = input('введите ссылку')
    parsed_url = urlparse(url)
    parsed_key = parsed_url.path[1:]
    is_short = is_shorten_link(vk_token, parsed_key)
    if is_short:
        clicks_link = count_clicks(vk_token, parsed_key)
        print(clicks_link)
    else:
        short_url = shorten_link(vk_token, url)
        print(short_url)
