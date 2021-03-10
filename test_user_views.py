"""User views tests."""

# run these tests like:
#
#    python -m unittest test_user_views.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

# Now we can import app

from app import app

CURR_USER_KEY = "curr_user"

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewsTestCase(TestCase):
	""" testing views for users """
	
	def setUp(self):
		""" test user """
		
		User.query.delete()
		db.session.commit()
		
		self.client = app.test_client()
		
		self.testuser = User.signup(username="madonna", email="madge@gmail.com", password="ilovepets", image_url=None)
		
		db.session.add(self.testuser)
		db.session.commit()
		
		self.user_id = self.testuser.id

	def tearDown(self):
		"""Clean up fouled transactions."""
		
		db.session.rollback()
	
	def test_all_users(self):
		with app.test_client() as client:
			resp = client.get("/users")
			self.assertEqual(resp.status_code, 200)
			print("🌸🌸")
			print("🌸🌸")
			print(resp.data)
			print("🌸🌸")
			print("🌸🌸")
			self.assertEqual(
				resp.data,
				{'user': [{
					'id': self.user_id,
					'username': 'madonna',
					'email': 'madge@gmail.com'
				}]})
	
	def test_get_a_user(self):
		with app.test_client() as client:
			resp = client.get(f"/users/{self.user_id}")
			self.assertEqual(resp.status_code, 200)
			
			self.assertEqual(
				resp.data,
				{'user': {
					'id': self.user_id,
					'username': 'madonna',
					'email': 'madge@gmail.com'}})

	def test_add_user(self):
		with self.client as c:
			with c.session_transaction() as sess:
				sess[CURR_USER_KEY] = self.testuser.id
			resp = c.post("/signup", data={'username': 'lady gaga',
					'email': 'notmadonnna@gmail.com',
					'password': "ilovepets",
					'image_url': None})
			
			# Make sure it redirects
			self.assertEqual(resp.status_code, 302)
			
			new_user = User.query.one()
			self.assertEqual(new_user.username, "lady gaga")
	
	# def test_create_user(self):

# with app.test_client() as client:
		# 	resp = client.post(
		# 		"/user", json={
		# 			'username': 'lady gaga',
		# 			'email': 'notmadonnna@gmail.com',
		# 			'password': "ilovepets",
		# 			'image_url': None
		# 		})
		# 	self.assertEqual(resp.status_code, 201)
		#
		# 	self.assertIsInstance(resp.json['user']['id'], int)
		# 	del resp.json['user']['id']
		#
		# 	self.assertEqual(
		# 		resp.json,
		# 		{"user": {'username': 'lady gaga', 'email': 'notmadonna@gmail.com'}})
		#
		# 	self.assertEqual(User.query.count(), 2)