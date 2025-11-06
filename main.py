import requests
import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REFRESH_TOKEN = os.getenv('STRAVA_REFRESH_TOKEN')

def get_access_token():
    print("Getting access token...")
    response = requests.post(
        'https://www.strava.com/oauth/token',
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        }
    )
    print(f"Response status: {response.status_code}")
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return None
    return response.json()['access_token']

def get_activities(access_token, limit=10):
    print(f"Fetching up to {limit} activities...")
    response = requests.get(
        'https://www.strava.com/api/v3/athlete/activities',
        headers={'Authorization': f'Bearer {access_token}'},
        params={'per_page': limit, 'page': 1}
    )
    
    print(f"Rate limit: {response.headers.get('X-RateLimit-Limit')}")
    print(f"Remaining: {response.headers.get('X-RateLimit-Usage')}")
    
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return []
        
    return response.json()

def main():
    access_token = get_access_token()
    if not access_token:
        return
        
    activities = get_activities(access_token, limit=10)
    print(f"\nDownloaded {len(activities)} activities")
    
    for activity in activities:
        print(f"{activity['name']} - {activity['type']} - {activity['distance']}m")

if __name__ == "__main__":
    main()