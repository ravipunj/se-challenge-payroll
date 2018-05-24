from sqlalchemy.orm.exc import FlushError

from app import db
from models import TimeReport
from tests.base import BaseTestCase

def insert_time_report(**overrides):
    time_report_params = {"id": 123}
    time_report_params.update(overrides)

    time_report = TimeReport(**time_report_params)

    db.session.add(time_report)
    db.session.commit()

    return time_report


class TestTimeReport(BaseTestCase):
    def test_repr(self):
        time_report = TimeReport(id=1)
        self.assertEqual(str(time_report), "[TimeReport id=1]")


class TestTimeReportInsertion(BaseTestCase):
    def test_raises_integrity_error_for_missing_id_field(self):
        self.assertRaises(FlushError, insert_time_report, id=None)

    def test_insert_time_report(self):
        time_report = insert_time_report()
        self.assertEqual(db.session.query(TimeReport).one(), time_report)
