import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "openid",
    "https://www.googleapis.com/auth/contacts.readonly",
    "https://www.googleapis.com/auth/user.birthday.read",
    "https://www.googleapis.com/auth/userinfo.profile",
    "https://www.googleapis.com/auth/user.emails.read",
]


def main():
    """Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        people_service = build("people", "v1", credentials=creds)

        # Call the People API
        profile = people_service.people().get(resourceName="people/me", personFields="names,emailAddresses,birthdays").execute()
        print(profile)

        print(f"\n\n{profile['emailAddresses'][0]['value']}")
        # print("List 10 connection names")
        # results = (
        #     people_service.people()
        #     .connections()
        #     .list(
        #         resourceName="people/me",
        #         pageSize=10,
        #         personFields="names,emailAddresses",
        #     )
        #     .execute()
        # )
        # connections = results.get("connections", [])

        # for person in connections:
        #     names = person.get("names", [])
        #     if names:
        #         name = names[0].get("displayName")
        #         print(name)
    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
