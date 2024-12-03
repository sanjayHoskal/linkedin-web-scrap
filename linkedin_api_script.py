import requests
import pandas as pd
from config import CLIENT_ID, CLIENT_SECRET, ACCESS_TOKEN

def get_access_token(client_id, client_secret):
    token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(token_url, headers=headers, data=data)

    if response.status_code == 200:
        return response.json()['access_token']
    else:
        print(f"Failed to get access token: {response.status_code}")
        return None

def fetch_linkedin_data(access_token, first_name, last_name):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    query = f"{first_name} {last_name}"
    url = f"https://api.linkedin.com/v2/search?q=people&query={query}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data['elements'][:5]  # First 5 relevant results
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return []

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    first_name = 'Sanjay'
    last_name = 'P'
    
    if ACCESS_TOKEN is None:
        access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    else:
        access_token = ACCESS_TOKEN
    
    linkedin_data = fetch_linkedin_data(access_token, first_name, last_name)
    save_to_csv(linkedin_data, 'linkedin_data.csv')
