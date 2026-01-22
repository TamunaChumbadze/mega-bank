import bcrypt
from db import get_connection

def hash_password(password):
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password, password_hash):
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def register_user(username, password):
    """Register a new user and create their account."""
    conn = get_connection()
    if not conn:
        return False, "Database connection error."
    try:
        cursor = conn.cursor()

        # Check if username already exists
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        if cursor.fetchone():
            print("Username '{username}' already exists.")
            return False
        # Hash password and insert user
        password_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s) RETURNING id", 
            (username, password_hash)
        )
        user_id = cursor.fetchone()[0]
        
        # Create account for the user with 0 balamce
        cursor.execute(
            "INSERT INTO accounts (user_id, balance) VALUES (%s, 0.00)", 
            (user_id,)
        )
        conn.commit()
        cursor.close()
        conn.close()
        print(f"User '{username}' registered successfully.")
        return True
    except Exception as e:
        print(f"Error registering user: {e}")
        return False

def login_user(username, password):
    """Authenticate a user and return success status."""
    conn = get_connection()
    if not conn:
        return False, "Database connection error."
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash FROM users WHERE username = %s", (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if not result:
            print("Invalid username or password!")
            return None
        
        user_id, password_hash = result
        if verify_password(password, password_hash):
            return user_id
        else:
            print("Invalid username or password!")
            return None
          
    except Exception as e:
        print(f"Error logging in user: {e}")
        return None
    
# register_user("Bob","secret")
logged_in_user_id = login_user("Bob","secret")
print("Logged in user ID:", logged_in_user_id)