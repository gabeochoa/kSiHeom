#!/usr/bin/python
import praw # reddit api
import urllib # get images from url
import os # makes directories
import time # used to rerun mainFunc every 30 sec
import requests # used to get html for BS
from imgurpython import ImgurClient #allows fix of image albums
import json #used to parse gfycat links
from keys import *
import random 

names = []

def parsefile():
	global names
	f = open('config.txt', 'r')
	cont = True
	strs = []
	line = ''
	while cont:
		line = f.read()
		for partial in line.split('\n'):
			if partial != '' :
				names.append(partial)
		else :
			cont = False
	print(names)
	return

def download_album_images(aid, filename, postTitle):
	client = ImgurClient(im_client, im_secret)
	imgs = None
	try:
		imgs = client.get_album_images(aid)
	except Exception:
		return
	#print("Downloading Album: " +postTitle)
	if not os.path.exists(filename+postTitle):
		os.mkdir(filename+postTitle)
	for image in imgs:
		fn = filename + postTitle + os.sep + ((image.link).split(".com/"))[1]
		downloadImage(image.link, fn, postTitle)
	return


def get_photo():
	return main()

def mainfunc():
	r = praw.Reddit(user_agent='KSiheom by /u/gabe1118 v0.1')
	name = random.choice(names)
	print(name)
	#print(dir(r.get_subreddit('kpics')))
	piclist = []
	for result in r.get_subreddit('kpics').search(name):
		#print dir(result)
		#print(result.url)
		#return result.url;

		piclist.append(result.url)
	return random.choice(piclist)
	'''
	for subreddit, keywords in subreddits.items():
		if not os.path.exists(subreddit):
			os.makedirs(subreddit)
		submissions = r.get_subreddit(subreddit).get_new(limit=1000)
		downloadAll = False
		if (keywords[0]).strip() == '*':
			#print("downloading all images")
			downloadAll = True

		for x in submissions:
			strs = str(x)
			postTitle = (strs.split("::"))[1]
			for Ina in keywords:
				Iname = Ina.strip()
				fn = subreddit+os.sep
				if not downloadAll:
					fn += Iname + os.sep
				if not os.path.exists(fn):
					os.mkdir(fn)
				if not matchKeyword(postTitle.lower(), Iname.lower(), downloadAll):
					continue
				else :
					savefile(subreddit, x, x.url, fn, postTitle)
	'''

def matchKeyword(postTitle, curKeyword, downloadAll):
	if downloadAll:
		return True
	if postTitle.find(curKeyword) != -1: 
		return True
	else:
		return False

	return False

def savefile(subreddit, submission, url, filename, postTitle):
	while os.sep in postTitle :
		postTitle = postTitle.replace(os.sep, '-')
	while '/' in postTitle :
		postTitle = postTitle.replace('/', '-')
	while '\\' in postTitle :
		postTitle = postTitle.replace('/', '-')

	#destroy for unicode characters. 
	postTitle = postTitle.decode('unicode_escape').encode('ascii','ignore')
	if '.jpg' not in url and '.png' not in url and '.gif' not in url:
		if 'http://imgur.com/a/' in url:
			# This is an album submission.
			albumId = url[len('http://imgur.com/a/'):]
			download_album_images(albumId, filename, postTitle)	
		if 'gfycat.com' in url:
			downloadURL, filenameToSave = parsegfycat(url)
			
			if not os.path.exists(filename):
				os.mkdir(filename)

			if not os.path.isfile( filename + os.sep + filenameToSave):
				downloadImage(downloadURL, filename + os.sep + filenameToSave, postTitle)
	else :
		if '.jpg' in url:
			postTitle += '.jpg'
		if '.png' in url:
			postTitle += '.png'
		if '.gif' in url:
			postTitle += '.gif'
		if not os.path.isfile( filename + os.sep + postTitle):  
			downloadImage(url, filename + os.sep + postTitle, postTitle)

def parsegfycat(url):
	#http://gfycat.com/cajax/get/
	parsename = 'http://gfycat.com/cajax/get/'
	ext = url.split("gfycat.com/",1)[1] 
	if '.webm' in ext: #good this is our filename
		ext = ext.replace('.webm', '')
	
	parsename += ext

	json_data = requests.get(parsename)
	data = json.loads(json_data.text)
	
	newurl = (data['gfyItem'])['webmUrl']
	fnts = ext + '.webm'

	#print (newurl)
	return newurl, fnts

def downloadImage(url, filename, postTitle):
	#http://stackoverflow.com/questions/16694907/how-to-download-large-file-in-python-with-requests-py
	if os.path.isfile(filename):
		return
	r = requests.get(url, stream=True)
	with open(filename, 'wb') as f:
		for chunk in r.iter_content(chunk_size=1024): 
			if chunk: # filter out keep-alive new chunks
				f.write(chunk)
				f.flush()
	return

def main():
	parsefile()
	return mainfunc()

if __name__ == '__main__':
	main()




