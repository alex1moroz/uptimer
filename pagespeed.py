import requests
import json
import re as regular
from dynaconf import settings

url = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url='
token = settings.PSTOKEN


def re(text):
    if len(text) == 0:
        content = 0
    else:
        content = regular.match(r'^[0-9.]*', text).group(0)
    return content


def ps(link):
    try:
        query = requests.get(f'{url}{link}&strategy=mobile&key={token}').content
        js = json.loads(query)
        speed = js['lighthouseResult']['audits']['speed-index']['displayValue']
        result = re(speed)
    except KeyError:
        result = None
    return result
