import csv
from io import StringIO

import dateutil.parser
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



if __name__ == "__main__":
    app.run()
