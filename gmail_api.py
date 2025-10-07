"""
gmail_api.py
------------------
Handles Gmail authentication for the Email Cleaner project.

Learning how to connect a Python script to Gmail using Google's API and OAuth2. Scope is
read-only for now to safely fetch and test data without modifying my current inbox.
"""

# --- Imports ---
# Libraries provided by Google for connecting securely to Gmail.
# Handle authentication, and allow service to make API requests.
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# --- OAuth Scope ---
# Defines the level of access the app has to Gmail.
# Read-only scope to fetch emails without modifying them.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_service():
    """
    Creates and returns an authenticated Gmail service object that can be used to make
    API calls.
    """
    creds = None

    # 1) Try to load existing credentials if it exists.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # 2) If credentials are unavailable / invalid, create new credentials.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # If the token is expired, refresh it.
            creds.refresh(Request())
        else:
            # No valid credentials available, begin OAuth flow to obtain credentials.
            # Currently uses credentials.json from Google Cloud Console.
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # 3) Save new credentials for next run.
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # 4) Build and return the Gmail API client.
    return build("gmail", "v1", credentials=creds)


# --- Main ---
# If this script is run directly, test the Gmail service by fetching the user's profile.
if __name__ == "__main__":

    # Signal module is loaded correctly.
    print("gmail_api module loaded")

    # Get the authenticated Gmail service.
    service = get_service()

    # Fetch and print the user's email address to verify authentication.
    me = service.users().getProfile(userId="me").execute()
    print(f"Logged in as: {me['emailAddress']}")
