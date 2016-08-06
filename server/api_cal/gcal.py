from oauth2client import client
from apiclient.discovery import build
from oauth2client.file import Storage

from minfo import app_dir

import sys

from flask import abort, redirect
import httplib2

import datetime
from dbase.dbase import dbase as db

class gcal:
    #Inits Calendar tables
    @staticmethod
    def init_cal_tbl():
        db.qry("""
            CREATE TABLE IF NOT EXISTS tbl_gcal (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                gid TEXT NOT NULL,
                backgroundColor TEXT,
                summary TEXT,
                description TEXT,
                active INT NOT NULL DEFAULT 1
            )
        """)

    @staticmethod
    def if_cal_tbl():
         return db.qry("SELECT name FROM sqlite_master WHERE type='table' AND name='tbl_gcal'")

    # Get auth flow
    @staticmethod
    def get_flow():
        gcal.init_cal_tbl()

        flow = client.flow_from_clientsecrets(
            app_dir+"/client_secret.json",
            scope=["https://www.googleapis.com/auth/calendar.readonly","https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/gmail.readonly"],
            redirect_uri="http://localhost:5000/gcal/auth2callback"
        )
        flow.params['access_type'] = 'offline'
        return flow

    # Get credential
    @staticmethod
    def get_cred():
        try:
            store = Storage(app_dir+'/gcal_credentials')
            return store.locked_get()
        except:
            print "ERROR!", sys.exc_info()[0]
            return None

    # Put credential
    @staticmethod
    def put_cred(cred):
        # try:
        store = Storage(app_dir+'/gcal_credentials')
        store.locked_put(cred)
        # except:
        #     return None

    # Remove credential
    @staticmethod
    def rmv_cred():
        try:
            store = Storage(app_dir+'/gcal_credentials')
            store.locked_delete()
        except:
            print "ERROR!", sys.exc_info()[0]
            return None

    # Checks for need of authentication
    @staticmethod
    def need_auth():
        if gcal.get_cred() == None:
            return True

        if gcal.get_disp_name() == False:
            return True

        return False

    # De authenticate user
    @staticmethod
    def deauth_usr():
        print "removing auth"

        if gcal.get_cred() != None:
            gcal.get_cred().revoke(httplib2.Http())
            gcal.rmv_cred()

        return "/"

    # Get Google Auth redirect URL
    @staticmethod
    def get_auth_uri():
        # if gcal.need_auth():
        flow = gcal.get_flow()
        auth_uri = flow.step1_get_authorize_url()
        return auth_uri
        # else:
        #     return "/"

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

    @staticmethod
    def get_disp_name():
        # if not gcal.need_auth():
        try:
            http = gcal.get_cred().authorize(httplib2.Http())
            info = build('plus','v1', http=http)

            results = info.people().get(userId='me').execute()
            return results.get('displayName')
        except:
            return False
            # print "ERROR!", sys.exc_info()[0]

    @staticmethod
    def get_mail():
        http = gcal.get_cred().authorize(httplib2.Http())
        mail = build('gmail', 'v1', http=http)

        results = mail.users().labels().list(userId='me').execute()

        return results.get('labels', [])

    # Return list calendarList
    @staticmethod
    def get_cals():
        gcal.init_cal_tbl()

        http = gcal.get_cred().authorize(httplib2.Http())
        cal = build('calendar', 'v3', http=http)

        c_list = cal.calendarList().list().execute()['items']
        db_list = []

        for i in c_list:
            db_list.append((i.get('id'),
                            i.get('backgroundColor'),
                            i.get('summary'),
                            i.get('description'),
                            i.get('id')))

        db.qry_many("""
            INSERT INTO tbl_gcal (gid, backgroundColor, summary, description)
            SELECT ?,?,?,?
            WHERE NOT EXISTS(SELECT gid FROM tbl_gcal WHERE gid=?)
        """, db_list)

        return db.qry("SELECT * FROM tbl_gcal")
        # return ''

    #Add list of calendars
    @staticmethod
    def add_cals(ids):
        # print ids
        # pass
        # gcal.init_cal_tbl()

        db.qry("UPDATE tbl_gcal SET active=0");
        db.qry_many("UPDATE tbl_gcal SET active=1 WHERE id=?", ids)

        return 200

        # print db.qry("SELECT * FROM tbl_gcal")

        # for id in ids:
        #     # print id
        #     db.qry("INSERT INTO tbl_gcal (gid) VALUES (?)", (id, ))

    #List user calendars
    @staticmethod
    def get_ucals():
        return db.qry("SELECT gid FROM tbl_gcal WHERE active=1")

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

        # print gcal.get_ucals()
        stuff = []
        for cl in gcal.get_ucals():
            results = cal.events().list(
                # calendarId='primary',
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
                stuff.append(e)

        return stuff
        # return events
