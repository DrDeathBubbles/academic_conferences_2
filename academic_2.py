# A small programme to
import requests


r = requests.get('http://export.arxiv.org/api/query?search_query=all:electron')

r.text
