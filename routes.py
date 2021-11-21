"""routes.py"""

import os

import requests
from flask import render_template, redirect

from app import app

# Getting the email and password for zendesk from environment variables
CREDENTIALS = os.environ['EMAIL'], os.environ['PASSWORD']
session = requests.Session()  # Creating a new session
session.auth = CREDENTIALS
SERVER = os.environ['MY_SERVER']  # Getting the server name from environment variable
ZENDESK = f'https://{SERVER}.zendesk.com'
base_url = f'{ZENDESK}/api/v2'
url = f'{ZENDESK}/api/v2/tickets.json?page[size]=25'  # Global url variable used for requests


@app.route('/')
def index():
    """
    Index function. Currently no functionality implemented.

    :return: Redirect to /posts
    """
    return redirect("/posts")


@app.route('/posts')
def posts_index():
    """
    Function which handles the request to the posts page.

    :return: error.html page if zendesk API error else the posts.html page
    """

    # Try except block to check whether zendesk API is available
    # If not, an error page is displayed
    try:
        _ = check_api_status()
    except:
        return render_template("error.html")

    posts = get_response_json(url)

    prev_link = posts['links']['prev']  # URL to the previous set of tickets
    next_link = posts['links']['next']  # URL to the next set of tickets

    # Checking to see if the 'prev' link has any tickets or if its empty
    prev_flag = True if \
        session.get(prev_link).json()['tickets'] != [] else False
    # Checking to see if the 'next' link has any tickets or if its empty
    next_flag = True if \
        session.get(next_link).json()['tickets'] != [] else False

    total_posts_count = session.get(f"{base_url}/tickets/count").json()['count']['value']
    current_page_count = len(posts['tickets'])
    requester_names = get_requester_names(posts['tickets'])

    context = {
        'posts': posts['tickets'],
        'prev_flag': prev_flag,
        'next_flag': next_flag,
        'total_posts_count': total_posts_count,
        'current_page_count': current_page_count,
    }

    return render_template("posts.html", context=context, requester_names=requester_names)


@app.route('/posts/next')
def posts_next():
    """
    Function that handles the request when the 'next' link is clicked.
    The link inside the 'next' field is set to the url variable and the control is redirected to the /posts handler.

    :return: redirect to the /posts handler
    """

    # Try except block to check whether zendesk API is available
    # If not, an error page is displayed
    try:
        _ = check_api_status()
    except:
        return render_template("error.html")

    global url
    url = get_response_json(url)['links']['next']

    return redirect("/posts")


@app.route('/posts/back')
def posts_back():
    """
    Function that handles the request when the 'back' link is clicked.
    The link inside the 'prev' field is set to the url variable and the control is redirected to the /posts handler.

    :return: redirect to the /posts handler
    """

    # Try except block to check whether zendesk API is available
    # If not, an error page is displayed
    try:
        _ = check_api_status()
    except:
        return render_template("error.html")

    global url
    url = get_response_json(url)['links']['prev']
    return redirect("/posts")


@app.route('/posts/show/<int:post_id>')
def show_post(post_id):
    """
    Shows the details of a ticket with the

    :param post_id: Ticket id
    :return: show.html page
    """
    # Try except block to check whether zendesk API is available
    # If not, an error page is displayed
    try:
        _ = check_api_status()
    except:
        return render_template("error.html")

    show_url = base_url + f"/tickets/{post_id}"
    post = get_response_json(show_url)

    requester_id = post['ticket']['requester_id']
    requester_name = get_requester_data(requester_id)

    return render_template("show.html", post=post['ticket'], post_id=post_id, requester_name=requester_name)


def get_response_json(request_url):
    """
    Utility function that returns the json response to the request.

    :param request_url: The request url
    :return: JSON reponse
    """
    response = session.get(request_url)
    return response.json()


def get_requester_data(req_id):
    """
    Utility function to return the name of the requester with a particular requester ID.
    Function can be extended to get other fields other fields of the requester as well like name, etc.

    :param req_id: ID of requester
    :return: Name of requester
    """
    requester_data = session.get(f"{base_url}/users/{req_id}").json()
    requester_name = requester_data['user']['name']

    return requester_name


def get_requester_names(data):
    """
    Function to map the requester IDs with the corresponding names to be used in the posts.html page.

    :param data: Tickets data
    :return: Python dict with name
    """
    names = {}
    for row in data:
        # Only need to add value to dict if it is not present already.
        try:
            _ = names[row['requester_id']]
        except:
            names[row['requester_id']] = get_requester_data(row['requester_id'])
    return names


def check_api_status():
    """
    Function to check if the zendesk API is available or not.
    URL can be changed to a more appropriate on if required.

    :return: Status code (can be used if needed)
    """
    response = session.get(f"{base_url}/users")
    return response.status_code
