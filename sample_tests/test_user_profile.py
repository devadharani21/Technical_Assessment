"""
Sample test file for user profile functionality.
Contains various quality issues and poor practices.
"""

import time
import os


# ISSUE: Global variable modification
CURRENT_USER = None


def test_update_user_profile():
    """Update user profile information."""
    # ISSUE: Function doesn't follow naming convention (no class)
    global CURRENT_USER
    
    # DUPLICATE CODE BLOCK 1 - File operations pattern
    # FLAKY: File operations without context manager
    file = open("user_data.json", "w")
    file.write('{"name": "John Doe", "email": "john@example.com"}')
    file.close()
    
    # DUPLICATE CODE BLOCK 1 - Validation pattern
    if not os.path.exists("user_data.json"):
        raise FileNotFoundError("User data file not found")
    with open("user_data.json", "r") as f:
        data = f.read()
        if not data:
            raise ValueError("User data is empty")
    
    time.sleep(2)
    
    # ISSUE: No assertions
    print("Profile updated")


def test_delete_user_account():
    """Delete user account - has resource issues."""
    global CURRENT_USER
    
    # DUPLICATE CODE BLOCK 1 - File operations pattern (duplicate of test_update_user_profile)
    # FLAKY: File operations without context manager
    file = open("user_data.json", "w")
    file.write('{"name": "John Doe", "email": "john@example.com"}')
    file.close()
    
    # DUPLICATE CODE BLOCK 1 - Validation pattern (duplicate of test_update_user_profile)
    if not os.path.exists("user_data.json"):
        raise FileNotFoundError("User data file not found")
    with open("user_data.json", "r") as f:
        data = f.read()
        if not data:
            raise ValueError("User data is empty")
    
    # FLAKY: File operations without proper error handling
    if os.path.exists("user_data.json"):
        os.remove("user_data.json")
    
    time.sleep(1)
    
    CURRENT_USER = None
    
    # ISSUE: No assertions


def test_upload_profile_picture():
    """Upload profile picture."""
    import requests
    
    # DUPLICATE CODE BLOCK 3 - File validation pattern
    if not os.path.exists("profile.jpg"):
        raise FileNotFoundError("Profile image file not found")
    file_size = os.path.getsize("profile.jpg")
    if file_size == 0:
        raise ValueError("Profile image is empty")
    if file_size > 5000000:
        raise ValueError("Profile image too large")
    
    # FLAKY: External network call
    with open("profile.jpg", "rb") as image_file:
        response = requests.post(
            "https://api.example.com/upload",
            files={"image": image_file}
        )
    
    # ISSUE: Broad exception handling
    try:
        assert response.status_code == 200
    except Exception:
        print("Upload failed")


def test_download_profile_picture():
    """Download profile picture."""
    import requests
    
    # DUPLICATE CODE BLOCK 3 - File validation pattern (duplicate of test_upload_profile_picture)
    if not os.path.exists("profile.jpg"):
        raise FileNotFoundError("Profile image file not found")
    file_size = os.path.getsize("profile.jpg")
    if file_size == 0:
        raise ValueError("Profile image is empty")
    if file_size > 5000000:
        raise ValueError("Profile image too large")
    
    # FLAKY: External network call
    response = requests.get("https://api.example.com/download/profile.jpg")
    
    # ISSUE: Broad exception handling
    try:
        assert response.status_code == 200
    except Exception:
        print("Download failed")


def test_user_profile_validation_with_multiple_edge_cases_and_boundary_conditions():
    """Test profile validation - ISSUE: Long function name and complexity."""
    # MAINTAINABILITY: Too complex, too many branches
    
    test_cases = [
        {"name": "", "email": "test@example.com", "age": 25},
        {"name": "John", "email": "", "age": 25},
        {"name": "John", "email": "invalid_email", "age": 25},
        {"name": "John", "email": "test@example.com", "age": -1},
        {"name": "John", "email": "test@example.com", "age": 0},
        {"name": "John", "email": "test@example.com", "age": 150},
        {"name": "A" * 100, "email": "test@example.com", "age": 25},
        {"name": "John", "email": "test@" + "a" * 100 + ".com", "age": 25},
    ]
    
    for test_case in test_cases:
        name = test_case["name"]
        email = test_case["email"]
        age = test_case["age"]
        
        # Validate name
        if not name:
            assert False, "Name cannot be empty"
        elif len(name) > 50:
            assert False, "Name too long"
        else:
            if not name.replace(" ", "").isalpha():
                assert False, "Name must contain only letters"
        
        # Validate email
        if not email:
            assert False, "Email cannot be empty"
        elif "@" not in email:
            assert False, "Invalid email format"
        else:
            if len(email) > 100:
                assert False, "Email too long"
            else:
                parts = email.split("@")
                if len(parts) != 2:
                    assert False, "Invalid email"
                else:
                    if not parts[0] or not parts[1]:
                        assert False, "Invalid email parts"
        
        # Validate age
        if age < 0:
            assert False, "Age cannot be negative"
        elif age == 0:
            assert False, "Age cannot be zero"
        elif age > 120:
            assert False, "Age unrealistic"
        else:
            if age < 18:
                print("Minor user")
            elif age >= 18 and age < 65:
                print("Adult user")
            else:
                print("Senior user")


class TestUserSettings:
    """Test user settings - has setup/teardown issues."""
    
    def setUp(self):
        """Setup method - ISSUE: No corresponding tearDown."""
        global CURRENT_USER
        CURRENT_USER = "testuser"
        
        # FLAKY: Database connection without proper cleanup
        import sqlite3
        self.db = sqlite3.connect("test.db")
        self.cursor = self.db.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT, value TEXT)")
        self.db.commit()
    
    # ISSUE: Missing tearDown method
    
    def test_update_notification_settings(self):
        """Update notification settings."""
        # DUPLICATE CODE BLOCK 2 - Database setup pattern
        time.sleep(1)
        
        self.cursor.execute("INSERT INTO settings VALUES ('notifications', 'enabled')")
        self.db.commit()
        
        time.sleep(1)
        
        # DUPLICATE CODE BLOCK 2 - Database verification pattern
        # ISSUE: Weak assertion
        result = self.cursor.execute("SELECT * FROM settings WHERE key='notifications'").fetchone()
        assert result is not None
        assert len(result) == 2
        assert result[0] == 'notifications'
    
    def test_update_privacy_settings(self):
        """Update privacy settings."""
        # DUPLICATE CODE BLOCK 2 - Database setup pattern (duplicate of test_update_notification_settings)
        time.sleep(1)
        
        self.cursor.execute("INSERT INTO settings VALUES ('privacy', 'public')")
        self.db.commit()
        
        time.sleep(1)
        
        # DUPLICATE CODE BLOCK 2 - Database verification pattern (duplicate of test_update_notification_settings)
        result = self.cursor.execute("SELECT * FROM settings WHERE key='privacy'").fetchone()
        assert result is not None
        assert len(result) == 2
        assert result[0] == 'privacy'

