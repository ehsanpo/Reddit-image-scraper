
import pickle as pkl

quotes = []

with open('./save.pkl', 'wb') as f:
	pkl.dump(quotes, f)