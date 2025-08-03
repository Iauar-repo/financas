import random
from faker import Faker

from run import create_app
from app.extensions import db
from app.models import Users
from app.users.repository import insert_provider

fake = Faker("pt_BR")

def seed():
    app = create_app()
    with app.app_context():
        users = [
            Users(name="Rodrigo FL", email="rodrigof.lops@gmail.com", is_admin=1, email_confirmed=1),
            Users(name="Rafael Rondon", email="rrmontebello@gmail.com", is_admin=1, email_confirmed=1),
        ]
        
        for _ in range(50):
            users.append(Users(
                name=fake.name(),
                email=fake.email(),
                email_confirmed=0 if random.random() < 0.1 else 1,
            ))

        db.session.add_all(users)
        db.session.flush()

        for user in Users.query.all():
            insert_provider(user.id,'email',user.email,'senha')

            if random.random() < 0.5 and user.email_confirmed:
                insert_provider(user.id,'google',str(random.randint(10**20, 10**21 - 1)))
        
        db.session.commit()
        print("Seed complete.")

if __name__ == "__main__":
    seed()
