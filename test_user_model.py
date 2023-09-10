"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, connect_db, Message, User, Follows, Bcrypt
from config.test_config import *
from app import app, CURR_USER_KEY
from sqlalchemy.exc import IntegrityError

bcrypt = Bcrypt()


os.environ['FLASK_ENV'] = 'testing'


db.create_all()


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)

        db.session.rollback()

    def test_repr(self):
        """Does the repr method work as expected?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        expected_repr = f"<User #{u.id}: {u.username}, {u.email}>"
        self.assertEqual(expected_repr, repr(u))

        db.session.rollback()

    def test_is_following(self):
        """Does is_following successfully detect when user1 is following user2?"""

        u1 = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="trina@test.com",
            username="trina",
            password="HASHED_PASSWORD"
        )
        db.session.add_all([u1, u2])
        db.session.commit()

        u1.following.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_following(u2))

        db.session.rollback()

    def test_is_not_following(self):
        """Does is_following successfully detect when user1 is not following user2?"""

        u1 = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="trina@test.com",
            username="trina",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertFalse(u1.is_following(u2))

        db.session.rollback()

    def test_is_followed_by(self):
        """Does is_followed_by successfully detect when user1 is followed by user2?"""

        u1 = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="trina@test.com",
            username="trina",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        u1.followers.append(u2)
        db.session.commit()

        self.assertTrue(u1.is_followed_by(u2))

        db.session.rollback()

    def test_is_not_followed_by(self):
        """Does is_followed_by successfully detect when user1 is not followed by user2?"""

        u1 = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD"
        )
        u2 = User(
            email="trina@test.com",
            username="trina",
            password="HASHED_PASSWORD"
        )

        db.session.add_all([u1, u2])
        db.session.commit()

        self.assertFalse(u1.is_followed_by(u2))

        db.session.rollback()

    def test_signup(self):
        """Does User.signup successfully create a new user given valid credentials?"""

        u = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, "dan")
        self.assertEqual(u.email, "dan@test.com")

        db.session.rollback()

    def test_signup_fail(self):
        """Does User.signup fail to create a new user if any of the validations (e.g. uniqueness, non-nullable fields) fail?"""

        u = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        u2 = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(u2)
        with self.assertRaises(IntegrityError) as context:
            db.session.commit()

            self.assertTrue(
                'UNIQUE constraint failed: users.username' in str(context.exception))

        db.session.rollback()

    def test_authenticate(self):
        """Does User.authenticate successfully return a user when given a valid username and password?"""
        hashed_pwd = bcrypt.generate_password_hash(
            "mypassword").decode('UTF-8')

        u = User(
            email="dan@test.com",
            username="dan",
            password=hashed_pwd)

        db.session.add(u)
        db.session.commit()

        self.assertEqual(User.authenticate("dan", "mypassword"), u)

        db.session.rollback()

    def test_authenticate_fail(self):
        """Does User.authenticate fail to return a user when the username is invalid?"""

        u = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(u)
        db.session.commit()

        self.assertFalse(User.authenticate("daniel", "HASHED_PASSWORD"))

        db.session.rollback()

    def test_authenticate_fail_password(self):
        """Does User.authenticate fail to return a user when the password is invalid?"""

        hashed_pwd = bcrypt.generate_password_hash(
            "mypassword").decode('UTF-8')

        u = User(
            email="dan@test.com",
            username="dan",
            password=hashed_pwd)

        db.session.add(u)
        db.session.commit()

        self.assertFalse(User.authenticate("dan", "wrongpassword"))

        db.session.rollback()
