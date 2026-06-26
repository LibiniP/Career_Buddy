"""
Input validation functions: 
Validate the 'username' input to ensure it meets basic criteria:
- Must not be empty or None
- Must have at least 3 characters
- Must only contain alphanumeric characters and underscores
Returns:
 (bool, str): Tuple where first element is validity (True/False),
 second element is an error message if invalid or empty string if valid.
 """

def validate_username(username):
    """Validate username"""
    # Check if username is empty or too short
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    # Check if username consists only of letters, digits, or underscores
    # Note: replace underscores with empty string before isalnum check
    if not username.replace('_', '').isalnum():
        return False, "Username must be alphanumeric"
    # If both checks pass, username is valid
    return True, ""


def validate_password(password):
    """
    Validate the 'password' input based on length requirement:
    - Must not be empty or None
    - Must have at least 6 characters
    Returns:
        (bool, str): Tuple where first element indicates validity,
                     second element provides an error message or empty string.
    """
    # Check if password is empty or less than 6 characters
    if not password or len(password) < 6:
        return False, "Password must be at least 6 characters"
    # Password is valid if above check passes
    return True, ""


def validate_profile(profile):
    """
    Validate profile information dictionary.
    Checks for presence and acceptable values in key fields:
    - 'education' must exist and be non-empty
    - 'interests' must exist and have at least one entry
    - 'work_preference' must exist and be non-empty
    - 'time_availability' must exist and be at least 1 hour (numeric)
    Args:
        profile (dict): Dictionary containing profile fields.
    Returns:
        (bool, str): Tuple where first element indicates if all required fields
                     are valid and second element is error message or empty string.
    """
    # Check if 'education' field exists and is non-empty
    if not profile.get('education'):
        return False, "Education level is required"
    # Check if 'interests' field exists and contains at least one item
    if not profile.get('interests'):
        return False, "At least one interest is required"
    # Check if 'work_preference' field exists and is non-empty
    if not profile.get('work_preference'):
        return False, "Work preference is required"
    # Check if 'time_availability' exists and is >= 1 (hour)
    # Supports the case where time_availability may be zero or None
    if not profile.get('time_availability') or profile['time_availability'] < 1:
        return False, "Time availability must be at least 1 hour"
     # If all checks pass, profile data is valid
    return True, ""