import datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

from app import db
from models import TimeReport, TimeReportEntry
from tests.base import BaseTestCase

def insert_time_report(**overrides):
    time_report_params = {"id": 123}
    time_report_params.update(overrides)

    time_report = TimeReport(**time_report_params)

    db.session.add(time_report)
    db.session.commit()

    return time_report

def insert_time_report_entry(**overrides):
    time_report = \
        overrides.pop("time_report") if "time_report" in overrides else insert_time_report()
    time_report_entry_params = {
        "report_id": time_report.id,
        "employee_id": 99,
        "date": datetime.date(2010, 4, 23),
        "hours_worked": 7,
        "job_group": "A"
    }
    time_report_entry_params.update(overrides)

    time_report_entry = TimeReportEntry(**time_report_entry_params)

    db.session.add(time_report_entry)
    db.session.commit()

    return time_report_entry


class TestTimeReport(BaseTestCase):
    def test_repr(self):
        time_report = TimeReport(id=1)
        self.assertEqual(str(time_report), "[TimeReport id=1]")


class TestTimeReportInsertion(BaseTestCase):
    def test_raises_error_for_missing_id_field(self):
        self.assertRaises(FlushError, insert_time_report, id=None)

    def test_inserts_time_report(self):
        time_report = insert_time_report()
        self.assertEqual(db.session.query(TimeReport).one(), time_report)


class TestTimeReportEntry(BaseTestCase):
    def test_repr(self):
        time_report_entry = TimeReportEntry(
            report_id=1,
            employee_id=1,
            hours_worked=3,
            date=datetime.date(2014, 5, 6),
            job_group="A",
        )
        self.assertEqual(
            str(time_report_entry),
            "[TimeReportEntry employee_id=1 date=2014-05-06 hours_worked=3 job_group=A]"
        )


class TestTimeReportEntryInsertion(BaseTestCase):
    def test_raises_error_for_missing_employee_id(self):
        self.assertRaises(IntegrityError, insert_time_report_entry, employee_id=None)

    def test_raises_error_for_missing_date(self):
        self.assertRaises(IntegrityError, insert_time_report_entry, date=None)

    def test_raises_error_for_missing_hours_worked(self):
        self.assertRaises(IntegrityError, insert_time_report_entry, hours_worked=None)

    def test_raises_error_for_missing_job_group(self):
        self.assertRaises(IntegrityError, insert_time_report_entry, job_group=None)

    def test_inserts_time_report_entry(self):
        time_report_entry = insert_time_report_entry()
        self.assertEqual(db.session.query(TimeReportEntry).one(), time_report_entry)
