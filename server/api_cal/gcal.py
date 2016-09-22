from dbase.dataset import Dataset

from oauth2client import client
from apiclient.discovery import build
from oauth2client.file import Storage

import socket as sct

import sys, os

from flask import abort
import httplib2

import datetime

class Gcal(Dataset):

    #Inits Calendar tables
    def create_tables(self):
        """ Initializes SQLITE3 storage for google calendars """

        # Creates primary google calendar storage table
        self._db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_gcal (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                gid TEXT NOT NULL,
                backgroundColor TEXT,
                summary TEXT,
                description TEXT,
                active INT NOT NULL DEFAULT 1
            )
        """)


    def get_flow(self):
        """ Returns google authentication flow for following services, from client_sercet.json file """

        flow = client.flow_from_clientsecrets(
            os.path.join(self._appdir, 'client_secret.json' ),
            scope=["https://www.googleapis.com/auth/calendar.readonly","https://www.googleapis.com/auth/userinfo.profile"],
            # redirect_uri="http://%s:5000/gcal/auth2callback" % (sct.gethostbyname(sct.gethostname()))
            # redirect_uri="http://%s:5000/gcal/auth2callback" % (sct.gethostbyname(sct.gethostname()))
            redirect_uri="http://localhost:5000/gcal/auth2callback"
        )
        flow.params['include_granted_scopes'] = "true"
        flow.params['access_type'] = 'offline'

        return flow

    # Get credential
    def get_cred(self):
        """ Reads current user credentials from saved file """

        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            return store.locked_get()
        except:
            self._log.exception("Failed to get google authentication credential")
            return None


    # Put credential
    def put_cred(self, cred):
        """ Saves current user credentials into file """

        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            store.locked_put(cred)
        except:
            self._log.exception("Failed to get google authentication credential")
            return None


    # Remove credential
    def rmv_cred(self):
        """ Removes current user credentials file """

        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            store.locked_delete()
        except:
            self._log.exception("Failed to remove google authentication credential")
            return None


    def get_auth(self):
        """ Attaches google authentication to current http request """
        try:
            return self.get_cred().authorize(httplib2.Http())
        except:
            self._log.exception("Failed to authenticate with google")


    # Checks for need of authentication
    def need_auth(self):
        """ Check for need of authentication """

        return not isinstance( self.get_auth(), httplib2.Http )


    # De-authenticate user
    def deauth_usr(self):
        """ Function for signing user out """

        self._log.debug("Removing google account authentication")

        self.get_cred().revoke(httplib2.Http())
        self.rmv_cred()

        return "/"


    # Get Google Auth redirect URL
    def get_auth_uri(self):
        """ Returns google authentication page URI """

        flow = self.get_flow()
        auth_uri = flow.step1_get_authorize_url()
        return auth_uri


    # Google Auth Redirect callback
    def auth_callback(self, key):
        """ Saves returned google authentication key for future use """

        assert isinstance(key, unicode)

        flow = self.get_flow()

        # Get and store credential file
        credential = flow.step2_exchange(key)
        self.put_cred(credential)

        # Return Index redirection
        return "/"


    def get_disp_name(self):
        """ Gets full name of current logged in user """
        try:
            http = self.get_auth()
            info = build('plus','v1', http=http)

            results = info.people().get(userId='me').execute()
            return results.get('displayName')
        except:
            self._log.exception("Failed to get user display name")


    # Return list calendarList
    def get_cals(self):
        """ Gets a list of all possible calendars, and saves them to a database """

        http = self.get_auth()
        cal = build('calendar', 'v3', http=http)

        c_list = cal.calendarList().list().execute()['items']

        db_list = []
        for i in c_list:
            db_list.append((i.get('id'),
                            i.get('backgroundColor'),
                            i.get('summary'),
                            i.get('description'),
                            i.get('id')))

        self._db.qry_many("""
            INSERT INTO tbl_gcal (gid, backgroundColor, summary, description)
            SELECT ?,?,?,?
            WHERE NOT EXISTS(SELECT gid FROM tbl_gcal WHERE gid=?)
        """, db_list)

        return self._db.qry("SELECT * FROM tbl_gcal")

    # Toggle calendars as active
    def add_cals(self, ids):
        """ Updates witch calendars to show on mirror interface """

        self._log.debug(ids)

        self._db.qry("UPDATE tbl_gcal SET active=0");
        self._db.qry_many("UPDATE tbl_gcal SET active=1 WHERE id=?", ids)

        self._log.debug(self._db.qry("SELECT * FROM tbl_gcal"))

        return 200

    # Returns all possible user calendars ids
    def get_ucals(self):
        return self._db.qry("SELECT gid FROM tbl_gcal WHERE active=1")

    # Returns todays events
    def get_today(self):
        http = self.get_auth()
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

        plans = []
        for cl in self.get_ucals():
            results = cal.events().list(
                calendarId=cl['gid'],

                timeMin=t_now.isoformat()+"Z",
                timeMax=t_max.isoformat()+"Z",

                showDeleted=False,
                singleEvents=True,

                maxResults=15,

                orderBy='startTime'
            ).execute()
            events = results.get('items',[])

            for e in events:
                plans.append(e)

        return plans
