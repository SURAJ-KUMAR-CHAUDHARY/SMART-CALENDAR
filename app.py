from flask import Flask, render_template
from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

app = Flask(__name__)

# Google credentials setup
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

calendar_service = build('calendar', 'v3', credentials=credentials)

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/create_event')
def create_event():
    now = datetime.datetime.utcnow()
    event = {
        'summary': 'Hackathon Demo Event',
        'location': 'Online',
        'description': 'This event was created by a button click!',
        'start': {
            'dateTime': (now + datetime.timedelta(hours=1)).isoformat() + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': (now + datetime.timedelta(hours=2)).isoformat() + 'Z',
            'timeZone': 'UTC',
        },
    }

    created_event = calendar_service.events().insert(calendarId='primary', body=event).execute()
    return f"✅ Event created! <a href='{created_event.get('htmlLink')}' target='_blank'>View Event</a>"

if __name__ == '__main__':
    app.run(debug=True)