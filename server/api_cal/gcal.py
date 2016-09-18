from dbase.dataset import Dataset

from oauth2client import client
from apiclient.discovery import build
from oauth2client.file import Storage

# from minfo import app_dir

import sys, os

from flask import abort
import httplib2

import datetime
# from dbase.dbase import dbase as db

# import logging
# logger = logging.getLogger("TB")

class Gcal(Dataset):

    #Inits Calendar tables
    def create_tables(self):
        self._log.debug("Initializing google calendar tables")

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


    # Get auth flow
    def get_flow(self):
        flow = client.flow_from_clientsecrets(
            os.path.join(self._appdir, 'client_secret.json' ),
            scope=["https://www.googleapis.com/auth/calendar.readonly","https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri="http://localhost:5000/gcal/auth2callback"
        )
        flow.params['access_type'] = 'offline'

        return flow

    # Get credential
    def get_cred(self):
        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            return store.locked_get()
        except:
            self._log.exception("Failed to get google authentication credential")
            return None


    # Put credential
    def put_cred(self, cred):
        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            store.locked_put(cred)
        except:
            self._log.exception("Failed to get google authentication credential")
            return None


    # Remove credential
    def rmv_cred(self):
        try:
            store = Storage( os.path.join(self._appdir, 'gcal_credentials') )
            store.locked_delete()
        except:
            self._log.exception("Failed to remove google authentication credential")
            return None


    def get_auth(self):
        try:
            return self.get_cred().authorize(httplib2.Http())
        except:
            self._log.exception("Failed to authenticate with google")


    # Checks for need of authentication
    def need_auth(self):
        return not isinstance( self.get_auth(), httplib2.Http )

        # if self.get_cred() == None:
        #     return True
        #
        # if self.get_disp_name() == False:
        #     return True

        # return False

    # De-authenticate user
    def deauth_usr(self):
        self._log.debug("Removing google account authentication")

        self.get_cred().revoke(httplib2.Http())
        self.rmv_cred()

        return "/"


    # Get Google Auth redirect URL
    def get_auth_uri(self):
        flow = self.get_flow()
        auth_uri = flow.step1_get_authorize_url()
        return auth_uri


    # Google Auth Redirect callback
    def auth_callback(self, key):
        assert isinstance(key, unicode)

        flow = self.get_flow()

        # Get and store credential file
        credential = flow.step2_exchange(key)
        self.put_cred(credential)

        # Return Index redirection
        return "/"


    def get_disp_name(self):
        # self._log.debug(self.need_auth())
        # assert not self.need_auth() # Check if authentication with google is valid

        try:
            http = self.get_auth()
            info = build('plus','v1', http=http)

            results = info.people().get(userId='me').execute()
            return results.get('displayName')
        except:
            self._log.exception("Failed to get user display name")


    # Return list calendarList
    def get_cals(self):
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
        self._db.qry("UPDATE tbl_gcal SET active=0");
        self._db.qry_many("UPDATE tbl_gcal SET active=1 WHERE id=?", ids)

        return 200

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
