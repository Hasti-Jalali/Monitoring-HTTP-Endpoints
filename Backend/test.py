import unittest
from app import db
from app import User, URL, Request
from  werkzeug.security import generate_password_hash
import uuid

class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db = db
        self.db.create_all()

    def test_create_records(self):
        for i in range(20):
            user = User(
                public_id = str(uuid.uuid4()),
                username = f"user{i}",
                password = generate_password_hash(f"password{i}")
            )
            for j in range(20):
                url = URL(
                address = f"http://www.example{j}.com",
                user_id = user.id,
                threshold = 10
                )
            
            self.db.session.add(user)
            self.db.session.add(url)
        self.db.session.commit()

        self.assertEqual(User.query.count(), 20)
        self.assertEqual(URL.query.count(), 20)
        self.assertEqual(Request.query.count(), 20)

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()

if __name__ == '__main__':
    unittest.main()
