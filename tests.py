from unittest import TestCase
from app import app
from models import db, Cupcake

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

with app.app_context():
    db.drop_all()
    db.create_all()

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Make demo data."""
        with app.app_context():
            Cupcake.query.delete()  # Clear previous data
            cupcake = Cupcake(**CUPCAKE_DATA)  # Create a new cupcake instance
            db.session.add(cupcake)  # Add it to the session
            db.session.commit()  # Commit the transaction

            # Fully load the cupcake instance before the session is closed
            db.session.refresh(cupcake)  # This ensures the data is fully loaded
            self.cupcake = cupcake  # Assign the instance to self.cupcake

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()


    #test methods go here, such as test_list_cupcakes, test_get_cupcake, etc.

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,  # The instance is bound to the session and accessible
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)
            self.assertEqual(resp.status_code, 201)

            data = resp.json
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

    def test_update_cupcake(self):
        """Test updating an existing cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            update_data = {
                "flavor": "UpdatedFlavor",
                "size": "UpdatedSize",
                "rating": 8.5,
                "image": "http://test.com/updated_cupcake.jpg"
            }
            resp = client.patch(url, json=update_data)
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "UpdatedFlavor",
                    "size": "UpdatedSize",
                    "rating": 8.5,
                    "image": "http://test.com/updated_cupcake.jpg"
                }
            })

    def test_delete_cupcake(self):
        """Test deleting an existing cupcake."""
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.delete(url)
            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {"message": "Deleted"})

            self.assertEqual(Cupcake.query.count(), 0)
