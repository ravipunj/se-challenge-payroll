import collections
import dateutil.parser

from app import db
from errors import CSVParsingError, ReportAlreadyExistsError
from models import TimeReport, TimeReportEntry

EXPECTED_CSV_HEADER = ["date", "hours worked", "employee id", "job group"]
JOB_GROUP_ALLOW_VALUES = ["A", "B"]


def _validate_header(header):
    header = list(map(lambda s: s.strip(), header))

    if not all(map(lambda cmp: cmp[0] == cmp[1], zip(EXPECTED_CSV_HEADER, header))):
        raise CSVParsingError("CSV header not as expected")


def _parse_footer(footer):
    report_id = int(footer[1])

    if db.session.query(TimeReport).get(report_id) is not None:
        raise ReportAlreadyExistsError("Report with id={id} already exists".format(id=report_id))

    return report_id


def _parse_row_for_time_report(row, time_report):
    date_str, hours_str, employee_id_str, job_group = map(lambda x: x.strip(), row)
    date = dateutil.parser.parse(date_str)
    hours = float(hours_str)
    employee_id = int(employee_id_str)
    assert job_group in JOB_GROUP_ALLOW_VALUES

    return TimeReportEntry(
        report_id=time_report.id,
        employee_id=employee_id,
        date=date,
        hours_worked=hours,
        job_group=job_group,
    )


def _parse_rows_for_time_report(rows, time_report):
    time_report_entries = []
    for idx, row in enumerate(rows):
        try:
            time_report_entry = _parse_row_for_time_report(row, time_report)
            time_report_entries.append(time_report_entry)
        except Exception:
            raise CSVParsingError("Error while parsing row# {row}".format(row=idx + 2))
    return time_report_entries


def get_time_report_and_entries_from_csv(csv_reader):
    header, *rows, footer = csv_reader
    _validate_header(header)
    report_id = _parse_footer(footer)

    time_report = TimeReport(id=report_id)
    time_report_entries = _parse_rows_for_time_report(rows, time_report)

    return time_report, time_report_entries


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


def calculate_total_amounts_paid_for_time_report_entries(time_report_entries):
    entries_by_employee_id_and_pay_period = collections.defaultdict(list)
    for entry in time_report_entries:
        pay_period = get_pay_period_start_and_end_date(entry.date)
        entries_by_employee_id_and_pay_period[(entry.employee_id, pay_period)].append(entry)

    return {employee_id_and_pay_period: sum(map(get_amount_paid_for_entry, entries))
            for employee_id_and_pay_period, entries
            in entries_by_employee_id_and_pay_period.items()}
