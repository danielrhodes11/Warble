"""Message model tests."""

import os
from unittest import TestCase
from models import db, connect_db, Message, User, Follows, Likes
from config.test_config import *
from app import app, CURR_USER_KEY
from sqlalchemy.exc import IntegrityError


os.environ['FLASK_ENV'] = 'testing'


db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_message_model(self):
        """Does basic model work?"""

        user = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(user)
        db.session.commit()

        message = Message(text="Test message", user_id=user.id)

        db.session.add(message)
        db.session.commit()

        retrieved_message = Message.query.get(message.id)

        self.assertEqual(retrieved_message.text, "Test message")
        self.assertEqual(retrieved_message.user_id, user.id)

    def test_message_without_user(self):
        """Does message model work without user?"""

        message = Message(text="Test message")

        db.session.add(message)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_message_without_text(self):
        """Does message model work without text?"""

        user = User(
            email="dan@test.com",
            username="dan",
            password="HASHED_PASSWORD")

        db.session.add(user)
        db.session.commit()

        message = Message(user_id=user.id)

        db.session.add(message)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_message_likes(self):
        """Test if messages can be liked by users."""
        # Create test users
        user1 = User(username='user1', email='user1@example.com',
                     password='password1')
        user2 = User(username='user2', email='user2@example.com',
                     password='password2')
        db.session.add_all([user1, user2])
        db.session.commit()

        # Create a test message
        message1 = Message(text='Test message 1', user=user1)
        message2 = Message(text='Test message 2', user=user2)
        db.session.add_all([message1, message2])
        db.session.commit()

        # Check if user1 and user2 like the message
        like1 = Likes(
            user_id=user1.id,
            message_id=message1.id
        )
        like2 = Likes(
            user_id=user2.id,
            message_id=message2.id
        )
        db.session.add_all([like1, like2])
        db.session.commit()

        db.session.refresh(message1)
        db.session.refresh(message2)

        # Retrieve the message and check the number of likes
        retrieved_message1 = Message.query.get(message1.id)
        retrieved_message2 = Message.query.get(message2.id)

        self.assertEqual(len(retrieved_message1.likes_from_users), 1)
        self.assertEqual(len(retrieved_message2.likes_from_users), 1)

        # Check if the message is liked by the correct user
        self.assertEqual(
            retrieved_message1.likes_from_users[0].user_id, user1.id)
        self.assertEqual(
            retrieved_message2.likes_from_users[0].user_id, user2.id)

        # Check if the user likes the correct message
        self.assertEqual(
            retrieved_message1.likes_from_users[0].message_id, message1.id)

        self.assertEqual(
            retrieved_message2.likes_from_users[0].message_id, message2.id)
