"""test user views."""

import os
from unittest import TestCase
from models import db, connect_db, Message, User, Follows, Likes
from config.test_config import *
from app import app, CURR_USER_KEY
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup


os.environ['FLASK_ENV'] = 'testing'


db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

        user = User.signup(username='testuser',
                           email='test@example.com',
                           password='password',
                           image_url=None,
                           header_image_url=None,
                           bio=None,
                           location=None)

        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        """Clean up fouled transactions."""

        db.session.rollback()

    def test_access_following_page_logged_in(self):
        """Can logged in user access following page?"""

        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = self.user.id

        resp = self.client.get(f'/users/{self.user.id}/following')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testuser', str(resp.data))

    def test_access_following_page_logged_out(self):
        """Can logged out user access following page?"""

        resp = self.client.get(f'/users/{self.user.id}/following',
                               follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', str(resp.data))

    def test_add_message_as_self(self):
        """Can logged in user add message as self?"""

        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = self.user.id

        resp = self.client.post('/messages/new',
                                data={'text': 'test message'},
                                follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('test message', str(resp.data))

    def test_add_message_as_other(self):
        """Can logged out user add message as other user?"""

        resp = self.client.post('/messages/new',
                                data={'text': 'test message'},
                                follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', str(resp.data))

    def test_access_followers_page_logged_in(self):
        """Can logged in user access followers page?"""

        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = self.user.id

        resp = self.client.get(f'/users/{self.user.id}/followers')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testuser', str(resp.data))

    def test_access_followers_page_logged_out(self):
        """Can logged out user access followers page?"""

        resp = self.client.get(f'/users/{self.user.id}/followers',
                               follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', str(resp.data))

    def test_access_user_page_logged_in(self):
        """Can logged in user access user page?"""

        with self.client.session_transaction() as session:
            session[CURR_USER_KEY] = self.user.id

        resp = self.client.get(f'/users/{self.user.id}')

        self.assertEqual(resp.status_code, 200)
        self.assertIn('testuser', str(resp.data))

    def test_access_user_page_logged_out(self):
        """Can logged out user access user page?"""

        resp = self.client.get(f'/users/{self.user.id}',
                               follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Access unauthorized', str(resp.data))
