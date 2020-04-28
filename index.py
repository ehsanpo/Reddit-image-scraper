import os
import time
import praw
import wget
import re
import pickle as pkl
import json
import requests
import cv2
from PIL import Image, ImageDraw, ImageFont
import textwrap
import random
from instapy_cli import client
from dotenv import load_dotenv
load_dotenv()


client_id = os.environ.get("client_id")
client_secret = os.environ.get("client_secret")
user_agent = os.environ.get("user_agent")
subreddit = os.environ.get("subreddit")
limit = int(os.environ.get("limit"))
addtext_to = int(os.environ.get("addtext"))
W, H = ( int(os.environ.get("width")) , int(os.environ.get("height")) )
random_font_nr = "font2.ttf"
checkWords = ['i.imgur.com',  'jpg', 'png', 'gif', 'gfycat.com', 'webm',]
gyfwords = ['gfycat.com']


reddit = praw.Reddit(client_id=client_id,
					 client_secret=client_secret,
					 user_agent=user_agent)



def addtext (img,path,textOB):
	print ('[LOG] Adding text')
	image = Image.open(path + img )
	draw = ImageDraw.Draw(image)
	 
	# desired size
	#random_font_nr = 'font' + str(random.randint(1,3)) + '.ttf' 
	
	font = ImageFont.truetype(random_font_nr , size=120)
	 
	# starting position of the message
	(x, y) = (50, 50)

	message = textOB['text']

	para = textwrap.wrap(message , width=20)
	MAX_W, MAX_H = 1080, 1000

	current_h, pad = 50, 10
	for line in para:
	    w, h = draw.textsize(line, font=font)

	   	#textshadowns
	    draw.text(((MAX_W - w) / 2 -1, current_h), line, font=font, fill = "#000")
	    draw.text(((MAX_W - w) / 2+1, current_h), line, font=font, fill = "#000")
	    draw.text(((MAX_W - w) / 2, current_h-1), line, font=font, fill = "#000")
	    draw.text(((MAX_W - w) / 2, current_h+1), line, font=font, fill = "#000")

	    #original text
	    draw.text(((MAX_W - w) / 2, current_h), line, font=font)
	    current_h += h + pad

	# draw the message on the background
	
	#draw.text((x, y), message, fill=color, font=font)
	(x, y) = (800, 1000)
	font = ImageFont.truetype(random_font_nr , size=50)
	name = textOB['author']
	draw.text((x, y), name, fill="#fff", font=font)
	
	# save the edited image
	
	image.save(path + img)

	return;


#GET Qu
quotes = []
with open('quotes.pkl', 'rb') as f:
	quotes = pkl.load(f)
  
#GET USED IMAGES
already_done = []
with open('save.pkl', 'rb') as f:
	already_done = pkl.load(f)



for submission in reddit.subreddit(subreddit).hot(limit=limit):
	print(submission.url)
	url_text = submission.url
	has_domain = any(string in url_text for string in checkWords)
	print ('[LOG] Getting url:  ' + url_text)
	is_gifcat = any(string in url_text for string in gyfwords)
	if submission.id not in already_done and has_domain:
		if is_gifcat:
			url = re.sub('http://.*gfycat.com/', '', url_text)
			url_text = 'http://giant.gfycat.com/' + url + '.gif' 

		img_name  = 'img-'+str(time.time())[-8:-3] + url_text[-4:]
		img_path = "./img/"

		wget.download(url_text, img_path + img_name )

		imgx = cv2.imread(img_path + img_name, cv2.IMREAD_UNCHANGED) 
		dim = (W, H)
		imgx_resized = cv2.resize(imgx , dim)
		cv2.imwrite(img_path+ img_name, imgx_resized )
		already_done.append(submission.id)
		
		if addtext_to :
			addtext(img_name,img_path,quotes[0])
		
		print ('[LOG] Done Getting ' + url_text)
		quotes.pop(0)


with open('./save.pkl', 'wb') as f:
	pkl.dump(already_done, f)

with open('./quotes.pkl', 'wb') as f:
	pkl.dump(quotes, f)



