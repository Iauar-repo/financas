from app.models import Users

def get_user_by_email(email):
    user = Users.query.filter_by(email=email).first()

    return user if user else None
