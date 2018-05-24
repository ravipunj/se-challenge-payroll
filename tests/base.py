from flask_testing import TestCase

from app import app, db


class BaseTestCase(TestCase):
    def create_app(self):
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/payroll_test.db"
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        return app

    def setUp(self):
        db.create_all()

        self.test_client = app.test_client()
        self.db = db

    def tearDown(self):
        self.db.session.remove()
        self.db.drop_all()
