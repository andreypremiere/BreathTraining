import datetime
from PyQt6.QtCore import QDate


def date_to_qdate(date_obj: datetime.date):
    return QDate(date_obj.year, date_obj.month, date_obj.day)


def qdate_to_date(qdate_obj: QDate):
    return datetime.date(qdate_obj.year(), qdate_obj.month(), qdate_obj.day())
