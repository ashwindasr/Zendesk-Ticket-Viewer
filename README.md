# Zendesk-Ticket-Viewer

![GitHub](https://img.shields.io/badge/Language-Python-blue.svg)

Built using `Python 3.9` and `Flask`.

The project conforms to the [PEP](https://www.python.org/dev/peps/pep-0008/) style guidelines for Python code.

## :rocket: Setup
Install `Python 3.9` from the website [here](https://www.python.org/downloads/).

The `requirements.txt` file includes all the necessary dependencies which can be run with the command.
```
pip install -r requirements.txt
```
Also make sure to store the auth creadentials in local environment variables `EMAIL`, `PASSWORD` and `SERVER`.
## :compass: Navigation

### routes.py
Contains the routes to the endpoints and their appropriate handlers. The account credentials have been stored in the local environment variables and accessed using the `os.environ` commands.

### templates
The `templates` directory contains the html files rendred by the app. The `index.html` displays the main page, `show.html` shows the details of a particular ticket and `error.html` displays an error page if the Zendesk API is unavailable. The appropriate route handlers have been defined in `routes.py` file.

### tests
The `tests` directory contains the unittests for checking the flask app endpoints and whether the Zendesk API is working or not.

## :mag_right: Screenshots
![alt text](https://github.com/ashwindasr/Zendesk-Ticket-Viewer/blob/master/assets/images/2.png)
![alt text](https://github.com/ashwindasr/Zendesk-Ticket-Viewer/blob/master/assets/images/1.png)

