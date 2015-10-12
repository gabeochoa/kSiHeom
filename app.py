from flask import Flask, redirect, url_for, session, request, render_template
import datetime
import requests
import json

app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
	return ""    


if __name__ == '__main__':
    app.run()
