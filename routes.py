import os

import requests
from flask import render_template, redirect

from app import app

CREDENTIALS = os.environ['EMAIL'], os.environ['PASSWORD']
session = requests.Session()
session.auth = CREDENTIALS
SERVER = os.environ['MY_SERVER']
ZENDESK = f'https://{SERVER}.zendesk.com'
base_url = f'{ZENDESK}/api/v2'
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

    total_posts_count = session.get(f"{base_url}/tickets/count").json()['count']['value']
    current_page_count = len(posts['tickets'])
    requester_names = get_requester_names(posts['tickets'])

    return render_template("posts.html", posts=posts['tickets'], prev_flag=prev_flag, next_flag=next_flag,
                           total_posts_count=total_posts_count, current_page_count=current_page_count,
                           requester_names=requester_names)


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
def show_post(post_id):
    show_url = base_url + f"/tickets/{post_id}"
    post = get_response_json(show_url)

    requester_id = post['ticket']['requester_id']
    requester_name = get_requester_data(requester_id)

    return render_template("show.html", post=post['ticket'], post_id=post_id, requester_name=requester_name)


# Utility function to get the json response
def get_response_json(get_url):
    response = session.get(get_url)
    return response.json()


# Utility function to get the email and phone number of the requester
def get_requester_data(req_id):
    requester_data = session.get(f"{base_url}/users/{req_id}").json()
    requester_name = requester_data['user']['name']

    return requester_name


def get_requester_names(data):
    names = {}
    for row in data:
        names[row['requester_id']] = get_requester_data(row['requester_id'])
    return names
