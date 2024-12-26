import os

from dotenv import load_dotenv
from fastapi import FastAPI
import requests
import webbrowser
from starlette.responses import RedirectResponse

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
REDIRECT_URI = "http://localhost:8080/callback"
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# Generate the authorization URL
auth_url = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read:user"

app = FastAPI()

def get_access_token(code):
   # Token endpoint
    token_url = "https://github.com/login/oauth/access_token"

    # Request payload
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": code,
        "redirect_uri": REDIRECT_URI,
    }

    # Set headers to request JSON response
    headers = {"Accept": "application/json"}

    response = requests.post(
        token_url, json=payload, headers=headers
    )
    if response.status_code == 200:
        access_token = response.json()["access_token"]
        return access_token
    return None

def get_user_data(access_token):
    # GitHub API URL
    api_url = "https://api.github.com/user"

    # Set headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/vnd.github+json",
    }

    # Make the GET request
    response = requests.get(api_url, headers=headers)
    user_data = response.json()
    print(user_data)

    if response.status_code == 200:
        return user_data
    return None

@app.get('/')
def authenticate():
    webbrowser.open(auth_url)
    return f"Open this URL in your browser to authorize: {auth_url}"

@app.get('/callback')
def code_handle(code:str):
    access_token = get_access_token(code)
    user_data = get_user_data(access_token)
    print(user_data)
    return RedirectResponse("authenticated/")

@app.get('/authenticated/')
def authenticated():
    return "User successfully authenticated"

    
