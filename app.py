import csv
import collections
import dateutil.parser
from io import StringIO

from flask import request
from flask_api import FlaskAPI
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = FlaskAPI(__name__)
CORS(app)
app.config["UPLOAD_FOLDER"] = "/tmp/"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/payroll.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app=app)
migrate = Migrate(app=app, db=db)

from models import TimeReport, TimeReportEntry
from errors import ReportAlreadyExistsError, CSVParsingError

db.create_all()


@app.route('/health', methods=['GET'])
def health():
    return {}


EXPECTED_CSV_HEADER = ["date", "hours worked", "employee id", "job group"]
JOB_GROUP_ALLOW_VALUES = ["A", "B"]


@app.route('/payroll_csv', methods=['POST'])
def payroll_csv():
    report_file = request.files['report']
    stream = StringIO(report_file.read().decode("UTF8"), newline=None)
    headers, *rows, footer = csv.reader(stream)
    headers = list(map(lambda s: s.strip(), headers))
    report_id = int(footer[1])

    if not all(map(lambda cmp: cmp[0] == cmp[1], zip(EXPECTED_CSV_HEADER, headers))):
        raise CSVParsingError("CSV header not as expected")

    if db.session.query(TimeReport).get(report_id) is not None:
        raise ReportAlreadyExistsError("Report with id={id} already exists".format(id=report_id))

    time_report = TimeReport(id=report_id)

    time_report_entries = []
    for idx, row in enumerate(rows):
        try:
            date_str, hours_str, employee_id_str, job_group = map(lambda x: x.strip(), row)
            date = dateutil.parser.parse(date_str)
            hours = float(hours_str)
            employee_id = int(employee_id_str)
            assert job_group in JOB_GROUP_ALLOW_VALUES
        except Exception as e:
            raise CSVParsingError("Error while parsing row# {row}".format(row=idx+2))

        time_report_entries.append(TimeReportEntry(
            report_id=time_report.id,
            employee_id=employee_id,
            date=date,
            hours_worked=hours,
            job_group=job_group,
        ))

    db.session.add(time_report)
    db.session.add_all(time_report_entries)
    db.session.commit()

    return {}, 201


def get_pay_period_start_and_end_date(date):
    start_day = 1
    end_day = 15
    if (date.day > 15):
        start_day = 16
        if date.month in [1, 3, 5, 7, 8, 10, 12]:
            end_day = 31
        elif date.month in [4, 6, 9, 11]:
            end_day = 30
        elif date.month == 2:
            end_day = 28
            if date.year % 4 == 0:
                end_day = 29

    return date.replace(day=start_day), date.replace(day=end_day)


def get_amount_paid_for_entry(entry):
    pay_rate = 0.
    if entry.job_group == "A":
        pay_rate = 20.
    elif entry.job_group == "B":
        pay_rate = 30.

    return pay_rate * entry.hours_worked


def format_date(date):
    return date.strftime("%m/%d/%Y")


def sort_function_for_payroll_report(entry):
    k, v = entry
    (employee_id, (pay_period_start, pay_period_end)) = k
    return (employee_id, pay_period_start)


@app.route('/payroll_report', methods=['GET'])
def payroll_report():
    time_report_entries = \
        db.session.query(TimeReportEntry).all()

    entries_by_employee_id_and_pay_period = collections.defaultdict(list)
    for entry in time_report_entries:
        pay_period = get_pay_period_start_and_end_date(entry.date)
        entries_by_employee_id_and_pay_period[(entry.employee_id, pay_period)].append(entry)

    total_amount_paid_by_employee_id_and_pay_period = \
        {employee_id_and_pay_period: sum(map(get_amount_paid_for_entry, entries))
                                     for employee_id_and_pay_period, entries
                                     in entries_by_employee_id_and_pay_period.items()}

    return [
        {"employee_id": str(employee_id),
         "pay_period": "{start} - {end}".format(start=format_date(pay_period_start),
                                                end=format_date(pay_period_end)),
         "amount_paid": "${amount_paid:.2f}".format(amount_paid=amount_paid)}
        for (employee_id, (pay_period_start, pay_period_end)), amount_paid in
        sorted(list(total_amount_paid_by_employee_id_and_pay_period.items()),
               key=sort_function_for_payroll_report)
    ]


if __name__ == "__main__":
    app.run()
