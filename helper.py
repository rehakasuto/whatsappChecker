import json
import os
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime


class Helper:
    def __init__(self):
        with open('configuration.json', 'r') as file:
            self.config = json.load(file)

    def get_firefox_binary_path(self):
        """Reads the Firefox Binary Path from the configuration.json file."""
        try:
            return self.config.get('firefoxBinaryPath', "")
        except FileNotFoundError:
            print("configuration.json file not found.")
            return ""

    def get_db_url(self):
        """Reads the database URL from the configuration.json file."""
        try:
            return self.config.get('dbUrl', "")
        except FileNotFoundError:
            print("configuration.json file not found.")
            return ""

    def firebase_auth(self):
        """Initializes Firebase authentication using the FirebaseAdminSDK.json file."""
        try:
            cred = credentials.Certificate('FirebaseAdminSDK.json')
            firebase_admin.initialize_app(cred, {
                'databaseURL': self.get_db_url()
            })
        except FileNotFoundError:
            print('Unable to find FirebaseAdminSDK.json file in ' + os.getcwd())
            exit(1)

    @staticmethod
    def write_log(dt: datetime, all_messages: str, last_message: str, receiver: str):
        """Writes a log entry to Firebase database."""
        date_format = dt.strftime("%x")
        time_format = dt.strftime("%X")
        ref = db.reference('/Logs')
        ref.push({
            'DateTime': date_format + " " + time_format,
            'AllMessages': all_messages,
            'LastMessage': last_message,
            'Receiver': receiver
        })

    @staticmethod
    def read_last_message():
        """Reads the last log entry from Firebase database."""
        ref = db.reference('/Logs')
        logs = ref.get()
        last_log = ""
        if logs:
            last_log_key = sorted(logs.keys())[-1]
            last_log = logs[last_log_key]['LastMessage']
        return last_log

    @staticmethod
    def get_all_messages():
        ref = db.reference('/Logs')
        logs = ref.get()

        messages = []
        if logs:
            for log_id in logs:
                log = logs[log_id]
                messages.append({
                    'id': log_id,
                    'DateTime': log.get('DateTime'),
                    'Receiver': log.get('Receiver'),
                    'LastMessage': log.get('LastMessage'),
                    'AllMessages': log.get('AllMessages')
                })
        return messages

    @staticmethod
    def check_text_in_blacklist(text: str):
        """Checks if the provided text contains any word from the blacklist."""
        try:
            with open("blacklist.txt", 'r') as file:
                blacklist = [line.strip() for line in file]
        except FileNotFoundError:
            print("blacklist.txt file not found.")
            return False

        words = text.lower().split()
        return any(word in blacklist for word in words)