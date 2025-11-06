import requests
import os
from dotenv import load_dotenv
import pandas as pd
from flask import Flask, render_template_string

load_dotenv()

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

app = Flask(__name__)

def get_access_token():
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        }
    )
    if response.status_code != 200:
        return None
    return response.json()['access_token']

def get_activities(access_token, limit=10):
    response = requests.get(
        'https://www.strava.com/api/v3/athlete/activities',
        headers={'Authorization': f'Bearer {access_token}'},
        params={'per_page': limit, 'page': 1}
    )

    if response.status_code != 200:
        return []

    return response.json()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Strava Activities</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #fc4c02;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #fc4c02;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .error {
            color: red;
            padding: 20px;
            background-color: #ffe6e6;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>🚴 Strava Activities</h1>
    {% if error %}
        <div class="error">{{ error }}</div>
    {% else %}
        <p>Showing {{ activities|length }} activities</p>
        {{ table|safe }}
    {% endif %}
</body>
</html>
'''

@app.route('/')
def index():
    access_token = get_access_token()
    if not access_token:
        return render_template_string(HTML_TEMPLATE, error="Failed to get access token", activities=[], table="")

    activities = get_activities(access_token, limit=30)
    if not activities:
        return render_template_string(HTML_TEMPLATE, error="No activities found", activities=[], table="")

    df = pd.DataFrame(activities)
    table_html = df.to_html(classes='table', index=False)

    return render_template_string(HTML_TEMPLATE, error=None, activities=activities, table=table_html)

if __name__ == "__main__":
    app.run(debug=True, port=5000)