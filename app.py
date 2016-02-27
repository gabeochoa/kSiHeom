from flask import Flask, redirect, url_for, session, request, render_template
import datetime
import requests
import json
import kpd

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/random.html')
def random_quiz():
	purl = kpd.get_photo()
	return render_template("random.html", purl=purl, pcode=getCode(purl))

def getCode(purl):
	if('gfycat.com' in purl):
		return '<div class="gfyitem" data-id="'+purl.split('.com/')[1]+'" ></div>'
	else:
		return '<img src="' +purl +'"/>'

if __name__ == '__main__':
    app.run()
