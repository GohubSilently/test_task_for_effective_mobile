from .import_data import ImportData
from users.models import Session


class Command(ImportData):
    model = Session
