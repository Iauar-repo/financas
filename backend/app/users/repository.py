from app.extensions import db
from app.models import Users, AuthProvider
from flask_bcrypt import generate_password_hash

def get_user_by_email(email: str):
    """
    Retrieve a user instance by email

    Parameters:
        email (str): Email address to search for
    
    Returns:
        Users: SQLAlchemy User instance
    """
    return Users.query.filter_by(email=email).first()

def get_user_by_id(id: int):
    """
    Retrieve a user instance by ID

    Parameters:
        id (int): User ID
    
    Returns:
        Users: SQLAlchemy User instance
    """
    return Users.query.filter_by(id=id).first()

def insert_user(data: dict):
    """
    Insert a new user record into Users table.

    Parameters:
        data (dict): Dictionary containing user fields.
                     Required keys: 'name', 'email'.
    Returns:
        None
    """
    db.session.add(Users(
        name = data.get('name'),
        email = data.get('email')
    ))

def insert_provider(user_id: int, provider: str, provider_id: str, password: str = None):
    """
    Insert a new record into the AuthProvider table for a given user.

    Parameters:
        user_id (int): ID of the user to link the provider to.
        provider (str): Name of the provider (e.g., 'email', 'google').
        provider_id (str): Unique identifier from the provider.
        password (str): Raw password to be hashed and stored.
    
    Notes:
        provider_id (str) will always be email to non social logins.

    Returns:
        None
    """
    if provider == 'email':
        db.session.add(AuthProvider(
            user_id = user_id,
            provider = provider,
            provider_user_id = provider_id,
            password_hash = generate_password_hash(password).decode('utf-8')
        ))
    else:
        db.session.add(AuthProvider(
            user_id = user_id,
            provider = provider,
            provider_user_id = provider_id
        ))

def update_user(data: dict, user: Users):
    """
    Update an existing user record with provided fields.

    Parameters:
        data (dict): Dictionary of fields to update.
        user (Users): SQLAlchemy User instance to be updated.

    Notes:
        The following fields cannot be updated:
        - id
        - is_admin
        - email
        - email_confirmed

    Returns:
        None
    """
    blacklist = ['id', 'is_admin', 'email_confirmed', 'email']
    for key,val in data.items():
        if key.lower() not in blacklist:
            setattr(user, key, val)

def get_all_users():
    """
    Retrieve all users.

    Parameters:
        None

    Returns:
        Users: SQLAlchemy User instance
    """
    return Users.query.all()