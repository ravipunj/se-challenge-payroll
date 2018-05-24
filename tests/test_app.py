from datetime import date
from io import BytesIO

from app import TimeReport, TimeReportEntry
from tests.base import BaseTestCase
from tests.test_models import insert_time_report

STUB_CSV_DATA = b"""date, hours worked, employee id, job group
4/11/2016, 10, 1, A
6/11/2016, 4, 1, A
20/11/2017, 4, 2, B
report id, 42"""


class TestHealthEndpoint(BaseTestCase):
    def test_returns_OK(self):
        response = self.test_client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {})


class TestPayrollCsvEndpoint(BaseTestCase):
    def test_returns_error_if_report_id_aready_exists(self):
        insert_time_report(id=42)
        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(STUB_CSV_DATA), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Report with id=42 already exists"})

    def test_returns_error_if_csv_headers_are_not_as_expected(self):
        stub_csv = b'''hours_worked, date, employee id, job group
        10, 4/11/2016, 1, A
        report id, 42'''

        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(stub_csv), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "CSV header not as expected"})

    def test_returns_error_if_date_cant_be_parsed(self):
        stub_csv = b"""date, hours worked, employee id, job group
        124/521/2214, 10, 1, A
        report id, 42"""

        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(stub_csv), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Error while parsing row# 2"})

    def test_returns_error_if_employee_id_cant_be_parsed(self):
        stub_csv = b"""date, hours worked, employee id, job group
        4/10/2015, 10, e1, A
        report id, 42"""

        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(stub_csv), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Error while parsing row# 2"})

    def test_returns_error_if_hours_worked_cant_be_parsed(self):
        stub_csv = b"""date, hours worked, employee id, job group
        124/521/2214, h10, 1, A
        report id, 42"""

        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(stub_csv), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Error while parsing row# 2"})

    def test_returns_error_if_job_group_not_allowed(self):
        stub_csv = b"""date, hours worked, employee id, job group
        124/521/2214, 10, 1, C
        report id, 42"""

        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(stub_csv), "sample.csv")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "Error while parsing row# 2"})

    def test_insert_time_report_and_entries(self):
        response = self.test_client.post('/payroll_csv',
                                         data={"report": (BytesIO(STUB_CSV_DATA), "sample.csv")})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json(), {})
        self.assertEqual(self.db.session.query(TimeReport).one(), TimeReport(id=42))
        self.assertEqual(
            self.db.session.query(TimeReportEntry)
                            .order_by(TimeReportEntry.date.desc(),
                                      TimeReportEntry.employee_id.desc()).all(),
            [TimeReportEntry(report_id=42,
                             employee_id=2,
                             date=date(2017, 11, 20),
                             hours_worked=4,
                             job_group="B"),
             TimeReportEntry(report_id=42,
                             employee_id=1,
                             date=date(2016, 6, 11),
                             hours_worked=4,
                             job_group="A"),
             TimeReportEntry(report_id=42,
                             employee_id=1,
                             date=date(2016, 4, 11),
                             hours_worked=10,
                             job_group="A")]
        )