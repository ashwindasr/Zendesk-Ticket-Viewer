import os

import requests
from flask import render_template, redirect

from app import app

CREDENTIALS = os.environ['EMAIL'], os.environ['PASSWORD']
session = requests.Session()
session.auth = CREDENTIALS
SERVER = os.environ['MY_SERVER']
ZENDESK = f'https://{SERVER}.zendesk.com'
base_url = f'{ZENDESK}/api/v2/tickets'
url = f'{ZENDESK}/api/v2/tickets.json?page[size]=25'


@app.route('/')
def index():
    return redirect("/posts")


@app.route('/posts')
def posts_index():
    posts = get_response_json(url)

    prev_link = posts['links']['prev']
    next_link = posts['links']['next']

    prev_flag = True if \
        session.get(prev_link).json()['tickets'] != [] \
        else False  # Checking to see if the 'prev' link has any tickets or if its empty
    next_flag = True if \
        session.get(next_link).json()['tickets'] != [] \
        else False  # Checking to see if the 'next' link has any tickets or if its empty

    return render_template("posts.html", posts=posts['tickets'], prev_flag=prev_flag, next_flag=next_flag)


@app.route('/posts/next')
def posts_next():
    global url
    url = get_response_json(url)['links']['next']
    return redirect("/posts")


@app.route('/posts/back')
def posts_back():
    global url
    url = get_response_json(url)['links']['prev']
    return redirect("/posts")


@app.route('/posts/show/<int:post_id>')
def show(post_id):
    show_url = base_url + f"/{post_id}"
    post = get_response_json(show_url)
    return render_template("show.html", post=post['ticket'], post_id=post_id)


# Utility function to get the json response
def get_response_json(get_url):
    response = session.get(get_url)
    return response.json()
