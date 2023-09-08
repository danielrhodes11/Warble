"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase
from models import db, connect_db, Message, User, Follows
from config.test_config import *
from app import app, CURR_USER_KEY
# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['FLASK_ENV'] = 'testing'

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

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
