from oauth2client import client
from apiclient.discovery import build
from oauth2client.file import Storage

from flask import abort, redirect
import httplib2

import datetime

class gcal:
    # Get auth flow
    @staticmethod
    def get_flow():
        return client.flow_from_clientsecrets(
            "client_secret.json",
            scope="https://www.googleapis.com/auth/calendar.readonly",
            redirect_uri="http://localhost:5000/gcal/auth2callback"
        )

    # Get credential
    @staticmethod
    def get_cred():
        store = Storage('gcal_credentials')
        return store.get()

    # Put credential
    @staticmethod
    def put_cred(cred):
        store = Storage('gcal_credentials')
        store.put(cred)

    # Checks for need of authentication
    @staticmethod
    def need_auth():
        if gcal.get_cred() == None:
            return True
        else:
            return False

    # Get Google Auth redirect URL
    @staticmethod
    def get_auth_uri():
        if gcal.get_cred() == None:
            flow = gcal.get_flow()

            auth_uri = flow.step1_get_authorize_url()
            return auth_uri
        else:
            return "/"

    # Google Auth Redirect callback
    @staticmethod
    def auth_callback(key):
        if key == None:
            abort(400)
            return

        flow = gcal.get_flow()

        # Get and store credential file
        credential = flow.step2_exchange(key)
        gcal.put_cred(credential)

        # Return Index redirection
        return "/"

    # Returns todays events
    @staticmethod
    def get_today():
        http = gcal.get_cred().authorize(httplib2.Http())
        cal = build('calendar', 'v3', http=http)

        t_now = datetime.datetime.utcnow()
        t_max = datetime.datetime(
            year=t_now.year,
            month=t_now.month,
            day=t_now.day,
            hour=23,
            minute=59,
            second=59,
            microsecond=999999)

        results = cal.events().list(
            calendarId='primary',
            timeMin=t_now.isoformat()+"Z",
            timeMax=t_max.isoformat()+"Z",
            showDeleted=False,
            singleEvents=True,
            maxResults=15,
            orderBy='startTime'
        ).execute()

        events = results.get('items',[])
        return events
