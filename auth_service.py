# auth_service.py
import os
import bcrypt
import streamlit as st 
from supabase_client import supabase
from postgrest.exceptions import APIError

def create_user(name, age, email, password):
    """
    Creates a new user, securely hashing the password before storing it.
    Returns the new user's integer ID and name on success.
    """
    try:
        # 1. Check if user already exists
        response = supabase.table('users').select('id').eq('email', email).limit(1).execute()
        if response.data:
            st.error("Sign-up Error: A user with this email already exists.")
            return None, None
        
        # 2. Hash the password securely with bcrypt
        hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password_hash = hashed_bytes.decode('utf-8')

        # 3. Insert user into Supabase
        data = {
            "name": name,
            "age": age,
            "email": email,
            "username": email.split('@')[0],
            "password_hash": password_hash
        }
        user_data = supabase.table('users').insert(data).execute().data[0]
        return user_data['id'], user_data['name'] # Return both ID and Name
    except APIError:
        st.error(f"Sign-up Error: API failed to create user.")
        return None, None
    except Exception as e:
        st.error(f"Sign-up Error: An unexpected error occurred. {e}")
        return None, None

def sign_in_user(email, password):
    """
    Signs in a user by securely verifying the password hash against Supabase.
    Returns the user's integer ID and Name on successful login.
    """
    try:
        # 1. Retrieve the stored hash, ID, and NAME
        response = supabase.table('users').select('id, name, password_hash').eq('email', email).limit(1).execute()
        
        if not response.data:
            return None, None # User not found
            
        user = response.data[0]
        stored_hash = user['password_hash'].encode('utf-8')
        
        # 2. Verify the password using bcrypt.checkpw
        if bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            return user['id'], user['name'] # Login successful, return ID and Name
        else:
            # Note: Do not reveal whether it's the email or password that is wrong
            st.error("Login failed. Invalid email or password.")
            return None, None 
            
    except APIError:
        st.error(f"Login Error: API failed to retrieve user.")
        return None, None
    except Exception as e:
        st.error(f"Login Error: An unexpected error occurred. {e}")
        return None, None