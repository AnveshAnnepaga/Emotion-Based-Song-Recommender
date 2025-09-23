import os
import requests
from dotenv import load_dotenv

load_dotenv()
CLERK_SECRET_KEY = os.environ.get("CLERK_SECRET_KEY")

def create_user(email, password):
    """
    Creates a new user via Clerk's Backend API.
    Returns the new user's ID on success, or None on failure.
    """
    if not CLERK_SECRET_KEY:
        print("Error: CLERK_SECRET_KEY not found in .env file.")
        return None

    api_url = "https://api.clerk.com/v1/users"
    headers = {
        "Authorization": f"Bearer {CLERK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "email_address": [email],
        "password": password
    }

    try:
        response = requests.post(api_url, headers=headers, json=data)
        response.raise_for_status()
        
        user_data = response.json()
        return user_data['id']
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during user creation: {e}")
        return None

def find_user_by_email(email):
    """
    Finds an existing user by email to get their ID for login.
    Note: A more robust login system would create a session token.
    """
    if not CLERK_SECRET_KEY:
        return None
    
    api_url = f"https://api.clerk.com/v1/users?email_address={email}"
    headers = {
        "Authorization": f"Bearer {CLERK_SECRET_KEY}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        
        users_list = response.json()
        if users_list and users_list[0]['email_addresses'][0]['email_address'] == email:
            return users_list[0]['id']
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error finding user: {e}")
        return None