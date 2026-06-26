"""
Authentication UI Components
Handles login and signup functionality
"""

import ipywidgets as widgets
from IPython.display import display, clear_output
from utils.helpers import create_header
from utils.validators import validate_username, validate_password
from datetime import datetime
import json
import os

# JSON file where user accounts are stored.
USERS_FILE = 'careerbuddy_users.json'

# Saves the user database to file.
def save_users_db(users_db):
    """Save users to file"""
    save_data = {}
    for username, data in users_db.items():
        save_data[username] = {  # Converts datetime to string for JSON compatibility.
            'password': data['password'],
            'created': data['created'].isoformat() if isinstance(data['created'], datetime) else data['created']
        }
    with open(USERS_FILE, 'w') as f:
        json.dump(save_data, f) # Writes user database to storage.


def show_login_page(model, users_db, output_area):
    """
    Display login/signup page
    
    Args:
        model: CareerBuddyModel instance
        users_db: User database dictionary
        output_area: Output widget for dynamic content
    """
    # Don't show header here - it's shown by start_application()
    
    # Login form widgets
    username_login = widgets.Text(
        placeholder='Enter username',
        description='Username:',
        style={'description_width': '100px'}
    )
    password_login = widgets.Password(
        placeholder='Enter password',
        description='Password:',
        style={'description_width': '100px'}
    )
    login_btn = widgets.Button(
        description='Login',
        button_style='primary',
        icon='sign-in'
    )
    
    # Signup form widgets
    username_signup = widgets.Text(
        placeholder='Choose username (min 3 chars)',
        description='Username:',
        style={'description_width': '100px'}
    )
    password_signup = widgets.Password(
        placeholder='Choose password (min 6 chars)',
        description='Password:',
        style={'description_width': '100px'}
    )
    confirm_password = widgets.Password(
        placeholder='Confirm password',
        description='Confirm:',
        style={'description_width': '100px'}
    )
    signup_btn = widgets.Button(
        description='Sign Up',
        button_style='success',
        icon='user-plus'
    )
    
    message_area = widgets.Output()
    
    def on_login_click(b):
        """Handle login button click"""
        with message_area:
            clear_output()
            
            username = username_login.value.strip()
            password = password_login.value
            
            # Validate
            if not username:
                print("❌ Please enter a username!")
                return
                
            valid, msg = validate_username(username)
            if not valid:
                print(f"❌ {msg}")
                return
            
            # Check credentials
            if username in users_db:
                if users_db[username]['password'] == password:
                    print(f"✅ Welcome back, {username}!")
                    
                    import time
                    time.sleep(0.5)
                    
                    # Navigate to profile setup or dashboard
                    agent = model.get_agent(username)
                    with output_area:
                        clear_output(wait=True)
                        if agent:
                            from ui.dashboard import show_dashboard
                            show_dashboard(model, username, output_area)
                        else:
                            from ui.profile_setup import show_profile_setup
                            show_profile_setup(model, username, users_db, output_area)
                else:
                    print("❌ Invalid password!")
            else:
                print("❌ User not found! Please sign up first.")
    
    def on_signup_click(b):
        """Handle signup button click"""
        with message_area:
            clear_output()
            
            username = username_signup.value.strip()
            password = password_signup.value
            confirm = confirm_password.value
            
            # Validate username
            if not username:
                print("❌ Please enter a username!")
                return
                
            valid, msg = validate_username(username)
            if not valid:
                print(f"❌ {msg}")
                return
            
            # Validate password
            if not password:
                print("❌ Please enter a password!")
                return
                
            valid, msg = validate_password(password)
            if not valid:
                print(f"❌ {msg}")
                return
            
            # Check password match
            if password != confirm:
                print("❌ Passwords do not match!")
                return
            
            # Check if username exists
            if username in users_db:
                print("❌ Username already exists!")
                return
            
            # Create account
            users_db[username] = {
                'password': password,
                'created': datetime.now()
            }
            save_users_db(users_db)
            
            print(f"✅ Account created! Welcome, {username}!")
            
            import time
            time.sleep(0.5)
            
            # Navigate to profile setup
            with output_area:
                clear_output(wait=True)
                from ui.profile_setup import show_profile_setup
                show_profile_setup(model, username, users_db, output_area)
    
    # Attach event handlers
    login_btn.on_click(on_login_click)
    signup_btn.on_click(on_signup_click)
    
    # Create tabs for login/signup
    # VBox = It arranges widgets vertically, one below another, like a column layout.
    # widgets.Tab creates a tabbed interface similar to browser tabs.
    tab = widgets.Tab()
    tab.children = [
        widgets.VBox([username_login, password_login, login_btn]),
        widgets.VBox([username_signup, password_signup, confirm_password, signup_btn])
    ]
    tab.set_title(0, 'Login')
    tab.set_title(1, 'Sign Up')
    
    display(tab)
    display(message_area)