import requests
import pickle as pkl

r = requests.get('https://type.fit/api/quotes')
quotes = r.json()

with open('./quotes.pkl', 'wb') as f:
	pkl.dump(quotes, f)