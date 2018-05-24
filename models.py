import datetime

from app import db

class TimeReport(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False, default=lambda: None)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return "[TimeReport id={id}]".format(id=self.id)

    def __eq__(self, other):
        return self.id == other.id


class TimeReportEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    modified = db.Column(db.DateTime, nullable=False,
                         default=datetime.datetime.now, onupdate=datetime.datetime.now)
    report_id = db.Column(db.Integer, db.ForeignKey("time_report.id"))
    employee_id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    hours_worked = db.Column(db.Float(precision=2), nullable=False)
    job_group = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return "[TimeReportEntry employee_id={employee_id} " \
                                "date={date} " \
                                "hours_worked={hours_worked} " \
                                "job_group={job_group}]".format(
                                    employee_id=self.employee_id,
                                    date=self.date,
                                    hours_worked=self.hours_worked,
                                    job_group=self.job_group,
                                )

    def __eq__(self, other):
        return (
            self.report_id == other.report_id and
            self.employee_id == other.employee_id and
            self.date == other.date and
            self.hours_worked == other.hours_worked and
            self.job_group == other.job_group
        )
